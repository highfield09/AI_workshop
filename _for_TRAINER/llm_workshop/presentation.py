"""Explicit, high-contrast reading surfaces in either editor theme."""


READING_CSS = """
/* Keep the lesson inside the available notebook width. */
.workshop-reading { background:#FFFFFF; color:#1D2939; color-scheme:light;
  padding:16px; border:1px solid #D0D5DD; border-radius:12px;
  line-height:1.6; box-sizing:border-box; max-width:100%; overflow-wrap:anywhere; }
.workshop-reading :is(p,li,td,th,h1,h2,h3,h4,summary,strong,b,small,em) { color:inherit; }
.workshop-reading a { color:#1849A9 !important; text-decoration:underline; }
.workshop-reading details { background:#FDF2FA !important; color:#1D2939 !important;
  border:1px solid #FCCEEE !important; border-left:5px solid #9E165F !important;
  border-radius:10px; padding:12px; margin:12px 0; }
.workshop-reading details > summary { display:list-item !important;
  list-style:disclosure-closed inside !important; cursor:pointer; color:#851651 !important; }
.workshop-reading details[open] > summary { list-style-type:disclosure-open !important; }
.workshop-reading details > summary::after { content:" — Click the arrow for more information";
  font-size:0.85em; font-weight:normal; }
.workshop-reading details > summary:focus-visible { outline:3px solid #9E165F; outline-offset:3px; }
.workshop-reading :is(code,kbd) { color:#1D2939 !important; background:#F2F4F7 !important;
  border-radius:4px; padding:1px 4px; overflow-wrap:anywhere; }
.workshop-reading table { display:block; max-width:100%; overflow-x:auto;
  color:#1D2939; background:#FFFFFF; }
.workshop-reading :is(th,td) { border-color:#D0D5DD; background:transparent; }
.workshop-reading pre { color:#1D2939; background:#F8FAFC; white-space:pre-wrap;
  max-width:100%; overflow-x:auto; box-sizing:border-box; }
.workshop-reading :is(img,svg) { max-width:100%; height:auto; }
.workshop-reading .workshop-flex { display:flex; flex-wrap:wrap; max-width:100%; }
.workshop-reading .workshop-flex > * { min-width:0; max-width:100%; box-sizing:border-box; }
.workshop-widget { background:#FFFFFF !important; color:#1D2939 !important; color-scheme:light; }
.workshop-widget :is(label,.widget-label) { color:#1D2939 !important; }
.workshop-widget textarea { background:#FFFFFF !important; color:#1D2939 !important;
  caret-color:#1D2939; border:1px solid #667085 !important; }
.workshop-widget button { background:#175CD3 !important; color:#FFFFFF !important; }
.workshop-widget button.mod-success { background:#067647 !important; }
.workshop-widget button.mod-danger { background:#B42318 !important; }
.workshop-widget button:focus-visible, .workshop-reading a:focus-visible {
  outline:3px solid #B54708; outline-offset:3px; }
"""


def readable_html(content: str) -> str:
    # Repeat scoped CSS: VS Code can render each output in a separate context.
    return (f"<style>{READING_CSS}</style>\n"
            '<div class="workshop-reading" style="background:#FFFFFF;color:#1D2939;'
            'color-scheme:light;max-width:100%;box-sizing:border-box;padding:16px;'
            'border:1px solid #D0D5DD;border-radius:12px;overflow-wrap:anywhere">\n\n'
            + content.strip() + "\n\n</div>")
