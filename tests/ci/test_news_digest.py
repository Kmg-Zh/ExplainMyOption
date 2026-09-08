"""Intel digest tests: coarse filter and labeled background (not a ticker gate)."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

from explain_my_option.data_loader import NewsItem
from explain_my_option.intel.relevance import coarse_keep
from explain_my_option.pipeline.digest import IntelDigest, run_intel_digest
from explain_my_option.report.catalysts import with_inferred_microstructure
from explain_my_option.report.synthesis import _catalyst_tags, _layer_b_news


class _MockDigester:
    def structured_invoke(self, *, system, human, schema):
        del system, human, schema
        return IntelDigest(
            relevant=[
                {
                    "title": "Meta shares fall after earnings miss",
                    "publisher": "Reuters",
                    "mechanisms": ["earnings", "made-up-tag"],
                    "one_line_fact": "The headline attributes the move to an earnings miss.",
                }
            ],
            discarded=[
                {
                    "title": "Options Strategy | How to Position with Options",
                    "reason": "generic promo content",
                }
            ],
            mechanisms=["earnings", "made-up-tag"],
            brief="One earnings-linked headline is relevant to META.",
        )


def test_coarse_keep_drops_promotional_noise():
    assert not coarse_keep("Options Strategy | How to Position with Options")
    assert not coarse_keep("Moomoo Community weekly roundup")
    assert coarse_keep("Meta shares fall after earnings miss")


def test_run_intel_digest_clamps_mechanisms_and_keeps_relevant():
    news = [
        NewsItem(
            title="Meta shares fall after earnings miss",
            publisher="Reuters",
            link="https://example.com/meta",
            published="2026-09-02",
        ),
        NewsItem(
            title="Options Strategy | How to Position with Options",
            publisher="Moomoo",
            link="https://example.com/promo",
            published="2026-09-02",
        ),
    ]
    digest = run_intel_digest(role=_MockDigester(), ticker="META", news=news)
    assert len(digest.relevant) == 1
    assert digest.relevant[0].title == "Meta shares fall after earnings miss"
    assert digest.relevant[0].mechanisms == ["earnings"]
    assert digest.mechanisms == ["earnings"]
    assert digest.discarded
    assert digest.discarded[0].reason


class _BoomDigester:
    def structured_invoke(self, *, system, human, schema):
        raise RuntimeError("digest down")


def test_run_intel_digest_invoke_failure_does_not_invent_tags():
    news = [
        NewsItem(title="Broadcom's Q3 earnings beat just isn't 'enough'"),
        NewsItem(title="Alphabet expands cloud capacity"),
    ]
    digest = run_intel_digest(role=_BoomDigester(), ticker="GOOGL", news=news)
    assert digest.relevant == []
    assert digest.mechanisms == []
    assert "failed" in digest.reason
    kept = _layer_b_news(news, digest, {"intel_digest": digest.model_dump()})
    assert [hit.title for hit in kept] == [item.title for item in news]


def test_run_intel_digest_without_role_fails_soft():
    news = [NewsItem(title="Meta shares fall after earnings miss", publisher="Reuters")]
    digest = run_intel_digest(role=None, ticker="META", news=news)
    assert digest.relevant == []
    assert digest.mechanisms == []
    assert "not configured" in digest.reason


class _PeerBackgroundDigester:
    """Yahoo mix: subject ticker stays relevant; peers are background, not discarded."""

    def structured_invoke(self, *, system, human, schema):
        del system, schema
        relevant = []
        background = []
        for line in human.splitlines():
            if not line[:1].isdigit():
                continue
            title = line.split(". ", 1)[-1].rsplit(" (", 1)[0]
            if "Alphabet" in title:
                relevant.append(
                    {
                        "title": title,
                        "publisher": "",
                        "mechanisms": [],
                        "one_line_fact": "Subject matches the target ticker.",
                    }
                )
            else:
                background.append(
                    {
                        "title": title,
                        "publisher": "",
                        "mechanisms": ["earnings"],
                        "one_line_fact": "Peer or sector tape.",
                    }
                )
        return IntelDigest(
            relevant=relevant,
            background=background,
            discarded=[],
            mechanisms=["earnings"],
            brief="Alphabet is relevant; peers retained as background.",
        )


def test_run_intel_digest_keeps_sept2_peers_as_background():
    news = [
        NewsItem(title="Broadcom's Q3 earnings beat just isn't 'enough' to keep investors happy"),
        NewsItem(title="Warren Buffett’s biggest bet has a dividend secret"),
        NewsItem(title="Two Utility Dividend Plays Are Quietly Beating XOM, CVX On Yield"),
        NewsItem(title="Alphabet expands cloud capacity after regulatory ruling"),
    ]
    digest = run_intel_digest(role=_PeerBackgroundDigester(), ticker="GOOGL", news=news)
    titles = [row.title for row in digest.relevant]
    assert titles == ["Alphabet expands cloud capacity after regulatory ruling"]
    background = " ".join(row.title for row in digest.background)
    assert "Broadcom" in background
    assert "Buffett" in background
    assert "XOM" in background
    assert all(not row.mechanisms for row in digest.background)
    assert digest.mechanisms == []
    assert "earnings" not in digest.mechanisms
    assert "ex-dividend" not in digest.mechanisms


class _RelatedIssuerDigester:
    def structured_invoke(self, *, system, human, schema):
        del system, schema
        titles = []
        for line in human.splitlines():
            if line[:1].isdigit():
                titles.append(line.split(". ", 1)[-1].rsplit(" (", 1)[0])
        return IntelDigest(
            relevant=[
                {
                    "title": titles[0],
                    "publisher": "Porsche SE",
                    "mechanisms": ["float", "squeeze"],
                    "one_line_fact": "Related-issuer stake disclosure names VW.",
                }
            ],
            background=[],
            discarded=[],
            mechanisms=["float", "squeeze"],
            brief="Porsche disclosure is relevant to VOW.",
        )


def test_run_intel_digest_keeps_related_issuer_for_vow():
    news = [
        NewsItem(
            title="Porsche disclosed 74.1% of VW voting stock via shares plus cash-settled options, collapsing free float",
            publisher="Porsche SE",
        )
    ]
    digest = run_intel_digest(role=_RelatedIssuerDigester(), ticker="VOW.DE", news=news)
    assert len(digest.relevant) == 1
    assert "Porsche" in digest.relevant[0].title
    assert "VW" in digest.relevant[0].title
    assert digest.mechanisms == ["float", "squeeze", "borrow"]
    assert digest.discarded == []


def test_run_intel_digest_promotes_microstructure_when_digest_empty():
    news = [
        NewsItem(
            title="GameStop jumps amid retail frenzy as an epic short squeeze continues; more than 138% of the float was sold short",
            publisher="CNBC",
        )
    ]
    digest = run_intel_digest(role=None, ticker="GME", news=news)
    assert digest.relevant
    assert "squeeze" in digest.mechanisms
    assert "borrow" in digest.mechanisms


def test_inferred_microstructure_from_squeeze_and_float():
    assert with_inferred_microstructure(["squeeze"]) == ["squeeze", "borrow"]
    assert "squeeze" in with_inferred_microstructure(["float"])


def test_layer_b_news_keeps_coarse_titles_when_digest_relevant_empty():
    news = [
        NewsItem(title="Options Strategy | How to Position with Options"),
        NewsItem(title="Broadcom's Q3 earnings beat just isn't 'enough'"),
        NewsItem(title="Alphabet expands cloud capacity"),
    ]
    digest = IntelDigest(
        relevant=[],
        background=[],
        discarded=[{"title": news[1].title, "reason": "peer"}],
        mechanisms=[],
        brief="No relevant catalysts.",
        reason="",
    )
    findings = {"intel_digest": digest.model_dump()}
    kept = _layer_b_news(news, digest, findings)
    assert [hit.title for hit in kept] == [news[1].title, news[2].title]
    assert _catalyst_tags(news, findings) == []


if __name__ == "__main__":
    test_coarse_keep_drops_promotional_noise()
    test_run_intel_digest_clamps_mechanisms_and_keeps_relevant()
    test_run_intel_digest_without_role_fails_soft()
    test_run_intel_digest_invoke_failure_does_not_invent_tags()
    test_run_intel_digest_keeps_sept2_peers_as_background()
    test_run_intel_digest_keeps_related_issuer_for_vow()
    test_run_intel_digest_promotes_microstructure_when_digest_empty()
    test_inferred_microstructure_from_squeeze_and_float()
    test_layer_b_news_keeps_coarse_titles_when_digest_relevant_empty()
    print("OK — news digest tests passed")
