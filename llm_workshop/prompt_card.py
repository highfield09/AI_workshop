"""Selectable prompt cards with a browser-copy button for notebook learners."""

from __future__ import annotations

import json
from textwrap import dedent

import ipywidgets as widgets
from IPython.display import Javascript, display


def copyable_prompt(prompt: str, *, title: str = "Copy this prompt"):
    """Return a readable prompt box with a clipboard button and fallback."""

    prompt = dedent(prompt).strip()
    line_count = prompt.count("\n") + 1
    prompt_height = max(115, min(330, 24 * line_count + 34))
    heading = widgets.HTML(
        "<div style='background:#FFFAEB;border:1px solid #FEDF89;"
        "border-radius:10px 10px 0 0;padding:10px 12px;color:#B54708'>"
        f"<b>📋 {title}</b>"
        "</div>"
    )
    text = widgets.Textarea(
        value=prompt,
        description="",
        layout=widgets.Layout(
            width="100%",
            height=f"{prompt_height}px",
            border="1px solid #D0D5DD",
        ),
    )
    copy = widgets.Button(
        description="Copy prompt",
        icon="copy",
        button_style="primary",
        tooltip="Copy this prompt to your browser clipboard",
    )
    status = widgets.HTML(
        "<small>You can also click in the box and press Ctrl+A, then Ctrl+C.</small>"
    )
    javascript_output = widgets.Output(
        layout=widgets.Layout(height="0", overflow="hidden")
    )

    def copy_prompt(_button) -> None:
        # Use the browser clipboard, not the remote Codespace clipboard.
        safe_prompt = json.dumps(text.value).replace("</", "<\\/")
        with javascript_output:
            javascript_output.clear_output(wait=True)
            display(Javascript(f"navigator.clipboard.writeText({safe_prompt});"))
        copy.button_style = "success"
        copy.description = "Copy requested"
        status.value = (
            "<small style='color:#067647'><b>Copy requested.</b> Paste it into "
            "the AI chat. If your browser blocks clipboard access, use "
            "Ctrl+A and Ctrl+C inside the box.</small>"
        )

    copy.on_click(copy_prompt)
    controls = widgets.HBox(
        [copy, status],
        layout=widgets.Layout(
            align_items="center",
            flex_flow="row wrap",
        ),
    )
    return widgets.VBox(
        [heading, text, controls, javascript_output],
        layout=widgets.Layout(
            border="1px solid #FEDF89",
            padding="0 0 12px 0",
            width="100%",
        ),
    )
