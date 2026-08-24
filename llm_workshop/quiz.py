"""Interactive, friendly quiz widgets for the learner notebook."""

from __future__ import annotations

import ipywidgets as widgets


COLORS = {
    "info": {"background": "#EFF8FF", "border": "#B2DDFF", "text": "#175CD3"},
    "warning": {"background": "#FFFAEB", "border": "#FEDF89", "text": "#B54708"},
    "success": {"background": "#ECFDF3", "border": "#ABEFC6", "text": "#067647"},
    "error": {"background": "#FEF3F2", "border": "#FECDCA", "text": "#B42318"},
}


def _message(content: str, tone: str) -> str:
    colors = COLORS[tone]
    return (
        f"<div style='background:{colors['background']};"
        f"border:1px solid {colors['border']};border-radius:10px;"
        f"padding:12px;color:#344054'>{content}</div>"
    )


def _question(tone: str) -> str:
    return _message(
        "<div style='font-size:0.78rem;letter-spacing:0.04em;margin-bottom:6px'>"
        "<b>QUESTION 1 · READ THE WELCOME PAGE</b></div>"
        "<b>According to <code>README.md</code>, what is this workshop mainly "
        "asking you to practise?</b><br><small>Hint: the answer is somewhere "
        "inside the README file at the root of the directory tree.</small>",
        tone,
    )


def readme_quiz():
    """Return an MCQ whose visual state changes after submission."""

    question = widgets.HTML(_question("info"))
    choices = widgets.RadioButtons(
        options=[
            ("Memorising Python syntax before making anything", "syntax"),
            (
                "Finding files, describing a target, making and opening a result, then refining it",
                "workflow",
            ),
            ("Putting every workshop file into one folder", "one-folder"),
        ],
        value=None,
    )
    submit = widgets.Button(
        description="Submit answer",
        button_style="primary",
        icon="check",
    )
    feedback = widgets.HTML(
        _message("<small>Choose one answer, then submit it.</small>", "info")
    )
    panel = widgets.VBox(
        [question, choices, submit, feedback],
        layout=widgets.Layout(
            border="2px solid #B2DDFF",
            padding="14px",
            width="100%",
            max_width="100%",
            min_width="0",
            overflow="hidden",
        ),
    )

    def check_answer(_button) -> None:
        if choices.value == "workflow":
            question.value = _question("success")
            feedback.value = _message(
                "<div style='font-size:1.05rem'>🎉 <b>Correct!</b> "
                "The workshop is about a clear make–inspect–refine workflow, "
                "not memorising syntax.</div>"
                "<div style='margin-top:10px;padding-top:10px;"
                "border-top:1px solid #ABEFC6'><b>KEY TIP · READ THE README "
                "FIRST</b><br><small>A README is the project's welcome page. "
                "Check it before starting: it explains the purpose, setup, "
                "folder map, and first actions.</small></div>"
                "<div style='margin-top:10px;padding-top:10px;"
                "border-top:1px solid #ABEFC6'>"
                "<code>widgets.RadioButtons(...) + widgets.Button(...)</code><br>"
                "<small>This simple MCQ, answer check, and submit button come "
                "directly from the <b>ipywidgets</b> package—cool, right?</small>"
                "</div>",
                "success",
            )
            panel.layout.border = "2px solid #12B76A"
            submit.description = "Correct"
            submit.button_style = "success"
            submit.icon = "check"
        elif choices.value is None:
            question.value = _question("warning")
            feedback.value = _message(
                "<b>Choose an answer first.</b>", "warning"
            )
            panel.layout.border = "2px solid #F79009"
            submit.description = "Submit answer"
            submit.button_style = "warning"
            submit.icon = ""
        else:
            question.value = _question("error")
            feedback.value = _message(
                "<b>Not quite.</b> Open <code>README.md</code> in the Explorer, "
                "read the opening paragraph, and try again.",
                "error",
            )
            panel.layout.border = "2px solid #F04438"
            submit.description = "Try again"
            submit.button_style = "danger"
            submit.icon = "refresh"

    submit.on_click(check_answer)
    return panel
