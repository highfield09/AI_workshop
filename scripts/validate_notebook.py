"""Validate notebook structure, outputs, and basic secret hygiene."""

from __future__ import annotations

import csv
import re
from collections import Counter
from datetime import date
from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "01_start_here.ipynb"
EFFORT_REPORT = ROOT / "Resources" / "2026 Agentic Coding Trends Report.pdf"
CATALOGUE_DATA = ROOT / "data" / "notebook1"
CATALOGUE_CSV = CATALOGUE_DATA / "products.csv"
REQUIRED_HEADINGS = [
    "## Stage 1 — Find your way around",
    "## Stage 2 — Choose an AI helper",
    "## Stage 3 — Ask, compare, and question",
    "## Main task — Build and refine a shopping catalogue",
    "## Orientation complete",
]
REQUIRED_SNIPPETS = [
    "Keep the lesson inside the available notebook width",
    "KEY CONCEPT · TOKEN EFFICIENCY",
    "KEY CONCEPT · MODEL EFFORT",
    "Effort is a <b>signal, not a strict token budget</b>",
    "20 questions",
    "PROMPTING RESOURCES",
    "Google AI Mode",
    "Read the icons at the end of each model option",
    "moonshotai/Kimi-K3",
    "Gemini 3.5 Flash-Lite",
    "Gemini 3.6 Flash",
    "TOKEN COUNT NOTE",
    "KEY CONCEPT · INFERENCE AND ASSUMPTIONS",
    "KEY CONCEPT · ARTICULATE THE TARGET",
    "KEY CONCEPT · REITERATION LOOP",
    "PROMPT → BUILD → OPEN → INSPECT → REQUEST ONE CHANGE → VERIFY AGAIN",
    "18 product records",
    "country_of_origin",
    "release_date",
    "data/notebook1/products.csv",
    "tasks/notebook1/catalogue.html",
    "Always know where your output is going",
    "tasks/stage3_answers.json",
]
FORBIDDEN_SNIPPETS = [
    "it is no longer a clickable link",
    "The growing workshop reference",
    "Limits can change",
    "add one light joke",
    "FINAL REFLECTION",
    "TROUBLESHOOTING LOOP",
    "I want to reproduce the attached example",
    "zai-org/GLM-5.2",
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


def validate_catalogue_data() -> None:
    with CATALOGUE_CSV.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    expected_fields = {
        "id",
        "name",
        "image",
        "price",
        "brand",
        "type",
        "colour",
        "release_date",
        "sizes",
        "country_of_origin",
        "designer",
    }
    if set(reader.fieldnames or []) != expected_fields:
        raise SystemExit("Catalogue CSV fields do not match the task brief")
    if len(rows) != 18:
        raise SystemExit(f"Catalogue must contain 18 products; found {len(rows)}")

    images = [row["image"] for row in rows]
    if len(set(images)) != len(images):
        raise SystemExit("Every catalogue row must map to a different image")
    missing = [name for name in images if not (CATALOGUE_DATA / name).is_file()]
    if missing:
        raise SystemExit(f"Missing catalogue images: {', '.join(missing)}")

    type_counts = Counter(row["type"] for row in rows)
    if set(type_counts.values()) != {3} or len(type_counts) != 6:
        raise SystemExit("Catalogue must contain three variants of six product types")
    for row in rows:
        date.fromisoformat(row["release_date"])
        for field in ("colour", "sizes", "country_of_origin", "designer"):
            if not row[field].strip():
                raise SystemExit(f"Catalogue field {field!r} cannot be blank")


def validate_castle_reference(markdown: str) -> None:
    match = re.search(
        r"Reveal one valid logic map.*?<pre[^>]*>(.*?)</pre>",
        markdown,
        re.DOTALL,
    )
    if not match:
        raise SystemExit("Missing hidden castle reference grid")
    rows = match.group(1).strip().splitlines()
    if len(rows) != 12 or any(len(row) != 12 for row in rows):
        raise SystemExit("Castle reference must be exactly 12 by 12")

    expected = {
        (0, 5): "G",
        (11, 6): "G",
        (1, 1): "C",
        (1, 10): "C",
        (10, 1): "C",
        (10, 10): "C",
        (2, 2): "T",
        (4, 4): "T",
        (6, 6): "T",
        (8, 8): "T",
        (2, 9): "K",
        (4, 7): "K",
        (6, 5): "K",
        (8, 3): "K",
    }
    expected.update(
        {(9, column): letter for column, letter in zip((1, 3, 5, 7, 9), "CROWN")}
    )
    wrong = [
        f"{position}={rows[position[0]][position[1]]!r}"
        for position, symbol in expected.items()
        if rows[position[0]][position[1]] != symbol
    ]
    if wrong:
        raise SystemExit(f"Castle reference violates fixed positions: {', '.join(wrong)}")
    border = rows[0] + rows[-1] + "".join(row[0] + row[-1] for row in rows[1:-1])
    if border.count("W") != 42 or border.count("G") != 2:
        raise SystemExit("Castle reference border must contain 42 walls and two gates")


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

    all_sources = "\n".join(cell.source for cell in notebook.cells)
    forbidden = [text for text in FORBIDDEN_SNIPPETS if text in all_sources]
    if forbidden:
        raise SystemExit(f"Removed workshop text returned: {', '.join(forbidden)}")

    if not EFFORT_REPORT.is_file():
        raise SystemExit(
            f"Missing student reference: {EFFORT_REPORT.relative_to(ROOT)}"
        )

    if "<abbr title='Probabilistic" not in markdown:
        raise SystemExit("Probabilistic definition must use a hover-only abbreviation")

    thumbnails = re.findall(
        r"src='../data/notebook1/([^']+\.png)'",
        markdown,
    )
    if len(thumbnails) != 18 or len(set(thumbnails)) != 18:
        raise SystemExit("Notebook must preview all 18 catalogue images once")
    if markdown.count("width:64px;height:64px") != 18:
        raise SystemExit("Catalogue preview thumbnails must remain compact")

    validate_catalogue_data()
    validate_castle_reference(markdown)

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
    if not any(
        "document.execCommand" in text and "navigator.clipboard.writeText" in text
        for text in searchable
    ):
        raise SystemExit("Notebook is missing the direct browser clipboard control")
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
