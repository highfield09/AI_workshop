"""Validate notebook structure, outputs, and basic secret hygiene."""

from __future__ import annotations

import re
from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "01_start_here.ipynb"
REQUIRED_HEADINGS = [
    "## Stage 1 — Find your way around",
    "## Stage 2 — Choose an AI helper",
    "## Stage 3 — Ask, compare, and question",
    "## Next — Six vibe-coding sandboxes",
    "## Orientation complete",
]
REQUIRED_SNIPPETS = [
    "Keep the lesson inside the available notebook width",
    "KEY CONCEPT · TOKEN EFFICIENCY",
    "PROMPTING RESOURCES",
    "Read the icons at the end of each model option",
    "moonshotai/Kimi-K3",
    "Always know where your output is going",
    "tasks/stage3_answers.json",
]
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(api[_-]?key\s*[=:]\s*)['\"][^'\"]{12,}['\"]", re.I),
]


def output_text(output) -> str:
    chunks = []
    if "text" in output:
        value = output["text"]
        chunks.append("".join(value) if isinstance(value, list) else value)
    for value in output.get("data", {}).values():
        if isinstance(value, str):
            chunks.append(value)
        elif isinstance(value, list):
            chunks.extend(item for item in value if isinstance(item, str))
    return "\n".join(chunks)


def main() -> None:
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    nbformat.validate(notebook)

    markdown = "\n".join(
        cell.source for cell in notebook.cells if cell.cell_type == "markdown"
    )
    missing = [heading for heading in REQUIRED_HEADINGS if heading not in markdown]
    if missing:
        raise SystemExit(f"Missing workshop sections: {', '.join(missing)}")

    missing_snippets = [text for text in REQUIRED_SNIPPETS if text not in markdown]
    if missing_snippets:
        raise SystemExit(
            f"Missing workshop concepts: {', '.join(missing_snippets)}"
        )

    expected_error_cells = [
        index
        for index, cell in enumerate(notebook.cells)
        if "expected-error" in cell.get("metadata", {}).get("tags", [])
    ]
    if len(expected_error_cells) != 1:
        raise SystemExit(
            "Notebook must contain exactly one intentional repair cell; "
            f"found {expected_error_cells}"
        )

    unexpected_errors = [
        index
        for index, cell in enumerate(notebook.cells)
        if cell.cell_type == "code"
        if "expected-error" not in cell.get("metadata", {}).get("tags", [])
        for output in cell.get("outputs", [])
        if output.get("output_type") == "error"
    ]
    if unexpected_errors:
        raise SystemExit(
            f"Notebook has unexpected error outputs in cells: {unexpected_errors}"
        )

    searchable = [cell.source for cell in notebook.cells]
    searchable.extend(
        output_text(output)
        for cell in notebook.cells
        if cell.cell_type == "code"
        for output in cell.get("outputs", [])
    )
    for pattern in SECRET_PATTERNS:
        if any(pattern.search(text) for text in searchable):
            raise SystemExit(f"Possible credential matched {pattern.pattern!r}")

    executed = sum(
        cell.cell_type == "code" and cell.get("execution_count") is not None
        for cell in notebook.cells
    )
    print(
        f"Validated {NOTEBOOK.relative_to(ROOT)}: "
        f"{len(notebook.cells)} cells, {executed} executed code cells"
    )


if __name__ == "__main__":
    main()
