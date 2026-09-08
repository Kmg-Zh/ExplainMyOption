# Notebooks

**Product code stays in `src/` and `app.py`.** Notebooks here are for visitors: how to use the package, and compiled graph diagrams. They are not shipped runtime.

Default cells **do not call OpenAI**.

| Notebook | Purpose | Needs API key? |
|----------|---------|----------------|
| [getting_started.ipynb](getting_started.ipynb) | `ExplainMyOption` on the `vol_crush` fixture (mock narrator) | No |
| [langgraph_architecture.ipynb](langgraph_architecture.ipynb) | Live LangGraph topology (Mermaid / PNG from compiled graphs) | No |

Start here: **[getting_started.ipynb](getting_started.ipynb)**.

## Run

From repo root with `.venv` activated:

```bash
pip install -r requirements.txt ipykernel
python -m ipykernel install --user --name explain-my-option
jupyter lab notebooks/getting_started.ipynb
```

Or open a notebook in your editor and pick the `.venv` kernel. Cwd may be the repo root or `notebooks/` — `tests/bootstrap.py` finds `src/explain_my_option/`.

**PNG cells** in the architecture notebook call LangGraph `draw_mermaid_png()` (often via mermaid.ink). If the network fails, the notebook falls back to printing Mermaid source — same as Streamlit's topology tab in `app.py`.

Canonical Mermaid helpers: `src/explain_my_option/graph/topology.py` (`pipeline_mermaid`, `leg_mermaid`, `book_mermaid`).
