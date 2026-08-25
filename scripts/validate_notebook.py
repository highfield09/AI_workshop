"""Validate notebook structure, outputs, and basic secret hygiene."""

from __future__ import annotations

import csv
import re
from collections import Counter
from datetime import date
from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
NOTEBOOK = ROOT / "notebooks" / "01_start_here.ipynb"
EFFORT_REPORT = ROOT / "Resources" / "2026 Agentic Coding Trends Report.pdf"
CATALOGUE_DATA = ROOT / "data" / "notebook1"
CATALOGUE_CSV = CATALOGUE_DATA / "products.csv"
VISION_IMAGE = CATALOGUE_DATA / "Screenshot 2026-02-23 145127.png"
EXPECTED_MISSING_IMAGE = "ice-harbour-jacket.png"
EXPECTED_MESSY_ID_ORDER = [
    "NB014",
    "NB006",
    "NB015",
    "NB018",
    "NB002",
    "NB005",
    "NB003",
    "NB011",
    "NB008",
    "NB007",
    "NB016",
    "NB013",
    "NB017",
    "NB001",
    "NB004",
    "NB012",
    "NB009",
    "NB010",
]
EXPECTED_MERGED_ROW_ID = "NB012"
REQUIRED_HEADINGS = [
    "## Find your way around",
    "## Choose an AI helper and prompt deliberately",
    "## Try the AI interfaces",
    "## Main task — Build and refine a shopping catalogue",
    "## Orientation complete",
]
REQUIRED_SNIPPETS = [
    "Keep the lesson inside the available notebook width",
    "KEY CONCEPT · TOKEN EFFICIENCY",
    "KEY CONCEPT · MODEL EFFORT",
    "Effort is a <b>signal, not a strict token budget</b>",
    "20 questions",
    "PROMPTING RESOURCES AND MORE GUIDES",
    "Google AI Mode",
    "Read the icons at the end of each model option",
    "HuggingChat models: read the card and the icons",
    "ONE-TIME SETUP · CONNECT OPENROUTER",
    "google/gemma-4-26b-a4b-it",
    "OpenRouter Activity",
    "Screenshot 2026-02-23 145127.png",
    "Thinking Effort → Medium",
    "KEY CONCEPT · TRACE THE PROVIDER",
    "VISION MODELS AND OCR",
    "### Check where the vision request was charged",
    "- **Route:**",
    "START WITH A FRESH CONTEXT WINDOW",
    "same Gemini 3.5 Flash-Lite model",
    "Give me the smallest change",
    "EXPERIMENT 5",
    "moonshotai/Kimi-K3",
    "Gemini 3.5 Flash-Lite",
    "QUESTION 13 · Answer B — Gemini 3.5 Flash-Lite with extended thinking",
    "KEY CONCEPT · INFERENCE AND ASSUMPTIONS",
    "KEY CONCEPT · ARTICULATE THE TARGET",
    "KEY CONCEPT · REITERATION LOOP",
    "PROMPT → BUILD → OPEN → INSPECT → REQUEST ONE CHANGE → VERIFY AGAIN",
    "CONTROLLED MESSY DATA",
    "DATA REPAIR BEFORE REDESIGN",
    "Do not prematurely read the notebook requirements and go beyond what is requested in this prompt",
    "change the mode to **Ask** and change the model to **Auto**",
    "18 product records",
    "**CSV** means comma-separated values",
    "**HTML** is the file type",
    "Ctrl</kbd> + <kbd>Alt</kbd>",
    "Chat: Open Chat",
    "appropriate message or icon if its image is missing",
    "country_of_origin",
    "release_date",
    "data/notebook1/products.csv",
    "outputs/notebook1/catalogue.html",
    "### Round 1 requirements",
    "ONE-TIME SETUP · INSTALL LIVE SERVER",
    "Open with Live Server",
    "QUESTION 2 · Prompt-and-token mini-check",
    "Always know where your output is going",
    "tasks/workbook_answers.json",
    "OPEN THE SAVED JSON FILE",
    "CHECK REFERENCES AND CLAIMS",
    "LANGUAGE CHOICE",
    "MODEL SIZE, QUALITY AND COST",
    "OBSERVE THE VISIBLE REASONING",
    "93.5 on GPQA Diamond",
    "58.7 on SciCode",
    "QUESTION 9 · FACT-CHECK THE EC NUMBERS",
    "Knowledge retrieval and reasoning are different abilities",
    "short-term working memory",
    "Statement B is wrong",
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
    "PROVIDER / FASTEST / CHEAPEST",
    "QUESTION S1-",
    "QUESTION S2-",
    "stage3_",
    "Hugging Face pricing and billing",
    "CLASS BUDGET",
    "If classroom credit is authorised",
    "More guides linked from the resource directory",
    "Python (Vibe Workshop)",
    "Experiment 2 uses two of them",
    "Add Context → Files & Folders",
    "Gemini 3.6 Flash",
]
EXPECTED_QUESTION_LABELS = [f"QUESTION {number} ·" for number in range(1, 19)]

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
    if ids != EXPECTED_MESSY_ID_ORDER:
        raise SystemExit("Catalogue rows must remain in the deliberately mixed order")

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
    tail_fields = ("sizes", "country_of_origin", "designer")
    malformed_rows = [
        row for row in rows if any(row[field] is None for field in tail_fields)
    ]
    if [row["id"] for row in malformed_rows] != [EXPECTED_MERGED_ROW_ID]:
        raise SystemExit("Catalogue must contain one controlled merged-column row")
    merged_row = malformed_rows[0]
    if (
        len(merged_row["release_date"]) < 100
        or "separators disappeared" not in merged_row["release_date"]
    ):
        raise SystemExit("Merged row must retain its unusually long combined field")

    for row in rows:
        if row["id"] == EXPECTED_MERGED_ROW_ID:
            continue
        date.fromisoformat(row["release_date"])
        for field in ("colour", *tail_fields):
            if not row[field].strip():
                raise SystemExit(f"Catalogue field {field!r} cannot be blank")


def main() -> None:
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    nbformat.validate(notebook)
    readme = README.read_text(encoding="utf-8")
    if "## Local VS Code setup" in readme:
        raise SystemExit("README must remain focused on the Codespaces workflow")
    if "Python (Vibe Workshop)" in readme:
        raise SystemExit("README must point learners to the .venv Python kernel")
    if "Python 3.12 (.venv)" not in readme:
        raise SystemExit("README is missing the learner-facing .venv kernel example")


    markdown = "\n".join(
        cell.source for cell in notebook.cells if cell.cell_type == "markdown"
    )
    missing = [heading for heading in REQUIRED_HEADINGS if heading not in markdown]
    all_sources = "\n".join(cell.source for cell in notebook.cells)
    if missing:
        raise SystemExit(f"Missing workshop sections: {', '.join(missing)}")

    missing_snippets = [text for text in REQUIRED_SNIPPETS if text not in all_sources]
    if missing_snippets:
        raise SystemExit(
            f"Missing workshop concepts: {', '.join(missing_snippets)}"
        )

    forbidden = [text for text in FORBIDDEN_SNIPPETS if text in all_sources]
    if forbidden:
        raise SystemExit(f"Removed workshop text returned: {', '.join(forbidden)}")
    if re.search(r"\bstages?\b", all_sources, re.I):
        raise SystemExit("Notebook must use a directions flow without stage labels")

    if markdown.index("EXPERIMENT 1") > markdown.index(
        "Read the icons at the end of each model option"
    ):
        raise SystemExit("Experiment 1 must appear before the HuggingChat icon guide")
    if "KEY TIP" in markdown:
        raise SystemExit("Post-question Key Tips must not be visible in markdown cells")
    if not (
        markdown.index("EXPERIMENT 1")
        < markdown.index("HuggingChat models: read the card and the icons")
        < markdown.index("EXPERIMENT 2")
    ):
        raise SystemExit("Model-card guidance must sit with HuggingChat selection")
    if not (
        all_sources.index("### Check where the vision request was charged")
        < all_sources.index("QUESTION 11 ·")
        < all_sources.index("### Compare with GitHub-provided Copilot usage")
    ):
        raise SystemExit("OpenRouter Activity guidance must appear before Question 11")

    if not (
        all_sources.index("QUESTION 11 ·")
        < all_sources.index("### Match effort to the task")
        < all_sources.index("EXPERIMENT 4")
    ):
        raise SystemExit("Effort guidance must sit directly before the Gemini exercise")

    if not EFFORT_REPORT.is_file():
        raise SystemExit(
            f"Missing student reference: {EFFORT_REPORT.relative_to(ROOT)}"
        )
    if not VISION_IMAGE.is_file():
        raise SystemExit(
            f"Missing vision exercise image: {VISION_IMAGE.relative_to(ROOT)}"
        )

    if "<abbr title='Probabilistic" not in markdown:
        raise SystemExit("Probabilistic definition must use a hover-only abbreviation")

    thumbnails = re.findall(
        r"src='../data/notebook1/(?!Screenshot%20)([^']+\.png)'",
        markdown,
    )
    if len(thumbnails) != 18 or len(set(thumbnails)) != 18:
        raise SystemExit("Notebook must preview all 18 catalogue images once")
    if markdown.count("width:64px;height:64px") != 18:
        raise SystemExit("Catalogue preview thumbnails must remain compact")

    validate_catalogue_data()
    if markdown.count("Screenshot%202026-02-23%20145127.png") != 1:
        raise SystemExit("Vision image must appear exactly once at a compact width")

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
        "from llm_workshop.quiz import readme_quiz",
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
    if len(worksheet_cells) != 16:
        raise SystemExit(
            "Notebook must contain sixteen independently saved worksheet questions; "
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
