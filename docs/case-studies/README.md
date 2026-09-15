# Case studies

Historical anomaly fixtures for the diagnose path. Each case is **synthetic**
(spot/IV tuned for residual behavior) with **frozen as-of news** drawn from cited
public sources — not live headlines mixed with a historical `as_of`.

Walkthroughs explain the **mechanism** (Taylor vs residual, what search is allowed
to add). They are not a scoreboard.

## News lineage

| Feed | What it is | Agent sees it? |
|------|------------|----------------|
| `as_of_news` | Headlines with `published <= case.date` | Yes (`frozen_news_for_case`) |
| `ground_truth` | Later recaps, papers, pedagogy | No — eval key only |
| `input_text` | Human scenario note | No |

Manifest: `tests/historical/historical_test_cases.json`  
Offline check: `python tests/historical/test_news_lineage.py`

| Case | As-of tape | Desk lesson | Walkthrough |
|------|------------|-------------|-------------|
| META (2022-02-03) | CNBC gap, Reuters options vol | Overnight gap + IV crush on the blotter | — |
| AAPL (2023-11-09) | Forbes ex-div reminder | Taylor misses the div vs early-exercise split | [aapl_exdiv_attribution.md](aapl_exdiv_attribution.md) |
| GME (2021-01-25) | Same-day CNBC squeeze | Borrow / squeeze is tape context, not an engine factor | — |
| VOW (2008-10-27) | Porsche SE 10-26 float disclosure | Large residual → escalate, don't invent | [vow_float_squeeze_2008.md](vow_float_squeeze_2008.md) |
| VMW (2008-01-28) | Same-day earnings reaction | Borrow is not modeled → low residual is expected | — |

```bash
python tests/historical/run.py --case vow_float_squeeze_2008
python tests/historical/run.py --case aapl_exdiv_2023
```

Frozen product reports (not the gitignored `output/` archives): [docs/samples/](../samples/README.md).
