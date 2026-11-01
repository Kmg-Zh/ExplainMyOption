"""Explain My Option from a checkout: ``python app.py ...`` or ``streamlit run app.py``.

The implementation lives in ``explain_my_option.cli`` so the installed
``explain-my-option`` console script works too.
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
