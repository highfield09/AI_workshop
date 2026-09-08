"""Selectable prompt cards with a browser-native copy button."""

from __future__ import annotations

from html import escape
from textwrap import dedent
from uuid import uuid4

from IPython.display import HTML


def copyable_prompt(prompt: str, *, title: str = "Copy this prompt"):
    """Return a prompt card whose copy action stays inside the browser click."""

    prompt = dedent(prompt).strip()
    line_count = prompt.count("\n") + 1
    prompt_height = max(115, min(360, 24 * line_count + 34))
    card_id = f"prompt-card-{uuid4().hex}"
    prompt_html = escape(prompt)
    title_html = escape(title)

    return HTML(
        f"""
<div id="{card_id}" style="border:1px solid #FEDF89;border-radius:10px;
  width:100%;max-width:100%;box-sizing:border-box;overflow:hidden">
  <div style="background:#FFFAEB;border-bottom:1px solid #FEDF89;
    padding:10px 12px;color:#B54708;box-sizing:border-box;
    max-width:100%;overflow-wrap:anywhere"><b>📋 {title_html}</b></div>
  <textarea aria-label="{title_html}" spellcheck="false" style="display:block;
    width:100%;max-width:100%;min-width:0;height:{prompt_height}px;
    padding:10px;border:0;border-bottom:1px solid #FEDF89;resize:vertical;
    box-sizing:border-box;font:13px/1.5 ui-monospace,SFMono-Regular,Consolas,
    monospace;color:#101828;background:#FFFFFF">{prompt_html}</textarea>
  <div style="display:flex;flex-wrap:wrap;align-items:center;gap:10px;
    padding:10px 12px;background:#FFFFFF">
    <button type="button" data-copy-prompt style="border:1px solid #1570EF;
      border-radius:7px;background:#1570EF;color:#FFFFFF;padding:7px 12px;
      font-weight:600;cursor:pointer">⧉ Copy prompt</button>
    <small data-copy-status style="color:#475467">Click once, then paste into the AI chat.</small>
  </div>
</div>
<script>
(() => {{
  const root = document.getElementById("{card_id}");
  if (!root || root.dataset.copyReady === "true") return;
  root.dataset.copyReady = "true";
  const button = root.querySelector("[data-copy-prompt]");
  const area = root.querySelector("textarea");
  const status = root.querySelector("[data-copy-status]");

  button.addEventListener("click", async () => {{
    area.focus();
    area.select();
    area.setSelectionRange(0, area.value.length);
    let copied = false;

    try {{ copied = document.execCommand("copy"); }} catch (_error) {{}}
    if (!copied && navigator.clipboard && window.isSecureContext) {{
      try {{
        await navigator.clipboard.writeText(area.value);
        copied = true;
      }} catch (_error) {{}}
    }}

    if (copied) {{
      button.textContent = "✓ Copied";
      button.style.background = "#067647";
      button.style.borderColor = "#067647";
      status.innerHTML = "<b style='color:#067647'>Copied.</b> Paste it into the AI chat.";
    }} else {{
      status.innerHTML = "<b>Prompt selected.</b> Press Ctrl+C (Windows/Linux) or Cmd+C (Mac).";
    }}
  }});
}})();
</script>
"""
    )
