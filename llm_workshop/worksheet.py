"""Friendly, persistent answer boxes used by the learner notebook."""

from __future__ import annotations

import json
from pathlib import Path

import ipywidgets as widgets


DEFAULT_ANSWERS_PATH = Path("tasks") / "workbook_answers.json"


def _read_answers(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return value if isinstance(value, dict) else {}


def _write_answers(path: Path, answers: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(answers, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _field(label: str, value: str, *, height: str):
    """Return a full-width label above a text area without truncation."""

    return widgets.VBox(
        [
            widgets.HTML(
                "<div style='font-weight:600;color:#344054;margin:6px 0 4px;"
                "max-width:100%;overflow-wrap:anywhere'>"
                f"{label}</div>"
            ),
            widgets.Textarea(
                value=value,
                description="",
                layout=widgets.Layout(
                    width="100%",
                    max_width="100%",
                    min_width="0",
                    height=height,
                ),
            ),
        ],
        layout=widgets.Layout(width="100%", max_width="100%", min_width="0"),
    )


def _initial_status(path: Path) -> str:
    return (
        "<div style='background:#EFF8FF;border:1px solid #B2DDFF;"
        "border-radius:8px;padding:9px;color:#344054'>"
        "<small>Submitting runs the save instructions in "
        "<b>llm_workshop/worksheet.py</b>. Output path: "
        f"<code style='white-space:normal;overflow-wrap:anywhere'>"
        f"{path.as_posix()}</code>.</small></div>"
    )


def _saved_status(path: Path) -> str:
    return (
        "<div style='background:#ECFDF3;border:1px solid #ABEFC6;"
        "border-radius:8px;padding:9px;color:#067647'>"
        "<b>Saved.</b> In the VS Code Explorer, open "
        f"<code style='white-space:normal;overflow-wrap:anywhere'>"
        f"{path.as_posix()}</code> to see the output. "
        "<small>The button triggered explicit file-writing instructions; "
        "it did not choose the destination automatically.</small></div>"
    )


def _worksheet_layout() -> widgets.Layout:
    return widgets.Layout(
        border="2px solid #B2DDFF",
        padding="14px",
        width="100%",
        max_width="100%",
        min_width="0",
        overflow="hidden",
    )


def worksheet_box(
    question_id: str,
    *,
    question_label: str,
    response_label: str = "Your response:",
    response_height: str = "120px",
    reveal_html: str | None = None,
    answers_path: str | Path = DEFAULT_ANSWERS_PATH,
):
    """Return one labelled response field with its own save action."""

    path = Path(answers_path)
    saved = _read_answers(path).get(question_id, {})
    if not isinstance(saved, dict):
        saved = {}
    response = _field(
        response_label,
        saved.get("response", saved.get("answer", "")),
        height=response_height,
    )
    question = widgets.HTML(
        "<div style='background:#EFF8FF;border:1px solid #B2DDFF;"
        "border-radius:9px;padding:10px;color:#175CD3;font-weight:700;"
        "letter-spacing:0.02em;overflow-wrap:anywhere'>"
        f"{question_label}</div>"
    )
    save = widgets.Button(
        description="Submit & save",
        button_style="primary",
        icon="save",
    )
    status = widgets.HTML(_initial_status(path))
    reveal = widgets.HTML(
        value="",
        layout=widgets.Layout(
            display="none",
            width="100%",
            max_width="100%",
            min_width="0",
        ),
    )
    box = widgets.VBox(
        [question, response, save, status, reveal],
        layout=_worksheet_layout(),
    )

    def on_save(_button) -> None:
        answers = _read_answers(path)
        answers[question_id] = {
            "question": question_label,
            "response": response.children[1].value.strip(),
        }
        _write_answers(path, answers)
        save.button_style = "success"
        save.description = "Saved"
        box.layout.border = "2px solid #12B76A"
        status.value = _saved_status(path)
        if reveal_html:
            reveal.value = reveal_html
            reveal.layout.display = "block"

    save.on_click(on_save)
    return box
