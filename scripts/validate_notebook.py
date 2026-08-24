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
EXPECTED_MISSING_IMAGE = "ice-harbour-jacket.png"
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
    "KEY CONCEPT · INFERENCE AND ASSUMPTIONS",
    "KEY CONCEPT · ARTICULATE THE TARGET",
    "KEY CONCEPT · REITERATION LOOP",
    "PROMPT → BUILD → OPEN → INSPECT → REQUEST ONE CHANGE → VERIFY AGAIN",
    "CONTROLLED MESSY DATA",
    "18 product records",
    "**CSV** means comma-separated values",
    "**HTML** is the file type",
    "Ctrl</kbd> + <kbd>Alt</kbd>",
    "Chat: Open Chat",
    "appropriate fallback message or icon",
    "country_of_origin",
    "release_date",
    "data/notebook1/products.csv",
    "outputs/notebook1/catalogue.html",
    "### Round 1 requirements",
    "ONE-TIME SETUP · INSTALL LIVE SERVER",
    "Open with Live Server",
    "QUESTION S2-Q1",
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
    "| Part | What it means in this task |",
    "display only the five core card details at first",
    "show three columns on a laptop",
    "Do the cards remain even when product names have different lengths?",
    "Does resizing produce three, then two, then one column",
    "Medieval Castle Logic Map",
    "castle_effort",
    "Use this quick comparison checklist",
    "effort_comparison_box(",
    "model_comparison_box(",
    "catalogue_reiteration",
    "use the stated 20-question HuggingChat allowance deliberately",
    "Where your submitted work goes",
    "from llm_workshop.worksheet import (",
    "Show Preview",
    "VS Code Live Preview",
    "tasks/notebook1/catalogue.html",
    "answer_label=",
    "observation_label=",
]
EXPECTED_QUESTION_LABELS = [
    "QUESTION S1-Q1",
    "QUESTION S2-Q1",
    "QUESTION S3-E1-Q1",
    "QUESTION S3-E1-Q2",
    "QUESTION S3-E2-Q1",
    "QUESTION S3-E2-Q2",
    "QUESTION S3-E2-Q3",
    "QUESTION S3-E3-Q1",
    "QUESTION S3-E3-Q2",
    "QUESTION S3-E3-Q3",
    "QUESTION S3-E3-Q4",
    "QUESTION S3-E3-Q5",
    "QUESTION MAIN-Q1",
    "QUESTION MAIN-Q2",
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

    ids = [row["id"] for row in rows]
    expected_ids = {f"NB{number:03d}" for number in range(1, 19)}
    if set(ids) != expected_ids:
        raise SystemExit("Catalogue IDs must contain NB001 through NB018 once each")
    if ids == sorted(ids):
        raise SystemExit("Catalogue IDs must remain deliberately out of order")

    images = [row["image"] for row in rows]
    if len(set(images)) != len(images):
        raise SystemExit("Every catalogue row must map to a different image")
    missing = [name for name in images if not (CATALOGUE_DATA / name).is_file()]
    if missing != [EXPECTED_MISSING_IMAGE]:
        raise SystemExit(
            "Catalogue must contain exactly one controlled missing image: "
            f"{EXPECTED_MISSING_IMAGE}"
        )
    if not (CATALOGUE_DATA / "ice-jacket.png").is_file():
        raise SystemExit("The original Ice Harbour Jacket asset must remain available")

    type_counts = Counter(row["type"] for row in rows)
    if set(type_counts.values()) != {3} or len(type_counts) != 6:
        raise SystemExit("Catalogue must contain three variants of six product types")
    for row in rows:
        date.fromisoformat(row["release_date"])
        for field in ("colour", "sizes", "country_of_origin", "designer"):
            if not row[field].strip():
                raise SystemExit(f"Catalogue field {field!r} cannot be blank")


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

    if markdown.index("EXPERIMENT 1") > markdown.index(
        "Read the icons at the end of each model option"
    ):
        raise SystemExit("Experiment 1 must appear before the HuggingChat icon guide")
    if "KEY TIP" in markdown:
        raise SystemExit("Post-question Key Tips must not be visible in markdown cells")

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

    setup_cells = [
        (index, cell)
        for index, cell in enumerate(notebook.cells)
        if "setup" in cell.get("metadata", {}).get("tags", [])
    ]
    if len(setup_cells) != 1:
        raise SystemExit(f"Notebook must contain one setup cell; found {setup_cells}")
    setup_index, setup_cell = setup_cells[0]
    setup_imports = [
        "import random",
        "from pathlib import Path",
        "from IPython.display import HTML, display",
        "from llm_workshop.prompt_card import copyable_prompt",
        "from llm_workshop.quiz import stage1_quiz",
        "from llm_workshop.worksheet import worksheet_box",
    ]
    missing_imports = [
        statement for statement in setup_imports if statement not in setup_cell.source
    ]
    if missing_imports:
        raise SystemExit(f"Setup cell is missing imports: {missing_imports}")
    setup_metadata = setup_cell.get("metadata", {})
    if (
        setup_cell.get("execution_count") is None
        or not setup_metadata.get("inputCollapsed")
        or not setup_metadata.get("jupyter", {}).get("source_hidden")
    ):
        raise SystemExit(f"Setup cell {setup_index} must be pre-executed and hidden")

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

    worksheet_cells = [
        (index, cell)
        for index, cell in enumerate(notebook.cells)
        if cell.cell_type == "code" and "worksheet_box(" in cell.source
    ]
    if len(worksheet_cells) != 12:
        raise SystemExit(
            "Notebook must contain twelve independently saved worksheet questions; "
            f"found {[index for index, _ in worksheet_cells]}"
        )
    for index, cell in worksheet_cells:
        metadata = cell.get("metadata", {})
        if cell.get("execution_count") is None:
            raise SystemExit(f"Worksheet cell {index} must be pre-executed")
        if (
            not metadata.get("inputCollapsed")
            or not metadata.get("jupyter", {}).get("source_hidden")
            or "hide-input" not in metadata.get("tags", [])
        ):
            raise SystemExit(f"Worksheet cell {index} must start with hidden input")
        if not any(
            "application/vnd.jupyter.widget-view+json"
            in output.get("data", {})
            for output in cell.get("outputs", [])
        ):
            raise SystemExit(f"Worksheet cell {index} is missing its widget output")

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
    combined_searchable = "\n".join(searchable)
    missing_labels = [
        label for label in EXPECTED_QUESTION_LABELS
        if label not in combined_searchable
    ]
    if missing_labels:
        raise SystemExit(f"Notebook questions are missing labels: {missing_labels}")

    tip_cells = [
        index
        for index, cell in enumerate(notebook.cells)
        if cell.cell_type == "code"
        if "KEY TIP" in cell.source and "reveal_html=" in cell.source
    ]
    if len(tip_cells) != 1:
        raise SystemExit(
            "Notebook must contain one Key Tip revealed by worksheet submission; "
            f"found {tip_cells}"
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
