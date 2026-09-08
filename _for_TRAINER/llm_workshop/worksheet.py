"""Friendly, persistent answer boxes used by the learner notebook."""

from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import ipywidgets as widgets

from llm_workshop.course import answer_label
from llm_workshop.presentation import readable_html


DEFAULT_ANSWERS_PATH = Path("tasks") / "workbook_answers.json"


def _read_answers(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise ValueError("The answer file could not be read. Your existing work has not been changed.") from exc
    if not isinstance(value, dict):
        raise ValueError("The answer file must contain a JSON object. Your existing work has not been changed.")
    return value


def _write_answers(path: Path, answers: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                prefix=".answers-", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(json.dumps(answers, ensure_ascii=False, indent=2) + "\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _field(label: str, value: str, *, height: str):
    """Return a full-width label above a text area without truncation."""

    return widgets.VBox(
        [
            widgets.HTML(
                "<div style='font-weight:600;color:#344054;background:#FFFFFF;margin:6px 0 4px;"
                "max-width:100%;overflow-wrap:anywhere'>"
                f"{label}</div>"
            ),
            widgets.Textarea(
                value=value,
                description="",
                style={"text_color": "#1D2939", "background": "#FFFFFF"},
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
    return readable_html(
        "<div style='background:#EFF8FF;border:1px solid #B2DDFF;"
        "border-radius:8px;padding:9px;color:#344054'>"
        "<small>Submitting runs the save instructions in "
        "<b>_for_TRAINER/llm_workshop/worksheet.py</b>. Output path: "
        f"<code style='white-space:normal;overflow-wrap:anywhere'>"
        f"{answer_label(path)}</code>.</small></div>"
    )


def _saved_status(path: Path) -> str:
    return readable_html(
        "<div style='background:#ECFDF3;border:1px solid #ABEFC6;"
        "border-radius:8px;padding:9px;color:#067647'>"
        "<b>Saved.</b> In the VS Code Explorer, open "
        f"<code style='white-space:normal;overflow-wrap:anywhere'>"
        f"{answer_label(path)}</code> to see the output. "
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
    load_error = None
    try:
        saved = _read_answers(path).get(question_id, {})
    except ValueError as exc:
        saved = {}
        load_error = str(exc)
    if not isinstance(saved, dict):
        saved = {}
    response = _field(
        response_label,
        saved.get("response", saved.get("answer", "")),
        height=response_height,
    )
    question = widgets.HTML(readable_html(
        "<div style='background:#EFF8FF;border:1px solid #B2DDFF;"
        "border-radius:9px;padding:10px;color:#175CD3;font-weight:700;"
        "letter-spacing:0.02em;overflow-wrap:anywhere'>"
        f"{question_label}</div>"
    ))
    save = widgets.Button(
        description="Submit & save",
        button_style="primary",
        icon="save",
        style={"button_color": "#175CD3", "text_color": "#FFFFFF"},
    )
    status = widgets.HTML(_initial_status(path))
    if load_error:
        status.value = readable_html(f"<b>Not loaded.</b> {load_error} Open {answer_label(path)} to check it.")
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
    box.add_class("workshop-widget")

    def on_save(_button) -> None:
        try:
            answers = _read_answers(path)
            answers[question_id] = {
                "question": question_label,
                "response": response.children[1].value.strip(),
            }
            _write_answers(path, answers)
        except (ValueError, OSError):
            save.description = "Retry save"
            save.button_style = "danger"
            box.layout.border = "2px solid #B42318"
            status.value = readable_html(
                "<b>Not saved.</b> Check the JSON format and file permissions in "
                f"<code>{answer_label(path)}</code>, then retry. "
                "Keep your answer in this box while you check the file."
            )
            return
        save.button_style = "success"
        save.description = "Saved"
        box.layout.border = "2px solid #12B76A"
        status.value = _saved_status(path)
        if reveal_html:
            reveal.value = readable_html(reveal_html)
            reveal.layout.display = "block"

    save.on_click(on_save)
    return box
