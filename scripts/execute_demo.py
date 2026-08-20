"""Execute the workshop in credential-free demo mode and save safe outputs."""

from __future__ import annotations

import os
from pathlib import Path

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "01_llm_chat_workshop.ipynb"


def main() -> None:
    os.environ["LLM_PROVIDER"] = "demo"
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=120,
        kernel_name="llm-workshop",
        resources={"metadata": {"path": str(ROOT)}},
    )
    client.execute()
    nbformat.write(notebook, NOTEBOOK)
    print(f"Executed in demo mode: {NOTEBOOK.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
