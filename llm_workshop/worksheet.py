"""Friendly, persistent answer boxes used by the learner notebook."""

from __future__ import annotations

import json
from pathlib import Path

import ipywidgets as widgets


DEFAULT_ANSWERS_PATH = Path("tasks") / "stage3_answers.json"


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
    answer_label: str = "Paste the AI answer:",
    observation_label: str = "What did you notice?",
    answers_path: str | Path = DEFAULT_ANSWERS_PATH,
):
    """Return two text areas and a button that saves work locally."""

    path = Path(answers_path)
    saved = _read_answers(path).get(question_id, {})
    answer = _field(
        answer_label,
        saved.get("answer", ""),
        height="110px",
    )
    observation = _field(
        observation_label,
        saved.get("observation", ""),
        height="90px",
    )
    save = widgets.Button(
        description="Submit & save",
        button_style="primary",
        icon="save",
    )
    status = widgets.HTML(_initial_status(path))
    box = widgets.VBox([answer, observation, save, status], layout=_worksheet_layout())

    def on_save(_button) -> None:
        answers = _read_answers(path)
        answers[question_id] = {
            "answer": answer.children[1].value.strip(),
            "observation": observation.children[1].value.strip(),
        }
        _write_answers(path, answers)
        save.button_style = "success"
        save.description = "Saved"
        box.layout.border = "2px solid #12B76A"
        status.value = _saved_status(path)

    save.on_click(on_save)
    return box


def model_comparison_box(
    question_id: str,
    *,
    observation_label: str = "What difference did you notice?",
    model_a_heading: str = "First model",
    model_a_placeholder: str = "Copy the first model name from HuggingChat",
    model_b_heading: str = "Second model",
    model_b_placeholder: str = "Copy the second model name from HuggingChat",
    answers_path: str | Path = DEFAULT_ANSWERS_PATH,
):
    """Return side-by-side fields for comparing two model responses."""

    path = Path(answers_path)
    saved = _read_answers(path).get(question_id, {})
    model_a = widgets.Text(
        value=saved.get("model_a", ""),
        description="Model A:",
        placeholder=model_a_placeholder,
        style={"description_width": "80px"},
        layout=widgets.Layout(width="100%", max_width="100%", min_width="0"),
    )
    answer_a = _field(
        "Paste Answer A:",
        saved.get("answer_a", ""),
        height="110px",
    )
    model_b = widgets.Text(
        value=saved.get("model_b", ""),
        description="Model B:",
        placeholder=model_b_placeholder,
        style={"description_width": "80px"},
        layout=widgets.Layout(width="100%", max_width="100%", min_width="0"),
    )
    answer_b = _field(
        "Paste Answer B:",
        saved.get("answer_b", ""),
        height="110px",
    )
    observation = _field(
        observation_label,
        saved.get("observation", ""),
        height="90px",
    )
    save = widgets.Button(
        description="Submit & save",
        button_style="primary",
        icon="save",
    )
    status = widgets.HTML(_initial_status(path))
    box = widgets.VBox(
        [
            widgets.HTML(f"<b>{model_a_heading}</b>"),
            model_a,
            answer_a,
            widgets.HTML(f"<b>{model_b_heading}</b>"),
            model_b,
            answer_b,
            observation,
            save,
            status,
        ],
        layout=_worksheet_layout(),
    )

    def on_save(_button) -> None:
        answers = _read_answers(path)
        answers[question_id] = {
            "model_a": model_a.value.strip(),
            "answer_a": answer_a.children[1].value.strip(),
            "model_b": model_b.value.strip(),
            "answer_b": answer_b.children[1].value.strip(),
            "observation": observation.children[1].value.strip(),
        }
        _write_answers(path, answers)
        save.button_style = "success"
        save.description = "Saved"
        box.layout.border = "2px solid #12B76A"
        status.value = _saved_status(path)

    save.on_click(on_save)
    return box


def effort_comparison_box(
    question_id: str,
    *,
    model_name: str,
    answers_path: str | Path = DEFAULT_ANSWERS_PATH,
):
    """Compare two effort settings while recording provider token counts."""

    path = Path(answers_path)
    saved = _read_answers(path).get(question_id, {})
    low_saved = saved.get("low", {})
    high_saved = saved.get("high", {})
    if not isinstance(low_saved, dict):
        low_saved = {}
    if not isinstance(high_saved, dict):
        high_saved = {}

    def token_field(description: str, value: str):
        return widgets.Text(
            value=str(value),
            description=description,
            placeholder="Number or Not shown",
            style={"description_width": "105px"},
            layout=widgets.Layout(
                flex="1 1 250px",
                width="auto",
                max_width="100%",
                min_width="0",
            ),
        )

    low_answer = _field(
        "Paste the Low-effort answer:",
        low_saved.get("answer", ""),
        height="180px",
    )
    low_input = token_field("Input tokens:", low_saved.get("input_tokens", ""))
    low_output = token_field("Output tokens:", low_saved.get("output_tokens", ""))
    high_answer = _field(
        "Paste the High-effort answer:",
        high_saved.get("answer", ""),
        height="180px",
    )
    high_input = token_field("Input tokens:", high_saved.get("input_tokens", ""))
    high_output = token_field("Output tokens:", high_saved.get("output_tokens", ""))
    observation = _field(
        "Which answer obeyed more rules? Was the extra effort worth the time or tokens?",
        saved.get("observation", ""),
        height="100px",
    )
    count_layout = widgets.Layout(
        display="flex",
        flex_flow="row wrap",
        width="100%",
        max_width="100%",
        min_width="0",
    )
    low_counts = widgets.HBox([low_input, low_output], layout=count_layout)
    high_counts = widgets.HBox([high_input, high_output], layout=count_layout)
    save = widgets.Button(
        description="Submit & save",
        button_style="primary",
        icon="save",
    )
    status = widgets.HTML(_initial_status(path))
    box = widgets.VBox(
        [
            widgets.HTML(f"<b>{model_name} · Low effort</b>"),
            low_answer,
            low_counts,
            widgets.HTML(f"<b>{model_name} · High effort</b>"),
            high_answer,
            high_counts,
            observation,
            save,
            status,
        ],
        layout=_worksheet_layout(),
    )

    def on_save(_button) -> None:
        answers = _read_answers(path)
        answers[question_id] = {
            "model": model_name,
            "low": {
                "effort": "Low",
                "answer": low_answer.children[1].value.strip(),
                "input_tokens": low_input.value.strip(),
                "output_tokens": low_output.value.strip(),
            },
            "high": {
                "effort": "High",
                "answer": high_answer.children[1].value.strip(),
                "input_tokens": high_input.value.strip(),
                "output_tokens": high_output.value.strip(),
            },
            "observation": observation.children[1].value.strip(),
        }
        _write_answers(path, answers)
        save.button_style = "success"
        save.description = "Saved"
        box.layout.border = "2px solid #12B76A"
        status.value = _saved_status(path)

    save.on_click(on_save)
    return box
