"""Shared workbook identities and workspace-local answer destinations."""

from pathlib import Path
import os


ROOT = Path(__file__).resolve().parents[1]
WORKBOOKS = (
    ("01_start_here", "Find your way and ask clearly", (1, 4)),
    ("02_models_and_reasoning", "Compare models and check evidence", (5, 9)),
    ("03_vision_and_context", "Explore vision, context and effort", (10, 16)),
    ("04_debugging", "Run, repair and rerun", None),
    ("05_shopping_catalogue", "Build and refine a shopping catalogue", (17, 18)),
)


def answer_path(workbook: str) -> Path:
    """Never select a remote/shared store; demos use an isolated temporary root."""
    if workbook not in {item[0] for item in WORKBOOKS}:
        raise ValueError(f"Unknown workbook: {workbook}")
    demo_root = os.environ.get("WORKSHOP_DEMO_ANSWERS")
    tasks = Path(demo_root) if demo_root else ROOT / "tasks"
    return tasks / workbook / "answers.json"


def answer_label(path: Path) -> str:
    """Show portable Explorer paths, not instructor or temporary home paths."""
    if path.name == "answers.json" and path.parent.name in {x[0] for x in WORKBOOKS}:
        return f"tasks/{path.parent.name}/answers.json"
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()
