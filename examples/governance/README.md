# Governance examples

Five short scripts. In each one an LLM role misbehaves on purpose, or the data
is bad, and you see what code lets through to the report. They run offline,
with no key and no network: the LLM roles are scripted with
`explain_my_option.testing`, and the market data comes from committed fixtures.

```bash
for f in examples/governance/0*.py; do echo "== $f"; python "$f"; echo; done
```

| Script | Rule | What you will see |
|--------|------|-------------------|
| [`01_invented_number.py`](01_invented_number.py) | The narrator never prints a figure | The narrator claims "$2.50"; code rejects the reply and the report ships the rule-based summary |
| [`02_injected_headline.py`](02_injected_headline.py) | Retrieved text is data, never instructions | The prompt the narrator received, with the attacker's forged closing tag escaped; the obeyed "50% surge" never becomes the verdict |
| [`03_verifier_needs_code_proof.py`](03_verifier_needs_code_proof.py) | An LLM's hard FAIL counts only when code reproduces it | A false alarm downgraded to PARTIAL, next to a real violation that stops the leg |
| [`04_quiet_day.py`](04_quiet_day.py) | A quiet day costs nothing and says nothing | A real SPY quiet day: 0 LLM calls, no search, free tools only; a material move for contrast |
| [`05_data_gap.py`](05_data_gap.py) | A data gap is not a market story | The leg stops before pricing and before any LLM, and the report names the coverage gap |

Each script names the test that pins its rule, and
[`tests/agent/test_examples.py`](../../tests/agent/test_examples.py) runs all of
them on every push. The full list of rules, one row each, is in
[`tests/agent/README.md`](../../tests/agent/README.md). How often a real model
breaks them is measured in [`evals/`](../../evals/README.md).
