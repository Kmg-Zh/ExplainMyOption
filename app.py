"""Explain My Option — entrypoint.

Two ways to run:

    # CLI
    python app.py --ticker AAPL --type call
    python app.py --fixture vol_crush

    # Streamlit UI
    streamlit run app.py

D1: the actual CLI/Streamlit implementation lives in
``src/explain_my_option/cli.py`` so the installed console script
(``explain-my-option``, ``pyproject.toml``'s ``[project.scripts]``) can
import it — ``pip install .`` only packages ``src/``
(``[tool.setuptools.packages.find]``), so an entry point pointing at this
root-level file (``app:run_cli``) used to raise ``ModuleNotFoundError:
No module named 'app'`` after a real install, since this file is never
installed. This file stays only as the thing `python app.py` and
`streamlit run app.py` invoke directly from a checkout.
"""

from __future__ import annotations

from explain_my_option.cli import _is_streamlit_runtime, run_cli, run_streamlit

if __name__ == "__main__":
    if _is_streamlit_runtime():
        run_streamlit()
    else:
        run_cli()
else:
    # `streamlit run app.py` imports the module rather than running __main__.
    if _is_streamlit_runtime():
        run_streamlit()
