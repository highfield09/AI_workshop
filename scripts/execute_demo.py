"""Execute the workshop in credential-free demo mode and save safe outputs."""

from __future__ import annotations

import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from llm_workshop.course import WORKBOOKS


def main() -> None:
    previous = {key: os.environ.get(key) for key in ("LLM_PROVIDER", "WORKSHOP_DEMO_ANSWERS")}
    try:
        with TemporaryDirectory(prefix="workshop-demo-") as temporary:
            os.environ["LLM_PROVIDER"] = "demo"
            os.environ["WORKSHOP_DEMO_ANSWERS"] = temporary
            for stem, _, _ in WORKBOOKS:
                path = ROOT / "notebooks" / f"{stem}.ipynb"
                notebook = nbformat.read(path, as_version=4)
                notebook.metadata.pop("widgets", None)
                for cell in notebook.cells:
                    if cell.cell_type == "code":
                        cell.outputs = []
                        cell.execution_count = None
                client = NotebookClient(
                    notebook, timeout=120, kernel_name="llm-workshop",
                    allow_errors=False, resources={"metadata": {"path": str(ROOT)}},
                )
                # Only the deliberate debugging cell may fail.
                for cell in notebook.cells:
                    tags = cell.metadata.get("tags", [])
                    if "expected-error" in tags and "raises-exception" not in tags:
                        tags.append("raises-exception")
                client.execute()
                nbformat.write(notebook, path)
                print(f"Executed with blank isolated answers: {path.relative_to(ROOT)}")
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


if __name__ == "__main__":
    main()
