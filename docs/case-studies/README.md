# Case studies

Anomaly cases for the diagnose path. Two (GME, AAPL) now run on **real**
quotes both days via `src/explain_my_option/data/historical_chain.py`
(DoltHub `post-no-preference/options`); the rest stay **synthetic**
(spot/IV tuned for residual behavior) with **frozen as-of news** drawn from
cited public sources — not live headlines mixed with a historical `as_of`.
See `tests/ci/stress_fixtures/README.md` for why each synthetic case can't
be (or, for GME/AAPL, no longer needs to be) converted.

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

**Historical cases (real chains):**

| Case | As-of tape | Desk lesson | Walkthrough |
|------|------------|-------------|-------------|
| GME real (2021-01-25) | Same-day CNBC squeeze | Real quotes: IV ~308%→358%, `borrow_regime=extreme` (`q_implied`≈58%) | — |
| AAPL real (2023-11-09) | Forbes ex-div reminder | Real $0.24 dividend; Taylor misses the div vs early-exercise split | [aapl_exdiv_attribution.md](aapl_exdiv_attribution.md) |

**Stress fixtures (synthetic inputs):**

| Case | As-of tape | Desk lesson | Walkthrough |
|------|------------|-------------|-------------|
| META (2022-02-03) | CNBC gap, Reuters options vol | Overnight gap + IV crush on the blotter | — |
| AAPL synthetic (2023-11-09) | Forbes ex-div reminder | Taylor misses the div vs early-exercise split | [aapl_exdiv_attribution.md](aapl_exdiv_attribution.md) |
| GME synthetic (2021-01-25) | Same-day CNBC squeeze | Borrow / squeeze is tape context, not an engine factor | — |
| VOW (2008-10-27) | Porsche SE 10-26 float disclosure | Large residual → escalate, don't invent | [vow_float_squeeze_2008.md](vow_float_squeeze_2008.md) |
| VMW (2008-01-28) | Same-day earnings reaction | Borrow is not modeled → low residual is expected | — |

```bash
python tests/historical/run.py --case vow_float_squeeze_2008
python tests/historical/run.py --case aapl_exdiv_2023
```

Frozen product reports (not the gitignored `output/` archives): [docs/samples/](../samples/README.md).
