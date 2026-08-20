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
    answer = widgets.Textarea(
        value=saved.get("answer", ""),
        description=answer_label,
        style={"description_width": "150px"},
        layout=widgets.Layout(width="100%", height="110px"),
    )
    observation = widgets.Textarea(
        value=saved.get("observation", ""),
        description=observation_label,
        style={"description_width": "150px"},
        layout=widgets.Layout(width="100%", height="90px"),
    )
    save = widgets.Button(description="Save answer", button_style="primary")
    status = widgets.HTML("<small>Your work is stored only in this Codespace.</small>")

    def on_save(_button) -> None:
        answers = _read_answers(path)
        answers[question_id] = {
            "answer": answer.value.strip(),
            "observation": observation.value.strip(),
        }
        _write_answers(path, answers)
        save.button_style = "success"
        status.value = (
            f"<b style='color:#18794e'>Saved.</b> "
            f"<small>Your worksheet is in {path.as_posix()}.</small>"
        )

    save.on_click(on_save)
    return widgets.VBox([answer, observation, save, status])


def model_comparison_box(
    question_id: str,
    *,
    observation_label: str = "What difference did you notice?",
    answers_path: str | Path = DEFAULT_ANSWERS_PATH,
):
    """Return side-by-side fields for comparing two model responses."""

    path = Path(answers_path)
    saved = _read_answers(path).get(question_id, {})
    model_a = widgets.Text(
        value=saved.get("model_a", ""),
        description="Model A:",
        placeholder="Copy the model name from HuggingChat",
        style={"description_width": "80px"},
        layout=widgets.Layout(width="100%"),
    )
    answer_a = widgets.Textarea(
        value=saved.get("answer_a", ""),
        description="Answer A:",
        style={"description_width": "80px"},
        layout=widgets.Layout(width="100%", height="110px"),
    )
    model_b = widgets.Text(
        value=saved.get("model_b", ""),
        description="Model B:",
        placeholder="Choose a different available model",
        style={"description_width": "80px"},
        layout=widgets.Layout(width="100%"),
    )
    answer_b = widgets.Textarea(
        value=saved.get("answer_b", ""),
        description="Answer B:",
        style={"description_width": "80px"},
        layout=widgets.Layout(width="100%", height="110px"),
    )
    observation = widgets.Textarea(
        value=saved.get("observation", ""),
        description=observation_label,
        style={"description_width": "170px"},
        layout=widgets.Layout(width="100%", height="90px"),
    )
    save = widgets.Button(description="Save comparison", button_style="primary")
    status = widgets.HTML("<small>Your work is stored only in this Codespace.</small>")

    def on_save(_button) -> None:
        answers = _read_answers(path)
        answers[question_id] = {
            "model_a": model_a.value.strip(),
            "answer_a": answer_a.value.strip(),
            "model_b": model_b.value.strip(),
            "answer_b": answer_b.value.strip(),
            "observation": observation.value.strip(),
        }
        _write_answers(path, answers)
        save.button_style = "success"
        status.value = (
            f"<b style='color:#18794e'>Saved.</b> "
            f"<small>Your worksheet is in {path.as_posix()}.</small>"
        )

    save.on_click(on_save)
    return widgets.VBox([
        widgets.HTML("<b>First model</b>"),
        model_a,
        answer_a,
        widgets.HTML("<b>Second model</b>"),
        model_b,
        answer_b,
        observation,
        save,
        status,
    ])
