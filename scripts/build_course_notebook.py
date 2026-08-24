"""Build the learner-facing onboarding notebook from readable cell sources."""

from __future__ import annotations

import csv
from html import escape
from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "01_start_here.ipynb"
CATALOGUE_CSV = ROOT / "data" / "notebook1" / "products.csv"
PALETTES = {
    "info": {
        "background": "#EFF8FF",
        "border": "#B2DDFF",
        "accent": "#175CD3",
    },
    "task": {
        "background": "#FFFAEB",
        "border": "#FEDF89",
        "accent": "#B54708",
    },
    "keyword": {
        "background": "#F4F3FF",
        "border": "#D9D6FE",
        "accent": "#5925DC",
    },
    "success": {
        "background": "#ECFDF3",
        "border": "#ABEFC6",
        "accent": "#067647",
    },
}


def markdown(source: str):
    return nbf.v4.new_markdown_cell(source.strip())


def code(source: str, *tags: str):
    cell = nbf.v4.new_code_cell(source.strip())
    cell_tags = list(tags)
    if "worksheet_box(" in cell.source:
        cell.metadata["inputCollapsed"] = True
        cell.metadata["jupyter"] = {"source_hidden": True}
        cell_tags.append("hide-input")
    if cell_tags:
        cell.metadata["tags"] = cell_tags
    return cell


def chip(label: str, tone: str = "keyword") -> str:
    colors = PALETTES[tone]
    return (
        f"<span style='display:inline-block;background:{colors['background']};"
        f"border:1px solid {colors['border']};color:{colors['accent']};"
        "border-radius:999px;padding:2px 9px;font-size:0.76rem;"
        "font-weight:700;letter-spacing:0.04em;white-space:normal;"
        "max-width:100%;box-sizing:border-box;overflow-wrap:anywhere'>"
        f"{label}</span>"
    )


def panel(label: str, body: str, tone: str = "info") -> str:
    colors = PALETTES[tone]
    return (
        f"<div style='background:{colors['background']};"
        f"border:1px solid {colors['border']};border-left:5px solid "
        f"{colors['accent']};border-radius:12px;padding:15px 17px;"
        "margin:12px 0;color:#344054;line-height:1.55;box-sizing:border-box;"
        "max-width:100%;overflow-wrap:anywhere'>"
        f"{chip(label, tone)}"
        f"<div style='margin-top:9px'>{body}</div></div>"
    )


def model_card_diagram() -> str:
    """Return a compact, responsive guide to the three model-card signals."""

    cards = [
        (
            "1 · DESCRIPTION",
            "What the model was built to do: chat, translate, code, analyse "
            "images, or something specialised.",
        ),
        (
            "2 · PARAMETER SIZE",
            "A rough scale label such as <b>4B</b>, <b>70B</b>, or "
            "<b>2.8T</b>. B means billion; T means trillion. More is not an "
            "automatic quality guarantee.",
        ),
        (
            "3 · MULTIMODALITY",
            "Which inputs it understands. Text-only models handle language; "
            "a vision or image badge means the model can also inspect images.",
        ),
    ]
    card_html = "".join(
        "<div style='flex:1 1 210px;background:#FFFFFF;border:1px solid "
        "#D9D6FE;border-radius:10px;padding:13px;min-width:0;"
        "max-width:100%;box-sizing:border-box;overflow-wrap:anywhere'>"
        f"{chip(title)}<p style='margin:9px 0 0'>{body}</p></div>"
        for title, body in cards
    )
    return (
        "<div style='background:#F9F5FF;border:1px solid #D9D6FE;"
        "border-radius:14px;padding:16px;margin:12px 0;color:#344054;"
        "box-sizing:border-box;max-width:100%;overflow-wrap:anywhere'>"
        "<div style='font-size:1.05rem;font-weight:700;color:#5925DC'>"
        "How to read a model card</div>"
        "<div style='display:flex;flex-wrap:wrap;gap:10px;margin-top:12px'>"
        f"{card_html}</div>"
        "<div style='text-align:center;font-size:1.3rem;color:#5925DC;"
        "padding:8px 0 2px'>↓</div>"
        "<div style='background:#ECFDF3;border:1px solid #ABEFC6;"
        "border-radius:10px;padding:11px;text-align:center'>"
        "<b>Choose the smallest suitable model that accepts your input and "
        "fits the task.</b></div></div>"
    )


def catalogue_preview() -> str:
    """Return a compact CSV-ordered preview of all catalogue products."""

    with CATALOGUE_CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    cards = []
    for row in rows:
        name = escape(row["name"])
        image = escape(row["image"])
        product_type = escape(row["type"])
        colour = escape(row["colour"])
        cards.append(
            "<div style='border:1px solid #D0D5DD;border-radius:8px;"
            "padding:7px;background:#FFFFFF;min-width:0;text-align:center;"
            "box-sizing:border-box;overflow:hidden'>"
            "<div style='height:64px;background:#F2F4F7;border-radius:6px;"
            "display:grid;place-items:center;overflow:hidden'>"
            f"<img src='../data/notebook1/{image}' alt='{name}' "
            "style='display:block;width:64px;height:64px;object-fit:contain;"
            "image-rendering:pixelated'></div>"
            f"<div style='font-size:0.72rem;font-weight:700;margin-top:5px;"
            f"line-height:1.15'>{name}</div>"
            f"<div style='font-size:0.64rem;color:#667085;line-height:1.2;"
            f"margin-top:2px'>{product_type}<br>{colour}</div></div>"
        )

    return (
        "<div style='background:#F8FAFC;border:1px solid #D0D5DD;"
        "border-radius:12px;padding:10px;margin:12px 0;max-width:100%;"
        "box-sizing:border-box'>"
        "<div style='font-size:0.78rem;font-weight:700;color:#344054;"
        "margin-bottom:8px'>COMPACT INVENTORY · CSV ORDER · 18 ITEMS</div>"
        "<div style='display:grid;grid-template-columns:repeat(auto-fit,"
        "minmax(98px,1fr));gap:7px'>"
        + "".join(cards)
        + "</div></div>"
    )


def main() -> None:
    cells = [
        markdown(
            f"""
# Vibe Coding Workshop — Start Here

<style>
/* Keep the lesson inside the available notebook width on laptops. */
table {{ display:block; max-width:100%; overflow-x:auto; }}
pre {{ box-sizing:border-box; max-width:100%; overflow-x:auto; }}
code {{ overflow-wrap:anywhere; }}
img, svg {{ max-width:100%; height:auto; }}
.workshop-flex {{ display:flex; flex-wrap:wrap; max-width:100%; }}
.workshop-flex > * {{ min-width:0; max-width:100%; box-sizing:border-box; }}
</style>

**Friendly setup · 45–60 minutes · No coding experience required**

This short notebook helps you get comfortable in VS Code, find the course files, and choose an AI helper. After this orientation, you will work through six small challenges where you reproduce a visible result.

{panel(
    "IMPORTANT",
    "<b>Run each cell from top to bottom.</b> Nothing in Stages 1 or 2 "
    "sends data to an API.<br><br><b>Using GitHub Codespaces?</b> Python "
    "runs inside the online workspace, so you do not need it installed on "
    "your laptop. If prompted for a kernel, select "
    "<b>Python (Vibe Workshop)</b>.",
    "info",
)}
"""
        ),
        markdown(
            f"""
### The simple workflow

1. **Look** at the result you want to recreate.
2. **Describe** what should match.
3. **Ask** an AI helper for the smallest useful next step.
4. **Make** or change a file.
5. **Open** the result and compare it with the target.
6. **Refine** one thing at a time.

You do not need to memorize commands. The aim is to learn where things live and how to ask for a clear outcome.

{panel(
    "COLOUR KEY",
    chip("KEYWORD") + " marks a useful term. &nbsp; "
    + chip("TASK", "task") + " tells you to do something. &nbsp; "
    + chip("CHECKPOINT", "success") + " shows progress.",
    "info",
)}
"""
        ),
        markdown(
            f"""
## Stage 1 — Find your way around

### Five friendly terms

| Term | What it means here |
|---|---|
| {chip("EDITOR")} | The main VS Code area where you open and change a file. |
| {chip("SCRIPT")} | A saved list of instructions that makes the computer do a repeatable task. |
| {chip("DATA TYPE")} | The shape of information, such as text, a number, a table, JSON, or CSV. |
| {chip("TERMINAL")} | The small command area where you can ask the computer to run something. |
| {chip("DIRECTORY TREE")} | The folder-and-file map shown in the Explorer on the left. |

{panel(
    "TIP",
    "If you feel lost, return to the <b>Explorer</b> and look for the "
    "folder named in the task.",
    "info",
)}
"""
        ),
        markdown(
            f"""
{panel(
    "WORKSHOP MAP",
    "<pre style='margin:0;padding:12px;background:#FFFFFF;"
    "border:1px solid #D0D5DD;border-radius:8px;line-height:1.55;"
    "overflow:auto;max-width:100%;box-sizing:border-box'>AI_workshop/\n"
    "├── notebooks/   ← lessons like this one\n"
    "├── tasks/       ← one isolated folder for each challenge\n"
    "├── data/        ← small input files supplied by the course\n"
    "├── outputs/     ← viewers, reports, and other results you create\n"
    "├── Resources/   ← optional student reading and reports\n"
    "├── scripts/     ← reusable instructions that run a task\n"
    "├── KEY_CONCEPTS.md ← growing take-home reference\n"
    "└── README.md    ← the project welcome page</pre>"
    "<p style='margin:10px 0 0'>Keep each challenge self-contained inside "
    "its own <b>tasks/</b> folder. Put shared source files in <b>data/</b> "
    "and finished examples in <b>outputs/</b>.</p>",
    "info",
)}
"""
        ),
        markdown(
            f"""
{panel(
    "RUN A CELL",
    "<b>Click the ▶ play button</b> beside a code cell, or press "
    "<b>Shift + Enter</b>. The cell will run and place its result directly "
    "underneath.",
    "task",
)}

{panel(
    "YOU CAN IGNORE THE CODE",
    "You do not need to understand the code inside the next cell. The "
    "folder list that appears underneath—and the interactive widget later—"
    "are direct results of the instructions in their code cells.<br><br>"
    "Run the next cell to answer: <b>Where am I?</b> and "
    "<b>What files are here?</b>",
    "info",
)}
"""
        ),
        code(
            """
from pathlib import Path

workspace = Path.cwd()
print(f"Current folder: {workspace}")
print("\\nWorkshop items:")
for item in sorted(workspace.iterdir(), key=lambda path: (not path.is_dir(), path.name.lower())):
    if not item.name.startswith("."):
        kind = "folder" if item.is_dir() else "file"
        print(f"  {item.name}/" if item.is_dir() else f"  {item.name}  ({kind})")
"""
        ),
        markdown(
            f"""
{panel(
    "QUICK CHECK",
    "Choose an answer and press <b>Submit answer</b>. The question panel "
    "turns green for a correct answer and red when you should try again.",
    "task",
)}
"""
        ),
        code(
            """
from llm_workshop.quiz import stage1_quiz

stage1_quiz()
""",
            "interactive",
        ),
        markdown(
            f"""
{panel(
    "STAGE 1 CHECKPOINT",
    "<ul style='margin:0;padding-left:20px'>"
    "<li>find the <b>Explorer</b>, <b>editor</b>, and <b>terminal</b>;</li>"
    "<li>point to the <b>notebooks</b>, <b>tasks</b>, <b>data</b>, and "
    "<b>outputs</b> folders;</li>"
    "<li>explain the difference between an input file and something you "
    "created.</li></ul><p style='margin:10px 0 0'>That is enough "
    "orientation to begin vibe coding.</p>",
    "success",
)}
"""
        ),
        markdown(
            f"""
## Stage 2 — Choose an AI helper

Use any interface available to you. These links open the official web experiences in a browser:

| AI interface | Open it |
|---|---|
| {chip("CHATGPT")} | [Open ChatGPT ↗](https://chatgpt.com/) |
| {chip("CLAUDE")} | [Open Claude ↗](https://claude.ai/) |
| {chip("GEMINI")} | [Open Gemini ↗](https://gemini.google.com/) |
| {chip("HUGGINGCHAT")} | [Open HuggingChat ↗](https://huggingface.co/chat/) |
| {chip("GOOGLE AI MODE")} | [Open Google AI Mode ↗](https://www.google.com/search?udm=50) |

{panel(
    "IMPORTANT",
    "Access can depend on your account, organization, or region. It is "
    "fine if the class uses a mixture of tools.",
    "info",
)}
"""
        ),
        markdown(
            f"""
### Read the model card before choosing

An **LLM card** is the model's label and short information page. Use three signals instead of choosing by name alone:

{model_card_diagram()}

{panel(
    "PARAMETERS ARE NOT TOKENS",
    "<b>Parameters</b> are learned values inside a model; they give a rough "
    "sense of scale. <b>Tokens</b> are pieces of the text and other content "
    "processed during each request. A larger parameter count can bring more "
    "capability, but it does not guarantee the best answer for every task.",
    "info",
)}
"""
        ),
        markdown(
            f"""
### Tokens, limits, and cost

{panel(
    "KEY CONCEPT · TOKEN EFFICIENCY",
    "Every question uses tokens: your prompt, relevant chat history and "
    "attachments are <b>input tokens</b>; the answer and sometimes extra "
    "reasoning are <b>output tokens</b>. Services set different limits and "
    "prices—some count tokens, while others show messages, requests, or "
    "credits.<br><br><b>Model size does not directly change the number of "
    "input tokens in the same sentence.</b> However, larger or reasoning "
    "models may cost more per token or produce longer answers. Complex "
    "questions, large files, long chat histories, and requests for detailed "
    "output can consume more than expected.",
    "task",
)}

<div class='workshop-flex' style='gap:8px;margin:10px 0'>
<div style='flex:1 1 180px;background:#EFF8FF;border:1px solid #B2DDFF;border-radius:9px;padding:10px'><b>Ask clearly</b><br><small>State the task, audience, and output format.</small></div>
<div style='flex:1 1 180px;background:#EFF8FF;border:1px solid #B2DDFF;border-radius:9px;padding:10px'><b>Send only what is needed</b><br><small>Avoid entire folders or repeated context.</small></div>
<div style='flex:1 1 180px;background:#EFF8FF;border:1px solid #B2DDFF;border-radius:9px;padding:10px'><b>Request a useful length</b><br><small>For example: “Answer in five bullets.”</small></div>
</div>

See [Hugging Face pricing and billing](https://huggingface.co/docs/inference-providers/en/pricing) for an example of how one service handles credits and pay-as-you-go use.

### Match effort to the task

{panel(
    "KEY CONCEPT · MODEL EFFORT",
    "Some interfaces provide an <b>Effort</b> control. It signals the model "
    "to spend less or more of its response budget on reasoning and checking. "
    "More effort can help on difficult, multi-step work, but it usually takes "
    "longer and may use more output or reasoning tokens. It does not guarantee "
    "a better answer.<br><br><b>Not every model or provider exposes this "
    "control.</b> Others use a fixed or automatic reasoning level.",
    "task",
)}

| Effort level | Compute / token use | Best fit |
|---|---|---|
| **Low** | Usually the smallest response and reasoning budget | Quick factual lookups, routing, and high-volume simple work. |
| **Medium** | A balanced, moderate budget | Routine editing, summaries, and tightly scoped tasks. |
| **High (often default)** | A larger reasoning and checking budget | Complex engineering, nuanced analysis, and difficult multi-step tasks. |
| **Max / XHigh** | The largest available budget; can be much more expensive | Long agentic work, large refactors, and difficult multi-file debugging. Availability varies. |

{panel(
    "IMPORTANT",
    "Effort is a <b>signal, not a strict token budget</b>. The same setting "
    "can use different amounts on different questions, models, or providers. "
    "High or Max is not automatically the most token-efficient choice.",
    "info",
)}

Student references:

- [Claude: optimizing for cost and intelligence](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)
- [Claude effort controls — current documentation](https://platform.claude.com/docs/en/build-with-claude/effort)
- [2026 Agentic Coding Trends Report](../Resources/2026%20Agentic%20Coding%20Trends%20Report.pdf) — a broader reference on increasingly complex, long-running coding agents.

### A six-point prompt check

1. **Set the objective:** decide whether you need information, ideas, or a problem solved.
2. **Be clear and concise:** use direct language and remove vague instructions.
3. **Add useful context:** include the background needed for the task, but not unrelated material.
4. **Experiment and iterate:** improve the wording after seeing what the first answer misses.
5. **Name the audience:** say who will read or use the result.
6. **Evaluate and adapt:** check the output and adjust rather than accepting it automatically.

{panel(
    "PROMPTING RESOURCES",
    "<ul style='margin:0;padding-left:20px'>"
    "<li><a href='https://drive.google.com/file/d/1AbaBYbEa_EbPelsT40-vj64L-2IwUJHy/view'>Google Prompt Engineering guide (PDF)</a> — a longer reference; Google Drive may ask you to sign in.</li>"
    "<li><a href='https://community.openai.com/t/a-guide-to-crafting-effective-prompts-for-diverse-applications/493914'>Community forum: crafting effective prompts</a> — the source of the six-point outline above.</li>"
    "<li><a href='https://www.amalytix.com/en/blog/free-prompt-engineering-guides/'>AMALYTIX directory of free prompting guides</a> — a third-party roundup with beginner and advanced choices.</li>"
    "</ul>",
    "info",
)}

<details style='background:#F4F3FF;border:1px solid #D9D6FE;border-radius:10px;padding:12px'>
<summary><b>More guides linked from the resource directory</b></summary>

- [OpenAI GPT-4.1 Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-4-1_prompting_guide) — advanced and developer-focused.
- [Anthropic prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
- [Google Workspace with Gemini Prompt Guide](https://workspace.google.com/learning/content/gemini-prompt-guide)
- [Microsoft prompt engineering techniques](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering?tabs=chat)
- [Learn Prompting](https://learnprompting.org/docs/introduction) — a broad, interactive learning guide.
- [DAIR.AI Prompt Engineering Guide](https://www.promptingguide.ai/) — a community-maintained reference.
- [O'Reilly: Prompt Engineering for LLMs](https://www.oreilly.com/library/view/prompt-engineering-for/9781098156145/) — access may require a trial or subscription.
- [AMALYTIX Amazon Prompts Guide](https://insights.amalytix.com/amazon-prompts-2025/) — specialised for e-commerce examples.

</details>

### Your role while using AI

- {chip("YOU CHOOSE")} the target.
- {chip("AI PROPOSES")} a step.
- {chip("YOU PLACE")} files in the correct folder.
- {chip("YOU RUN")} or open the result.
- {chip("YOU COMPARE")} and decide what changes next.

{panel(
    "USEFUL PHRASE",
    "If the answer becomes too technical, say: <i>Explain that in plain "
    "language and give me only the next action.</i>",
    "info",
)}

{panel(
    "STAGE 2 KEY CONCEPT",
    "Choose a model by its <b>description</b>, <b>parameter scale</b>, and "
    "<b>supported input types</b>. Then use tokens deliberately: enough "
    "context to do the job, without unnecessary material.",
    "success",
)}
"""
        ),
        markdown(
            f"""
### Stage 2 mini-check

Before choosing a model, which four controls or clues should you check?

<details>
<summary>Show the suggested answer</summary>

Check the model's description, parameter scale, supported input types, and whether an Effort control is available and appropriate for the task.

</details>

{panel(
    "STAGE 2 CHECKPOINT",
    "Check the model card and match the model and effort level to the task. "
    "Then ask in a clear, token-efficient way.",
    "success",
)}
"""
        ),
        markdown(
            f"""
## Stage 3 — Ask, compare, and question

{panel(
    "IMPORTANT",
    "Stage 3 moves between Google AI Mode, Hugging Face and Gemini so you "
    "can see how the interface, model and prompt affect an answer.<br><br>"
    "<b>HuggingChat allowance:</b> free accounts have <b>20 questions</b>. "
    "Experiment 2 uses two of them.",
    "info",
)}

LLMs are <abbr title='Probabilistic means the model chooses among likely next pieces of text; the same request can produce different wording.' style='text-decoration:underline dotted;cursor:help'><b>probabilistic</b></abbr>. In simple words, models choose from several likely next pieces of text rather than retrieving one fixed sentence. Two runs may therefore use different wording or detail. Ideally, the answers should remain **semantically similar**—their central meaning should agree—even when their phrasing varies.
"""
        ),
        markdown(
            f"""
### Read the icons at the end of each model option

Open [HuggingChat Models](https://huggingface.co/chat/models). A model row may show small capability icons at its right-hand end. Hover over an icon in HuggingChat to see its own label.

<div class='workshop-flex' style='gap:10px;margin:12px 0'>
<div style='flex:1 1 260px;background:#EFF8FF;border:1px solid #B2DDFF;border-radius:10px;padding:13px'><b>💬 Text / natural language model</b><br><small>Best for writing, explaining, translating, summarising, and text questions. It may have no image icon.</small></div>
<div style='flex:1 1 260px;background:#F4F3FF;border:1px solid #D9D6FE;border-radius:10px;padding:13px'><b>🖼️ Vision / multimodal model</b><br><small>The image icon means it accepts images as well as text. Choose this when the task requires looking at a picture, chart, or screenshot.</small></div>
</div>

| What appears at the right | Simple meaning |
|---|---|
| {chip("NO IMAGE ICON")} | Usually text-first: use it for natural-language tasks unless its card says otherwise. |
| {chip("🖼 IMAGE")} | Multimodal: it can inspect image inputs as well as read text. |
| {chip("🔨 HAMMER")} | Tool calling: it can ask connected tools or functions to do an action. |
| {chip("PROVIDER / FASTEST / CHEAPEST")} | Where the model runs, or which service route is selected—not a new model skill. |
| {chip("⚙ SETTINGS")} | Opens controls for that model; it is not a capability badge. |

{panel(
    "CHOOSING RULE",
    "Use a <b>text-first model</b> for the questions below. Choose a "
    "<b>vision model</b> only when your input includes something the model "
    "must see. You may not see every icon on every model row.",
    "success",
)}
"""
        ),
        markdown(
            f"""
### Where your submitted work goes

{panel(
    "YOUR WORKSHEET",
    "When you press <b>Submit & save</b>, look in the VS Code Explorer: "
    "<b>tasks → stage3_answers.json</b>. The file is ignored by Git, so "
    "personal answers are not committed.<br><br>The button does not "
    "magically choose a destination. The Python instructions inside "
    "<a href='../llm_workshop/worksheet.py'><b>llm_workshop/worksheet.py</b></a> "
    "explicitly create the folder and "
    "write the output to that path; clicking the button only triggers "
    "those instructions.",
    "info",
)}

{panel(
    "STAGE 3 KEY CONCEPT",
    "<b>Always know where your output is going—and where to find it.</b> "
    "Before running or submitting anything, identify its destination in "
    "the directory tree.",
    "success",
)}

"""
        ),
        code(
            """
from llm_workshop.worksheet import (
    effort_comparison_box,
    model_comparison_box,
    worksheet_box,
)
"""
        ),
        markdown(
            f"""
{panel(
    "EXPERIMENT 1",
    "<b>Simple fact retrieval.</b> Open Google AI Mode, ask one factual "
    "question, and inspect the answer and source it provides.",
    "task",
)}

Open [Google AI Mode](https://www.google.com/search?udm=50), then send the prompt below.
"""
        ),
        code(
            '''from llm_workshop.prompt_card import copyable_prompt

copyable_prompt(
    """Approximately what percentage of Earth's surface is covered by ocean?
Answer in one sentence and include one source link."""
)''',
            "interactive",
        ),
        code(
            """
worksheet_box(
    "simple_fact",
    answer_label="Paste Google AI Mode's answer:",
    observation_label="What figure did it give, and which source did it cite?",
)
""",
            "interactive",
        ),
        markdown(
            f"""
{panel(
    "EXPERIMENT 2",
    "<b>Small model versus very large model.</b> Translate one Sanskrit "
    "sentence with the exact same prompt and compare the responses.",
    "task",
)}

- [Browse text-generation model cards on Hugging Face](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending)
- [Open the model selector in HuggingChat](https://huggingface.co/chat/models)

1. **Model A:** choose a text model whose card lists **10B parameters or fewer**. Availability changes, so record the exact name you find.
2. **Model B:** use [moonshotai/Kimi-K3 in HuggingChat](https://huggingface.co/chat/models/moonshotai/Kimi-K3). Its card lists **2.8T total parameters** and **104B activated parameters**.
3. Start a fresh chat for each model and use the identical prompt. Do not correct either model midway.

{panel(
    "HYPOTHESIS, NOT A PROMISE",
    "The much larger Kimi K3 may give a more rounded or informative answer, "
    "but parameter size alone never guarantees that it will. Judge the "
    "actual answers.",
    "info",
)}
"""
        ),
        code(
            '''from llm_workshop.prompt_card import copyable_prompt

copyable_prompt(
    """Translate this Sanskrit sentence into clear English.
Then explain its meaning in one short sentence:

विद्या ददाति विनयम्।"""
)''',
            "interactive",
        ),
        markdown(
            f"""

{panel(
    "CHECKPOINT",
    "The literal idea is <b>Knowledge gives humility.</b> Notice whether "
    "each model separates translation from interpretation.",
    "success",
)}
"""
        ),
        code(
            """
model_comparison_box(
    "sanskrit_translation",
    model_a_heading="Model A · small text model (10B or fewer)",
    model_a_placeholder="Enter the small model's exact name",
    model_b_heading="Model B · moonshotai/Kimi-K3",
    model_b_placeholder="moonshotai/Kimi-K3",
    observation_label="Which answer seems more well put together or informative?",
)
""",
            "interactive",
        ),
        markdown(
            f"""
{panel(
    "EXPERIMENT 3",
    "<b>A harder logic-and-rules test.</b> Give Gemini 3.6 Flash the same "
    "12×12 castle task once with Low thinking and once with High thinking. "
    "Compare rule-following, self-checking and any token counts shown.",
    "task",
)}

Open [Google AI Studio](https://aistudio.google.com/prompts/new_chat) and sign in with a Google account.

1. Select **Gemini 3.6 Flash**, start a fresh chat, choose **Low** thinking, and send the prompt once.
2. Start another fresh chat with **Gemini 3.6 Flash**, choose **High** thinking, and send the identical prompt once.
3. Do not repair either answer. Paste both original results into the worksheet.
4. Record exact input/output token counts only if the interface exposes them. Otherwise enter **Not shown**—a model cannot reliably audit its provider's billing counters.

{panel(
    "FAIR TEST",
    "Keep the <b>model, prompt, and fresh-chat context identical</b>. Change "
    "only Effort. This does not prove that High always wins; it tests whether "
    "extra effort helped on this one structured task.",
    "info",
)}
"""
        ),
        code(
            '''from llm_workshop.prompt_card import copyable_prompt

copyable_prompt(
    """Create a 12x12 text grid called a Medieval Castle Logic Map.

Follow every rule exactly:
1. Output exactly 12 grid rows, each containing exactly 12 visible characters.
2. The outer edge is W, except for two gates: G at (0,5) and G at (11,6).
3. Put a tower C at each inner corner: (1,1), (1,10), (10,1), and (10,10).
4. Put exactly four treasures T at (2,2), (4,4), (6,6), and (8,8).
5. For every T at (row, column), place one key K at its horizontal mirror position (row, 11-column). Derive these four K coordinates yourself.
6. On row 9, spell CROWN from left to right, placing exactly one ground dot between consecutive letters. Start C at column 1.
7. No symbol may overwrite another. Fill every unused inner cell with a ground dot (.).
8. Below the grid, list the 0-based coordinates of both G gates, all four tower C cells, all four T cells, all four K cells, and the five CROWN letters.
9. Add a SELF-CHECK confirming: 12 rows; 12 characters per row; 42 border W cells; 2 gates; 4 towers; 4 treasures; 4 mirrored keys; CROWN order; and matching coordinates.

Do not put row numbers, bullets, spaces, or Markdown fences inside the 12 grid rows. Double-check every rule before answering, but do not show hidden reasoning.

Finish with a TOKEN REPORT. If the chat system gives you exact input and output token counts, report them. If those counts are not available to you, write "not available to the model". Never estimate or invent token counts."""
)''',
            "interactive",
        ),
        markdown(
            f"""
Use this quick comparison checklist:

| Check | Low | High |
|---|:---:|:---:|
| Exactly 12 rows of 12 characters | ☐ | ☐ |
| Border has 42 `W`s and the two gates are correct | ☐ | ☐ |
| Four towers and four treasures are correctly placed | ☐ | ☐ |
| Four `K`s mirror the treasure columns using `11-column` | ☐ | ☐ |
| `C.R.O.W.N` occupies row 9 from column 1 | ☐ | ☐ |
| Every coordinate matches the grid | ☐ | ☐ |
| Token report avoids invented numbers | ☐ | ☐ |

{panel(
    "TOKEN COUNT NOTE",
    "The prompt asks for a token report to expose an important limitation: "
    "the model may not have access to exact provider counters. Prefer numbers "
    "shown by the interface. If none are shown, record <b>Not shown</b> and "
    "compare response length and quality without pretending they are exact tokens.",
    "success",
)}
"""
        ),
        code(
            '''effort_comparison_box(
    "castle_effort",
    model_name="Gemini 3.6 Flash",
)''',
            "interactive",
        ),
        markdown(
            f"""
<details style='background:#F4F3FF;border:1px solid #D9D6FE;border-radius:10px;padding:12px'>
<summary><b>Reveal one valid logic map only after recording both attempts</b></summary>

This is the correctly assembled reference:

<pre style='overflow:auto;max-width:100%;box-sizing:border-box'>WWWWWGWWWWWW
WC........CW
W.T......K.W
W..........W
W...T..K...W
W..........W
W....KT....W
W..........W
W..K....T..W
WC.R.O.W.N.W
WC........CW
WWWWWWGWWWWW</pre>

Gates: `(0,5)`, `(11,6)`<br>
Towers: `(1,1)`, `(1,10)`, `(10,1)`, `(10,10)`<br>
Treasures: `(2,2)`, `(4,4)`, `(6,6)`, `(8,8)`<br>
Keys: `(2,9)`, `(4,7)`, `(6,5)`, `(8,3)`<br>
CROWN: `C (9,1)`, `R (9,3)`, `O (9,5)`, `W (9,7)`, `N (9,9)`

</details>

{panel(
    "EXPERIMENT 4",
    "<b>The nearby car-wash test.</b> Compare a fast lightweight model with "
    "a stronger model using extended thinking, then improve the prompt and "
    "test the lightweight model again.",
    "task",
)}

Open [Google Gemini](https://gemini.google.com/app) and sign in with a Google account.

1. Start a fresh chat with **Gemini 3.5 Flash-Lite** and send the prompt once.
2. Start a fresh chat with **Gemini 3.6 Flash** using **High / extended thinking** and send the identical prompt once.
3. Save both original answers. Do not add clarification yet.
"""
        ),
        code(
            '''from llm_workshop.prompt_card import copyable_prompt

copyable_prompt(
    """My car is dirty and needs to be washed. The car wash is only 100 metres from my home. Should I walk there or drive?"""
)''',
            "interactive",
        ),
        code(
            '''model_comparison_box(
    "carwash_model_comparison",
    model_a_heading="Answer A · Gemini 3.5 Flash-Lite",
    model_a_placeholder="Gemini 3.5 Flash-Lite",
    model_b_heading="Answer B · Gemini 3.6 Flash · High / extended thinking",
    model_b_placeholder="Gemini 3.6 Flash · High thinking",
    observation_label="Does either answer contain a logic flaw? Which assumption did it make?",
)''',
            "interactive",
        ),
        markdown(
            f"""
<details style='background:#EFF8FF;border:1px solid #B2DDFF;border-radius:10px;padding:12px'>
<summary><b>Reveal the hidden assumption after saving both answers</b></summary>

The useful answer is to **drive the dirty car**, because the car itself must reach the car wash. Older language models sometimes focused on “100 metres is close” and recommended walking, while missing the goal of the trip.

The prompt never explicitly says that the car must be physically present. The model has to infer that unstated requirement from context. This is an everyday form of **inductive or contextual reasoning** rather than a formal proof. Even clear-looking wording can hide assumptions that a model—or a person—may misunderstand.

</details>

{panel(
    "KEY CONCEPT · INFERENCE AND ASSUMPTIONS",
    "Clarity is not always as obvious as it feels to the writer. Stronger "
    "reasoning can improve contextual inference, but no model should be "
    "trusted to recover every unstated assumption.",
    "info",
)}

### Repeat with the target made explicit

Return to **Gemini 3.5 Flash-Lite** in a fresh chat and send this revised prompt:
"""
        ),
        code(
            '''from llm_workshop.prompt_card import copyable_prompt

copyable_prompt(
    """My car is dirty and needs to be washed. The car wash is only 100 metres from my home. Should I walk there or drive? Consider what needs to be physically present at the destination for the task to be completed."""
)''',
            "interactive",
        ),
        code(
            '''worksheet_box(
    "carwash_clear_prompt",
    answer_label="Paste Gemini 3.5 Flash-Lite's answer to the clearer prompt:",
    observation_label="Did the explicit target remove the logic flaw? What changed?",
)''',
            "interactive",
        ),
        markdown(
            f"""
{panel(
    "KEY TIP",
    "A well-keyed prompt with an explicit target and outcome can improve "
    "response quality without switching to a larger model or activating "
    "higher reasoning.",
    "success",
)}

{panel(
    "EXPERIMENT 5",
    "<b>Repair a broken HTML animation.</b> Run the next cell, copy its red "
    "error and the broken code, then write your own question to an LLM. "
    "Apply the suggested fix and rerun the cell.",
    "task",
)}
"""
        ),
        code(
            '''import random
from IPython.display import HTML, display

# A notebook-native disco scene (no desktop window needed).
rng = random.Random(7)
disco_colors = ["#FF007F", "#00F0FF", "#FFDF00", "#7000FF", "#00FF66", "#FF00FF"]

# BUG: one name below does not match the list name above.
lights = "".join(
    f"<span class='disco-light' style='left:{rng.randint(4, 92)}%;"
    f"top:{rng.randint(8, 70)}%;background:{rng.choice(disco_colours)};"
    f"animation-delay:-{rng.random():.2f}s'></span>"
    for _ in range(22)
)

display(HTML(f"""
<div class="disco-stage">
  <div class="disco-ball">🪩</div>
  <div class="stick-zone">
    <pre class="stick-pose pose-1">  O  \n ╱│╲ \n ╱ ╲ </pre>
    <pre class="stick-pose pose-2"> ╲O╱ \n  │  \n ╱ ╲ </pre>
    <pre class="stick-pose pose-3">  O╱ \n ╱│  \n ╱ ╲ </pre>
    <pre class="stick-pose pose-4"> ╲O  \n  │╲ \n ╱ ╲ </pre>
    <pre class="stick-pose pose-5">**O**\n  │  \n ╱ ╲ </pre>
  </div>
  <div class="dance-caption">🎶 FIXED — UNCE UNCE UNCE 🎶</div>
  {lights}
</div>
<style>
.disco-stage {{ position:relative; height:260px; overflow:hidden; border-radius:16px;
  background:radial-gradient(circle at top, #312e81, #09090b 68%); color:white; }}
.disco-ball {{ text-align:center; font-size:48px; animation:swing 1.2s ease-in-out infinite alternate; }}
.stick-zone {{ position:absolute; z-index:2; left:50%; top:78px; width:130px; height:115px;
  transform:translateX(-50%); }}
.stick-pose {{ position:absolute; inset:0; margin:0; text-align:center; color:#00F0FF;
  font:700 30px/1.15 monospace; text-shadow:0 0 12px #00F0FF; opacity:0;
  animation:showpose 1.5s linear infinite; }}
.pose-2 {{ animation-delay:-.3s; color:#FFDF00; }}
.pose-3 {{ animation-delay:-.6s; color:#FF007F; }}
.pose-4 {{ animation-delay:-.9s; color:#00FF66; }}
.pose-5 {{ animation-delay:-1.2s; color:#FF00FF; }}
.dance-caption {{ position:absolute; z-index:2; bottom:20px; width:100%; text-align:center;
  color:#FFDF00; font:700 16px system-ui; animation:bounce .55s ease-in-out infinite alternate; }}
.disco-light {{ position:absolute; width:14px; height:14px; border-radius:50%;
  animation:flash .7s linear infinite alternate; }}
@keyframes showpose {{ 0%, 19% {{ opacity:1; }} 20%, 100% {{ opacity:0; }} }}
@keyframes flash {{ from {{ opacity:.18; transform:scale(.55); }} to {{ opacity:1; transform:scale(1.7); }} }}
@keyframes bounce {{ to {{ transform:translateY(-8px); }} }}
@keyframes swing {{ to {{ transform:translateX(35px) rotate(18deg); }} }}
</style>
"""))''',
            "expected-error",
        ),
        markdown(
            f"""
<details style='background:#FFFAEB;border:1px solid #FEDF89;border-radius:10px;padding:12px'>
<summary><b>Hint: use a short troubleshooting loop</b></summary>

1. Read the final line of the red traceback.
2. Copy the broken code and traceback into the LLM.
3. Ask for either the whole corrected block or only the exact line to replace.
4. Change only the bug, then rerun the same cell.

</details>

<details style='background:#ECFDF3;border:1px solid #ABEFC6;border-radius:10px;padding:12px'>
<summary><b>Show one possible repair after you have tried</b></summary>

Python reports that `disco_colours` is not defined. The list was created as `disco_colors`. Change only that name in the `rng.choice(...)` line, then rerun the broken cell.

</details>

{panel(
    "CHECKPOINT",
    "Troubleshooting is a loop: <b>run → read the last error line → ask or "
    "inspect → make one repair → rerun</b>. The LLM can suggest a fix, but "
    "you choose what code changes and verify the result yourself.",
    "success",
)}
"""
        ),
        markdown(
            f"""
{panel(
    "STAGE 3 CHECKPOINT",
    "<ul style='margin:0;padding-left:20px'>"
    "<li>separate text-first models from vision or multimodal models;</li>"
    "<li>expect probabilistic wording while checking semantic meaning;</li>"
    "<li>change only one variable when comparing Low and High effort;</li>"
    "<li>use provider token counts when shown—never invented estimates;</li>"
    "<li>use the stated 20-question HuggingChat allowance deliberately;</li>"
    "<li>distinguish translation from interpretation;</li>"
    "<li>check hidden assumptions before accepting a confident answer;</li>"
    "<li>make the target explicit before paying for more reasoning;</li>"
    "<li>use a short run–repair–rerun troubleshooting loop;</li>"
    "<li>find saved work in <b>tasks/stage3_answers.json</b>.</li></ul>"
    "<p style='margin:10px 0 0'><b>Always know where your output is going "
    "and where to find it.</b></p>",
    "success",
)}
"""
        ),
        markdown(
            f"""
## Main task — Build and refine a shopping catalogue

{panel(
    "NOTEBOOK 1 · MAIN VIBE-CODING TASK",
    "Use GitHub Copilot Chat inside VS Code to build, open, inspect, and "
    "repeatedly improve a shopping catalogue. Ask Copilot to <b>return the "
    "code in chat</b>; create and edit the HTML file yourself. The goal is "
    "to practise expressing a target and steering one change at a time.",
    "task",
)}

{panel(
    "THE REITERATION LOOP",
    "<div style='font-weight:700;text-align:center;letter-spacing:0.02em'>"
    "PROMPT → BUILD → OPEN → INSPECT → REQUEST ONE CHANGE → VERIFY AGAIN"
    "</div><div style='margin-top:7px'>Your first result is a starting "
    "point. Each preview gives you evidence for the next small prompt.</div>",
    "keyword",
)}

### 1 · Inspect the data and define the first version

<table style="width:100%;table-layout:fixed">
<tr><td style="width:22%"><b>Data</b></td><td><code>data/notebook1/products.csv</code>: 18 product records and their image filenames, with columns including <code>release_date</code> and <code>country_of_origin</code>.</td></tr>
<tr><td><b>Output</b></td><td>One file that you create yourself: <code>tasks/notebook1/catalogue.html</code>.</td></tr>
<tr><td><b>Target</b></td><td>You need to build a simple shopping catalogue of the items listed in the <code>*.csv</code> file. The catalogue should be neat and organised and should display information that would be relevant to potential consumers. Inspect the CSV file to learn what information it contains.</td></tr>
</table>

**CSV** means comma-separated values: a plain-text table where each row is one record and each column is one kind of information.

**HTML** is the file type used to structure a webpage that a browser can open and display.

{panel(
    "CONTROLLED MESSY DATA",
    "The product IDs are deliberately out of order, and one image filename "
    "does not match a file in the image folder. Keep every product row: your "
    "catalogue should handle imperfect source data without hiding the item.",
    "task",
)}

The first version should:

- load `../../data/notebook1/products.csv` in the browser;
- map each CSV image filename to `../../data/notebook1/<filename>`;
- create one card per CSV row rather than hard-coding 18 cards;
- use equal square image areas and consistent card heights;
- format every price with two decimal places;
- use plain HTML, CSS and JavaScript with no framework or package install;
- show a friendly message if the CSV cannot be loaded;
- show an appropriate message or icon if an individual image is missing.

{catalogue_preview()}

The preview above is deliberately compact and follows CSV order: three colour
variants of each product type sit together. It is an inventory glance, not the
large shopping-card layout you are asking Copilot to build.

### 2 · Write the first prompt and build

{panel(
    "QUICKLY OPEN COPILOT CHAT",
    "Open Chat directly: on Windows or Linux press <kbd>Ctrl</kbd> + "
    "<kbd>Alt</kbd> + <kbd>I</kbd>; on macOS press <kbd>Control</kbd> + "
    "<kbd>Command</kbd> + <kbd>I</kbd>.<br><br>Fallback: open the Command "
    "Palette with <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> on "
    "Windows or Linux, or <kbd>Command</kbd> + <kbd>Shift</kbd> + "
    "<kbd>P</kbd> on macOS. Run <b>Chat: Open Chat</b>. Some VS Code "
    "versions label the command <b>Chat: Focus on Chat View</b>.",
    "keyword",
)}

1. In the Explorer, open `data/notebook1/products.csv`. Inspect its columns, image filenames and deliberately mixed ID order.
2. Open **GitHub Copilot Chat** with one of the shortcuts above and use **Ask/Chat mode**, not an automatic file-editing mode.
3. Explain the **data**, **output**, **target** and requirements above in your own words. Tell Copilot not to create or edit files; ask it to return one complete HTML document in chat.
4. Read its short plan. If it misunderstood a path or requirement, correct the instruction before accepting code.
5. In the Explorer, create `tasks/notebook1/catalogue.html`, then copy the returned HTML code into that file and save it.
6. Right-click `catalogue.html` and choose **Show Preview**. The Codespace includes VS Code Live Preview so the browser can load the CSV.

{panel(
    "KEY CONCEPT · ARTICULATE THE TARGET",
    "A coding agent works best when you can express the data it should read, "
    "the output you will create, the target you want to see, and the checks "
    "that define success. Also state what should <b>not</b> appear yet. "
    "Asking for code in chat and placing it yourself reinforces ownership "
    "of the file path.",
    "success",
)}
"""
        ),
        code(
            '''worksheet_box(
    "catalogue_brief",
    answer_label="Write the instruction you will send to GitHub Copilot:",
    observation_label="After opening the first version, what is its most important mismatch?",
)''',
            "interactive",
        ),
        markdown(
            f"""
### 3 · Inspect before asking again

Check the evidence in the preview before writing another prompt:

- Did all 18 rows become catalogue entries, including the one with a missing image?
- Does the page show useful consumer information without displaying every CSV field?
- Does the missing image show an appropriate fallback message or icon?
- Did the out-of-order IDs accidentally control the display order?
- Is the strongest problem a data problem, a layout problem, or a prompt problem?

### 4 · Reiterate one change at a time

Use the same chat so Copilot has the current code, but make each request small.
You may ask for one complete revised HTML document or the exact section to
replace; you still make the edit in `catalogue.html` yourself.

1. **Visibility round:** add a **More details** control. It may reveal colour,
   release date, sizes, country of origin and designer, but those fields should
   remain hidden when the page first opens.
2. **Sorting round:** add choices for original CSV order, ID number,
   price low-to-high, price high-to-low, and newest release. Test whether
   numerical ID sorting restores the expected sequence.
3. **Relevance round:** decide which optional details genuinely help a shopper.
   Ask to hide one unhelpful field, or reveal only the useful fields instead
   of displaying every available column.

A useful follow-up prompt contains four parts:

| Part | What to write |
|---|---|
| **Evidence** | What you can see in the current preview. |
| **One change** | The single behaviour or field you want changed. |
| **Preserve** | What already works and must stay unchanged. |
| **Check** | How you will know the revision succeeded. |

{panel(
    "KEY CONCEPT · REITERATION LOOP",
    "A useful first prompt sets direction; useful follow-up prompts steer "
    "the result. Change one thing, reopen the page, and verify both the new "
    "behaviour and the parts that should remain stable. Showing every field "
    "is not automatically better—relevance is part of the design.",
    "success",
)}
"""
        ),
        code(
            '''worksheet_box(
    "catalogue_reiteration",
    answer_label="Write one small follow-up prompt using evidence, one change, preserve and check:",
    observation_label="What changed after you applied it, and what will you verify next?",
)''',
            "interactive",
        ),
        markdown(
            f"""
### Final catalogue check

- [ ] All 18 CSV rows become 18 catalogue entries.
- [ ] The 17 valid image paths work, and the missing image has a useful fallback.
- [ ] Each entry shows information that is relevant to a potential consumer.
- [ ] Optional metadata is hidden when the page first opens.
- [ ] A deliberate control can reveal the optional details chosen as useful.
- [ ] A sort control can order by ID number, price and release date.
- [ ] Irrelevant fields remain hidden, and you can explain that choice.
- [ ] The layout is neat, with no clipped text or sideways scrolling.
- [ ] The result is saved at `tasks/notebook1/catalogue.html`.

Do not judge only by appearance. Check the CSV-to-image mapping, try the
controls, resize the preview, and confirm that a later change did not break
something that worked in the previous version.
"""
        ),
        markdown(
            f"""
## Orientation complete

{panel(
    "READY",
    "You are ready when you can find the course folders, choose an AI "
    "interface, describe a target, and verify where its output belongs."
    "<br><br><b>Next action:</b> finish and preview "
    "<b>tasks/notebook1/catalogue.html</b>.",
    "success",
)}
"""
        ),
    ]

    notebook = nbf.v4.new_notebook(cells=cells)
    notebook.metadata.kernelspec = {
        "display_name": "Python (Vibe Workshop)",
        "language": "python",
        "name": "llm-workshop",
    }
    notebook.metadata.language_info = {"name": "python", "version": "3.12"}
    nbf.write(notebook, NOTEBOOK)
    print(f"Built {NOTEBOOK.relative_to(ROOT)} with {len(cells)} cells")


if __name__ == "__main__":
    main()
