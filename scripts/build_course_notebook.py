"""Build the learner-facing onboarding notebook from readable cell sources."""

from __future__ import annotations

import csv
from copy import deepcopy
from html import escape
from pathlib import Path
import sys

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from llm_workshop.course import WORKBOOKS
from llm_workshop.presentation import readable_html
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
    "warning": {
        "background": "#FEF3F2",
        "border": "#FECDCA",
        "accent": "#B42318",
    },
}


def markdown(source: str):
    return nbf.v4.new_markdown_cell(source.strip())


def code(source: str, *tags: str):
    cell = nbf.v4.new_code_cell(source.strip())
    cell_tags = list(tags)
    if any(marker in cell.source for marker in ("worksheet_box(", "copyable_prompt(")) or "hide-input" in cell_tags:
        cell.metadata["inputCollapsed"] = True
        cell.metadata["jupyter"] = {"source_hidden": True}
        if "hide-input" not in cell_tags:
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


def interface_intro(name: str, guidance: str, extra: str = ""):
    """Introduce one resource with consistent save-location guidance."""
    return markdown(
        f"## Try the AI interface · {name}\n\n"
        + panel(
            "IMPORTANT",
            guidance + "<br><br>"
            "<b>Your submitted worksheet:</b> each <b>Submit & save</b> button writes "
            "its labelled answer to <b>tasks → workbook_answers.json</b>. "
            "This answer file is ignored by Git. The instructions inside "
            "<b>llm_workshop/worksheet.py</b> explicitly choose the path; "
            "the button only runs those instructions.<br><br>"
            "<b>Always know where your output is going—and where to find it.</b>",
            "info",
        )
        + ("\n\n" + extra if extra else "")
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


def build_lesson_cells():
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
    "<b>Run each cell from top to bottom.</b> Nothing in the opening directions "
    "sends data to an API.<br><br><b>Using GitHub Codespaces?</b> Python "
    "runs inside the online workspace, so you do not need it installed on "
    "your laptop. If prompted for a kernel, select "
    "the Python interpreter marked <b>.venv</b>.",
    "info",
)}
"""
        ),
        code(
            """
import random
from pathlib import Path

from IPython.display import HTML, display

from llm_workshop.prompt_card import copyable_prompt
from llm_workshop.quiz import readme_quiz
from llm_workshop.worksheet import worksheet_box
""",
            "setup",
            "hide-input",
        ),
        markdown(
            f"""
## Find your way around

You do not need to memorize commands. The aim is to learn where things live and how to ask for a clear outcome.

{panel(
    "COLOUR KEY",
    chip("KEYWORD") + " marks a useful term. &nbsp; "
    + chip("TASK", "task") + " tells you to do something. &nbsp; "
    + chip("CHECKPOINT", "success") + " shows progress.",
    "info",
)}

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
workspace = WORKSHOP_ROOT
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
    "QUESTION 1 · QUICK CHECK",
    "Choose an answer and press <b>Submit answer</b>. The question panel "
    "turns green for a correct answer and red when you should try again.",
    "task",
)}
"""
        ),
        code(
            """
readme_quiz()
""",
            "interactive",
        ),
        markdown(
            f"""
{panel(
    "READY TO CONTINUE",
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
## Choose an AI helper and prompt deliberately

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

### A six-point prompt check

1. **Set the objective:** decide whether you need information, ideas, or a problem solved.
2. **Be clear and concise:** use direct language and remove vague instructions.
3. **Add useful context:** include the background needed for the task, but not unrelated material.
4. **Experiment and iterate:** improve the wording after seeing what the first answer misses.
5. **Name the audience:** say who will read or use the result.
6. **Evaluate and adapt:** check the output and adjust rather than accepting it automatically.

<div class='workshop-flex' style='gap:8px;margin:12px 0'>
<div style='flex:1 1 180px;background:#EFF8FF;border:1px solid #B2DDFF;border-radius:9px;padding:10px'><b>Ask clearly</b><br><small>State the task, audience, and output format.</small></div>
<div style='flex:1 1 180px;background:#EFF8FF;border:1px solid #B2DDFF;border-radius:9px;padding:10px'><b>Send only what is needed</b><br><small>Avoid entire folders or repeated context.</small></div>
<div style='flex:1 1 180px;background:#EFF8FF;border:1px solid #B2DDFF;border-radius:9px;padding:10px'><b>Request a useful length</b><br><small>For example: “Answer in five bullets.”</small></div>
</div>

<details style='background:#F4F3FF;border:1px solid #D9D6FE;border-radius:10px;padding:12px'>
<summary><b>PROMPTING RESOURCES AND MORE GUIDES</b></summary>

**Suggested starting points**

- [Google Prompt Engineering guide (PDF)](https://drive.google.com/file/d/1AbaBYbEa_EbPelsT40-vj64L-2IwUJHy/view) — Google Drive may ask you to sign in.
- [Community forum: crafting effective prompts](https://community.openai.com/t/a-guide-to-crafting-effective-prompts-for-diverse-applications/493914) — source of the six-point outline above.
- [AMALYTIX directory of free prompting guides](https://www.amalytix.com/en/blog/free-prompt-engineering-guides/) — a third-party roundup.

**More references**

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
    "KEY CONCEPT · PROMPT DELIBERATELY",
    "State the objective, add only useful context, request an appropriate "
    "format and length, then inspect the answer before asking again. Clear "
    "prompts protect both attention and tokens.",
    "success",
)}
"""
        ),
        markdown(
            f"""
### QUESTION 2 · Prompt-and-token mini-check

Which prompt is likely to be more token-efficient while still giving a useful answer?

- **A:** “Tell me everything about oceans.”
- **B:** “In five bullets for a 12-year-old, explain why oceans matter to Earth.”

<details>
<summary>Show the suggested answer</summary>

**B** gives the model an audience, subject and useful output length. It is more likely to return a focused answer without unnecessary material.

</details>

{panel(
    "READY TO EXPERIMENT",
    "Keep the objective clear, provide only relevant context, and request a "
    "useful answer length. You will inspect model cards and effort controls when each becomes relevant.",
    "success",
)}
"""
        ),
        interface_intro(
            "Google AI Mode",
            "Use <b>Google AI Mode</b> for this workbook's fact-retrieval activity. "
            "Ask one focused question, then inspect the answer and the source "
            "behind it. If no source is given, ask for a citation or source link.",
        ),
        markdown(
            f"""
{panel(
    "EXPERIMENT 1",
    "<b>Simple fact retrieval.</b> Open Google AI Mode, ask one factual "
    "question, and inspect both the answer and its source.",
    "task",
)}

Open [Google AI Mode](https://www.google.com/search?udm=50), then send the prompt below.
"""
        ),
        code(
            '''copyable_prompt(
    """Approximately what percentage of Earth’s surface is covered by ocean?
Answer in one sentence and include one source link."""
)''',
            "interactive",
        ),
        code(
            f'''worksheet_box(
    "google_fact_answer",
    question_label="QUESTION 3 · Record the AI answer",
    response_label="Paste Google AI Mode’s answer:",
    reveal_html={(panel(
        "OPEN THE SAVED JSON FILE",
        "In the VS Code Explorer, open <b>tasks → workbook_answers.json</b>. "
        "<b>JSON</b> (JavaScript Object Notation) is a plain-text format that "
        "stores structured information as named keys and values. It is commonly "
        "used around modern LLM applications for API messages, tool calls and "
        "structured outputs.",
        "success",
    ) + panel(
        "CHECK REFERENCES AND CLAIMS",
        "Some AI services provide references automatically; others need to be "
        "asked. Even as many systems improve, an LLM can still hallucinate—give "
        "a confident answer that is unsupported or incorrect. Ask for sources, "
        "open them, and inspect important claims before relying on the output.",
        "success",
    ))!r},
)''',
            "interactive",
        ),
        code(
            f'''worksheet_box(
    "google_fact_source",
    question_label="QUESTION 4 · Check the fact and source",
    response_label="What percentage did it give, and which source did it cite?",
    reveal_html={panel(
        "KEY TIP · ASK FOR A CITATION",
        "Make source checking a habit whenever you ask an AI to retrieve a "
        "fact, figure or other data. Ask for a citation or source link if one "
        "is missing, then open it and check that it actually supports the "
        "answer. A citation can be incorrect or invented too—check the original "
        "source rather than trusting the link alone.",
        "success",
    )!r},
)''',
            "interactive",
        ),
        interface_intro(
            "HuggingChat",
            "Use <b>HuggingChat</b> to try different models, and <b>Hugging Face "
            "model cards</b> to find out what each model is designed to do. "
            "Compare the responses to the same prompt.<br><br>"
            "<b>HuggingChat allowance:</b> free accounts have <b>20 questions</b>. "
            "Experiment 2 uses four of them.",
            "LLMs are <abbr title='Probabilistic means the model chooses among likely next pieces of text; the same request can produce different wording.' style='text-decoration:underline dotted;cursor:help'><b>probabilistic</b></abbr>. "
            "In simple words, models choose from several likely next pieces of text rather "
            "than retrieving one fixed sentence. Two runs may therefore use different wording "
            "or detail. Ideally, the answers should remain **semantically similar**—their "
            "central meaning should agree—even when their phrasing varies.",
        ),
        markdown(
            f"""
### HuggingChat models: read the card and the icons

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
{panel(
    "EXPERIMENT 2",
    "<b>Small model versus very large model.</b> Translate one Sanskrit "
    "sentence with the exact same prompt and compare the responses.",
    "task",
)}

- [Browse text-generation model cards on Hugging Face](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending)
- [Open the model selector in HuggingChat](https://huggingface.co/chat/models)

1. **Answer A:** choose a text model whose card lists **10B parameters or fewer**. Record its exact name.
2. **Answer B:** use [moonshotai/Kimi-K3 in HuggingChat](https://huggingface.co/chat/models/moonshotai/Kimi-K3). Its card lists **2.8T total parameters** and **104B activated parameters**.
3. Start a fresh tab or chat for each model and use the identical prompt. Do not correct either model midway.

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
            '''copyable_prompt(
    """Translate this Sanskrit sentence into clear English.
Then explain its meaning in one short sentence:

विद्या ददाति विनयम्।"""
)''',
            "interactive",
        ),
        code(
            '''worksheet_box(
    "sanskrit_small_answer",
    question_label="QUESTION 5 · Answer A — small model",
    response_label="Write the exact Model A name, then paste Answer A:",
    response_height="150px",
)''',
            "interactive",
        ),
        code(
            f'''worksheet_box(
    "sanskrit_large_answer",
    question_label="QUESTION 6 · Answer B — moonshotai/Kimi-K3",
    response_label="Paste Answer B from moonshotai/Kimi-K3:",
    response_height="150px",
    reveal_html={panel(
        "LANGUAGE CHOICE",
        "Many models are trained on text in multiple languages, so you can often "
        "communicate with an LLM in the language that is most comfortable for "
        "you. Performance varies: lower-resource or less-documented languages may "
        "be translated or understood less reliably. Verify important meaning with "
        "a fluent speaker or a trusted reference.",
        "success",
    )!r},
)''',
            "interactive",
        ),
        code(
            f'''worksheet_box(
    "sanskrit_comparison",
    question_label="QUESTION 7 · Compare Answer A with Answer B",
    response_label="Which answer seems more well put together or informative, and why?",
    reveal_html={(panel(
        "CHECKPOINT",
        "The literal idea is <b>Knowledge gives humility.</b> Check whether "
        "each model separated translation from interpretation.",
        "success",
    ) + panel(
        "MODEL SIZE, QUALITY AND COST",
        "A larger parameter count usually means greater model capacity and often "
        "comes with more training compute, which can support more refined answers. "
        "It does <b>not</b> prove that the training data or every response is "
        "better. Larger models also generally need more memory, computation and "
        "energy during inference, so they tend to cost more. Choose by the quality "
        "the task requires, then weigh that against speed and cost.",
        "success",
    ))!r},
)''',
            "interactive",
        ),
        markdown(
            f"""
### Challenge the same two models with an expert reasoning task

Use the **same small model** chosen for Question 5 and **moonshotai/Kimi-K3** from Question 6. Start a fresh chat for each, send the identical prompt once, and let each model finish.

{panel(
    "OBSERVE THE VISIBLE REASONING",
    "Some interfaces display a thinking panel or a short reasoning summary; "
    "this is not necessarily the model’s complete private chain of thought. "
    "Compare only what the interface actually shows and the final answer. "
    "Do not paste either full response into this notebook.",
    "info",
)}

While both models work, contemplate:

1. Which model showed a longer visible reasoning process?
2. Did either model fail, hang, repeat itself, or become lost in a reasoning loop?
3. Did one visible reasoning trace contain more useful detail?
4. Did either model insert special characters, equations, headings, or other formatting?
"""
        ),
        code(
            '''copyable_prompt(
    """A fungal metabolic model contains the reaction
cer1_26 + 2 H⁺ + 2 ferrocytochrome b5 + O₂ → cer2_26 + H₂O + 2 ferricytochrome b5

Two candidate annotations are proposed:
A. EC 1.14.19.17, a sphingolipid Δ4 desaturase whose canonical reaction produces 2 H₂O.
B. EC 1.14.18.6, a sphingolipid C4 hydroxylase whose canonical reaction produces 1 H₂O.

The product cer2_26 is named Ceramide 2 Phytosphingosine C26:0, while cer1_26 is Ceramide 1 Sphinganine C26:0.

Determine which EC assignment is chemically and biologically most consistent. Do not rely on the metabolite names alone. Instead:

1. infer the structural transformation implied by each enzyme class;
2. account for O₂, proton, cytochrome-b5 and water stoichiometry;
3. identify whether the encoded reaction itself is chemically balanced;
4. explain whether a bad stoichiometric representation could cause the wrong EC to appear superficially correct;
5. state what additional database evidence you would require before modifying the SBML annotation.

If the reaction, name and candidate EC assignments cannot all simultaneously be correct, explicitly identify which fields are most likely wrong and give a corrected reaction hypothesis."""
)''',
            "interactive",
        ),
        code(
            f'''worksheet_box(
    "expert_reasoning_comparison",
    question_label="QUESTION 8 · Compare the visible reasoning",
    response_label="Record only your four observations; do not paste the full model responses:",
    response_height="170px",
    reveal_html={panel(
        "BENCHMARK CONTEXT",
        "Published benchmarks show meaningful capability differences on difficult "
        "expert tasks. Moonshot AI’s model card reports <b>93.5 on GPQA Diamond</b> "
        "and <b>58.7 on SciCode</b> for Kimi K3 at maximum reasoning effort, along "
        "with long-context and software-engineering results. "
        "<a href='https://github.com/MoonshotAI/Kimi-K3/blob/main/README.md'>"
        "Open the Kimi K3 model card</a>. GPQA is a difficult graduate-level, "
        "Google-proof science benchmark; "
        "<a href='https://arxiv.org/abs/2311.12022'>read its paper</a>. These are "
        "reported benchmark results, not a guarantee that one model will answer "
        "this particular question correctly.",
        "success",
    )!r},
)''',
            "interactive",
        ),
        markdown(
            f"""
{panel(
    "QUESTION 9 · FACT-CHECK THE EC NUMBERS",
    "<b>The prompt deliberately contains a small annotation error.</b><br><br>"
    "<b>A.</b> EC 1.14.19.17 — claimed to be a sphingolipid Δ4 desaturase "
    "whose canonical reaction produces 2 H₂O.<br>"
    "<b>B.</b> EC 1.14.18.6 — claimed to be a sphingolipid C4 hydroxylase "
    "whose canonical reaction produces 1 H₂O.<br><br>"
    "Open the authoritative entries: "
    "<a href='https://enzyme.expasy.org/EC/1.14.18.6'>EC 1.14.18.6</a>, "
    "<a href='https://enzyme.expasy.org/EC/1.14.19.17'>EC 1.14.19.17</a>, and "
    "<a href='https://enzyme.expasy.org/EC/1.14.18.5'>EC 1.14.18.5</a>."
    "<br><br><b>Which statement is wrong, and what should it say?</b>",
    "warning",
)}

**Knowledge retrieval and reasoning are different abilities.** A model may be excellent at redox chemistry and structural inference yet misremember a specific enzyme classification.

Within a conversation, an LLM uses its current context like short-term working memory. In a very large context—or during a task with many internal reasoning steps—important details can become diluted, overlooked, or confused with nearby information.

This is why a strong reasoning process can still end with a small identifier error. Experts evaluate these systems with guardrails, checkpoints, and source inspection; we can do the same.
"""
        ),
        code(
            f'''worksheet_box(
    "ec_number_fact_check",
    question_label="QUESTION 9 · State the corrected EC assignment",
    response_label="Which candidate statement is wrong? Write the correct EC number and enzyme name:",
    reveal_html={panel(
        "FACT-CHECK ANSWER",
        "<b>Statement B is wrong.</b> EC 1.14.18.6 is a "
        "<b>4-hydroxysphinganine ceramide fatty acyl 2-hydroxylase</b>, not the "
        "sphingolipid C4 hydroxylase. The C4 enzyme is <b>EC 1.14.18.5, "
        "sphingolipid C4-monooxygenase</b>; its canonical reaction forms a "
        "phytoceramide and one H₂O. Statement A correctly identifies EC "
        "1.14.19.17 as sphingolipid 4-desaturase, whose canonical reaction forms "
        "two H₂O. Before editing SBML, still confirm metabolite structures, "
        "database identifiers, atom/charge balance, organism evidence and the "
        "original model source.",
        "success",
    )!r},
)''',
            "interactive",
        ),
        markdown(
            f"""
{panel(
    "EXPERIMENT 3",
    "<b>Vision inside VS Code.</b> Connect a vision-capable OpenRouter model "
    "to Copilot Chat, attach the supplied image, and trace what the request cost.",
    "task",
)}

{panel(
    "OPEN COPILOT CHAT INSIDE VS CODE",
    "On Windows or Linux press <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + "
    "<kbd>I</kbd>; on macOS press <kbd>Control</kbd> + <kbd>Command</kbd> + "
    "<kbd>I</kbd>.<br><br>Fallback: open the Command Palette with "
    "<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> on Windows/Linux or "
    "<kbd>Command</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> on macOS, then run "
    "<b>Chat: Open Chat</b> or <b>Chat: Focus on Chat View</b>.",
    "keyword",
)}

{panel(
    "ONE-TIME SETUP · CONNECT OPENROUTER",
    "<ol style='margin:0;padding-left:22px'>"
    "<li>Create a free <a href='https://openrouter.ai/'>OpenRouter</a> account, "
    "then open <a href='https://openrouter.ai/workspaces/default/keys'>"
    "OpenRouter Keys</a> and create a key.</li>"
    "<li>In the Chat model picker, choose <b>Other Models</b>, then the "
    "<b>Manage Language Models</b> gear icon.</li>"
    "<li>Select <b>Add Models → OpenRouter</b>. Enter a group name if asked, "
    "then paste the key into VS Code's secure API-key prompt and press Enter.</li>"
    "<li>To replace it later, return to the gear icon, choose the OpenRouter "
    "provider, and select <b>Update API Key</b>.</li>"
    "</ol>",
    "info",
)}

{panel(
    "KEEP THE KEY PRIVATE",
    "Paste the key only into VS Code's secure API-key prompt. Never put it in "
    "this notebook, a chat message, <code>.env</code>, a screenshot, or a "
    "committed file.",
    "task",
)}

| OpenRouter free-account limit | Allowance |
|---|---|
| Free-model requests per day | **50** |
| Requests per minute | **20** |
| Token charge on models ending in `:free` | **$0** |
| Free models available | **25+** |

See [OpenRouter pricing](https://openrouter.ai/pricing) for the live plan details.

### Select the vision model

1. In **Manage Language Models**, make **Gemma 4 26B A4B** visible, then select it from the Chat model picker. Its OpenRouter ID is [`google/gemma-4-26b-a4b-it`](https://openrouter.ai/google/gemma-4-26b-a4b-it).
2. Choose the arrow beside the model name and set **Thinking Effort → Medium**.

<div style='background:#F8FAFC;border:1px solid #D0D5DD;border-radius:12px;padding:12px;margin:12px 0;max-width:100%;box-sizing:border-box;text-align:center'>
<img src='../data/notebook1/Screenshot%202026-02-23%20145127.png' alt='Vision experiment source image' style='display:block;width:min(100%,480px);height:auto;margin:0 auto;border-radius:8px'>
<div style='font-size:0.75rem;color:#667085;margin-top:7px'>SOURCE IMAGE · data/notebook1/Screenshot 2026-02-23 145127.png</div>
</div>

### Attach the image and ask

1. Drag **Screenshot 2026-02-23 145127.png** directly from the Explorer into Copilot Chat.
2. Confirm that an image/file chip appears in the Chat box.
3. Send the prompt below.
"""
        ),
        code(
            '''copyable_prompt(
    """Describe what is shown in this image."""
)''',
            "interactive",
        ),
        code(
            f'''worksheet_box(
    "vision_description",
    question_label="QUESTION 10 · Record the vision answer",
    response_label="Paste Gemma 4 26B A4B’s description of the image:",
    response_height="150px",
    reveal_html={panel(
        "VISION MODELS AND OCR",
        "A vision model interprets images using patterns learned during training. "
        "Like a person, it can struggle when an image is low-quality, obscure or "
        "hard to distinguish. When text is clear enough, a vision model can also "
        "extract it from an image—similar to modern <b>OCR</b>, or optical "
        "character recognition. Check important details against the original image.",
        "success",
    )!r},
)''',
            "interactive",
        ),
        markdown(
            """
### Check where the vision request was charged

Open [OpenRouter Activity](https://openrouter.ai/activity), select the vision request, and look for:

- **Route:** which provider route actually handled the model request.
- **Input / output tokens:** how much content was sent to and generated by the model.
- **Cost:** whether the route was free or the amount charged.

OpenRouter-key usage is measured by OpenRouter and does **not** use a Copilot request allowance.
"""
        ),
        code(
            '''worksheet_box(
    "vision_cost",
    question_label="QUESTION 11 · Trace the vision request",
    response_label="From OpenRouter Activity, record the route, input/output tokens if shown, cost, and whether it was free or paid:",
)''',
            "interactive",
        ),
        markdown(
            f"""
### Compare with GitHub-provided Copilot usage

For GitHub-provided Copilot usage, open [GitHub Billing and licensing](https://github.com/settings/billing), then choose **AI usage**, or check **Copilot settings → Usage**. The current Copilot Free plan includes up to **2,000 inline code completions per month**; Chat uses a limited monthly GitHub AI Credits allowance and Auto model selection. Read the [current Copilot plan details](https://docs.github.com/en/copilot/get-started/plans) rather than assuming an older fixed number of chats.

{panel(
    "KEY CONCEPT · TRACE THE PROVIDER",
    "The interface and the model provider are not always the same. VS Code "
    "displayed this chat, OpenRouter routed and measured the inference, and "
    "your selected model interpreted the image. Check the activity page that "
    "belongs to the provider holding the key.",
    "success",
)}

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

{panel(
    "EXPERIMENT 4",
    "<b>The nearby car-wash test.</b> Compare the same lightweight model at "
    "two effort settings, then improve the prompt and test it again. Keeping "
    "the model and prompt identical makes the effort comparison fairer and "
    "more reproducible.",
    "task",
)}

Open [Google Gemini](https://gemini.google.com/app) and sign in with a Google account.

{panel(
    "START WITH A FRESH CONTEXT WINDOW",
    "Choose <b>New chat</b> in Gemini before each run. A <b>context window</b> "
    "is the amount of prompt text, conversation history, attachments and output "
    "a model can consider at one time. It is measured in tokens and is usually "
    "listed on the model card or model description. A fresh chat prevents the "
    "first answer from influencing the second comparison.",
    "success",
)}

1. Create a new chat with **Gemini 3.5 Flash-Lite** at its default or low effort and send the prompt once.
2. Create another new chat with the **same Gemini 3.5 Flash-Lite model**, select **High / extended thinking**, and send the identical prompt once.
3. Save both original answers separately. Do not add clarification yet.
"""
        ),
        code(
            '''copyable_prompt(
    """My car is dirty and needs to be washed. The car wash is only 100 metres from my home. Should I walk there or drive?"""
)''',
            "interactive",
        ),
        code(
            '''worksheet_box(
    "carwash_answer_a",
    question_label="QUESTION 12 · Answer A — Gemini 3.5 Flash-Lite at default effort",
    response_label="Paste the original Flash-Lite answer:",
    response_height="140px",
)''',
            "interactive",
        ),
        code(
            '''worksheet_box(
    "carwash_answer_b",
    question_label="QUESTION 13 · Answer B — Gemini 3.5 Flash-Lite with extended thinking",
    response_label="Paste the same model’s extended-thinking answer:",
    response_height="140px",
)''',
            "interactive",
        ),
        code(
            f'''worksheet_box(
    "carwash_logic",
    question_label="QUESTION 14 · Compare the logic",
    response_label="Does either answer contain a logic flaw? Which assumption did it make?",
    reveal_html={panel(
        "REVEAL · THE HIDDEN ASSUMPTION",
        "The useful answer is to <b>drive the dirty car</b>, because the car "
        "must reach the car wash. The prompt never explicitly says the car "
        "must be physically present. Inferring that unstated requirement is "
        "an everyday form of inductive or contextual reasoning.",
        "info",
    )!r},
)''',
            "interactive",
        ),
        markdown(
            f"""
{panel(
    "KEY CONCEPT · INFERENCE AND ASSUMPTIONS",
    "Clarity is not always as obvious as it feels to the writer. Stronger "
    "reasoning can improve contextual inference, but no model should be "
    "trusted to recover every unstated assumption.",
    "info",
)}

### Repeat with the target made explicit

Return to **Gemini 3.5 Flash-Lite** in a fresh tab or chat and send this revised prompt:
"""
        ),
        code(
            '''copyable_prompt(
    """My car is dirty and needs to be washed. The car wash is only 100 metres from my home. Should I walk there or drive? Consider what needs to be physically present at the destination for the task to be completed."""
)''',
            "interactive",
        ),
        code(
            '''worksheet_box(
    "carwash_clear_answer",
    question_label="QUESTION 15 · Record the clearer-prompt answer",
    response_label="Paste Gemini 3.5 Flash-Lite’s answer to the clearer prompt:",
    response_height="140px",
)''',
            "interactive",
        ),
        code(
            f'''worksheet_box(
    "carwash_clear_observation",
    question_label="QUESTION 16 · Evaluate the clearer prompt",
    response_label="Did the explicit target remove the logic flaw? What changed?",
    reveal_html={panel(
        "KEY TIP",
        "A well-keyed prompt with an explicit target and outcome can improve "
        "response quality without switching to a larger model or activating "
        "higher reasoning.",
        "success",
    )!r},
)''',
            "interactive",
        ),
        markdown(
            f"""
{panel(
    "EXPERIMENT 5",
    "<b>Repair a broken HTML animation.</b> Set Copilot Chat to <b>Ask</b> mode "
    "and choose the <b>Auto</b> model. Run the next cell, then write your own "
    "question to the LLM agent about the error. Apply the suggested fix and "
    "rerun the cell.<br><br><b>Pro-tip:</b> add <i>Give me the smallest change "
    "I can do to fix it.</i> to your prompt.",
    "task",
)}
"""
        ),
        code(
            '''# A notebook-native disco scene (no desktop window needed).
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
<div class="disco-scene">
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
.disco-scene {{ position:relative; height:260px; overflow:hidden; border-radius:16px;
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
    "EXPERIMENT CHECKPOINT",
    "<ul style='margin:0;padding-left:20px'>"
    "<li>separate text-first models from vision or multimodal models;</li>"
    "<li>expect probabilistic wording while checking semantic meaning;</li>"
    "<li>distinguish translation from interpretation;</li>"
    "<li>check hidden assumptions before accepting a confident answer;</li>"
    "<li>make the target explicit before paying for more reasoning;</li>"
    "<li>use a short run–repair–rerun troubleshooting loop;</li>"
    "<li>find saved work in <b>tasks/workbook_answers.json</b>.</li></ul>"
    "<p style='margin:10px 0 0'><b>Always know where your output is going "
    "and where to find it.</b></p>",
    "success",
)}
"""
        ),
        markdown(
            f"""
## Main task — Build and refine a shopping catalogue

### The simple workflow

1. **Look** at the result you want to recreate.
2. **Describe** what should match.
3. **Ask** an AI helper for the smallest useful next step.
4. **Make** or change a file.
5. **Open** the result and compare it with the target.
6. **Refine** one thing at a time.

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
<tr><td><b>Output</b></td><td>One file that you create yourself: <code>outputs/notebook1/catalogue.html</code>.</td></tr>
<tr><td><b>Target</b></td><td>You need to build a simple shopping catalogue of the items listed in the <code>*.csv</code> file. The catalogue should be neat and organised and should display information that would be relevant to potential consumers. Inspect the CSV file to learn what information it contains.</td></tr>
</table>

**CSV** means comma-separated values: a plain-text table where each row is one record and each column is one kind of information.

**HTML** is the file type used to structure a webpage that a browser can open and display.

{panel(
    "CONTROLLED MESSY DATA",
    "The product rows are deliberately mixed rather than grouped into a useful "
    "shopping order. The CSV also contains <b>two controlled data-quality "
    "problems</b>. Build the first version from what is present; the first "
    "follow-up iteration will inspect and repair the source data.",
    "task",
)}

### Round 1 requirements

Copy this first-round specification into your Copilot message, then add any visual choices you want.
"""
        ),
        code(
            '''copyable_prompt(
    """ROUND 1 REQUIREMENTS

- Load ../../data/notebook1/products.csv in the browser.
- Map every CSV image filename to ../../data/notebook1/<filename>.
- Create one catalogue entry per CSV row instead of hard-coding 18 products.
- Choose and show information that is relevant to a potential consumer.
- Use equal square image areas and consistent entry heights.
- Format every price with two decimal places.
- Use plain HTML, CSS and JavaScript with no framework or package installation.
- Show a friendly message if the CSV cannot be loaded.
- Keep a product visible and show an appropriate message or icon if its image is missing.
- Return one complete HTML document in chat; do not create or edit the file for me.

Do not prematurely read the notebook requirements and go beyond what is requested in this prompt."""
)''',
            "interactive",
        ),
        markdown(
            f"""
{catalogue_preview()}

The preview above is deliberately compact and follows the intentionally mixed
CSV row order. It is an inventory glance, not the organised shopping-card
layout you are asking Copilot to build.

### 2 · Write the first prompt and build

{panel(
    "ONE-TIME SETUP · INSTALL LIVE SERVER",
    "An <b>extension</b> is a small add-on that gives VS Code an extra "
    "ability.<ol style='margin:8px 0 0;padding-left:22px'>"
    "<li>Open <b>Extensions</b> from the left sidebar, or press "
    "<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>X</kbd> on Windows/Linux "
    "or <kbd>Command</kbd> + <kbd>Shift</kbd> + <kbd>X</kbd> on macOS.</li>"
    "<li>Search for <b>Live Server</b>.</li>"
    "<li>Select <b>Live Server</b> by <b>Ritwick Dey</b> and click "
    "<b>Install</b>. If the button says Disable or Uninstall, it is already "
    "ready.</li></ol>",
    "info",
)}

1. Close the vision experiment conversation, then open a fresh **GitHub Copilot Chat**.
2. In the Chat box, change the mode to **Ask** and change the model to **Auto**.
3. In the Explorer, open `data/notebook1/products.csv`. Inspect its columns, image filenames and deliberately mixed ID order.
4. Explain the **data**, **output**, **target** and paste the copyable Round 1 requirements. Tell Copilot to return one complete HTML document in chat rather than editing files.
5. Read its short plan. If it misunderstood a path or requirement, correct the instruction before accepting code.
6. In the Explorer, create `outputs/notebook1/catalogue.html`, paste the returned HTML code into that file, and save it.
7. Open `catalogue.html` in the editor. Right-click inside the editor and choose **Open with Live Server**.
8. If that menu is missing, open the Command Palette and run **Live Server: Open With Live Server**. Codespaces will open or offer a forwarded browser tab. Keep Live Server running while you test changes.

Do not open the HTML as a plain `file://` page: serving it with Live Server allows its JavaScript to load the CSV.

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
    "catalogue_brief_prompt",
    question_label="QUESTION 17 · Write the first Copilot instruction",
    response_label="Write the instruction you will send to GitHub Copilot:",
    response_height="150px",
)''',
            "interactive",
        ),
        code(
            '''worksheet_box(
    "catalogue_brief_mismatch",
    question_label="QUESTION 18 · Inspect the first catalogue",
    response_label="After opening the first version, what is its most important mismatch?",
)''',
            "interactive",
        ),
        markdown(
            f"""
### 3 · First iteration: inspect and repair the data

{panel(
    "DATA REPAIR BEFORE REDESIGN",
    "Do not solve a source-data problem only with prettier HTML. Before changing "
    "layout or sorting, find the two controlled defects in the CSV, repair the "
    "source rows, then reload the catalogue.",
    "task",
)}

1. Open `data/notebook1/products.csv` and compare each product row with the 11-column header.
2. Ask Copilot in **Ask** mode to inspect that file and **report suspicious rows and evidence only**. It should not edit the file for you.
3. Check every image filename against the files in `data/notebook1/`. Also look for a row whose separators no longer line up with the header.
4. Correct only the two source-data problems in `products.csv`, save it, and reload the Live Server page.
5. Confirm that all 18 records now have complete fields and valid images before requesting a new display order.

<details style='background:#FFFAEB;border:1px solid #FEDF89;border-radius:10px;padding:12px'>
<summary><b>Hint: what should the inspection count?</b></summary>

The header defines **11 fields**. A healthy row therefore needs the same field structure. Missing commas can merge several values into one unusually long field and leave later fields empty. For images, compare the CSV filename character-for-character with the actual files in the folder.

</details>

### 4 · Inspect before asking again

Check the evidence after the data repair:

- Do all 18 rows have 11 complete fields and become 18 catalogue entries?
- Do all 18 image filenames now point to real files?
- Does the page show useful consumer information without displaying every CSV field?
- Is the current row order useful to a shopper, or merely the messy source order?
- What exact primary and secondary order would make the catalogue easier to browse?

### 5 · Reiterate one change at a time

Use the same chat so Copilot has the current code, but make each request small.
You may ask for one complete revised HTML document or the exact section to
replace; you still make the edit in `catalogue.html` yourself.

1. **Visibility round:** add a **More details** control. It may reveal colour,
   release date, sizes, country of origin and designer, but those fields should
   remain hidden when the page first opens.
2. **Sorting round:** name the exact default order you want—for example, type
   then product name, newest release first, or price low-to-high. Ask for the
   primary and secondary sort explicitly; do not assume numerical ID order is
   useful simply because it is easy for code to produce.
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
        markdown(
            f"""
### Final catalogue check

- [ ] After repair, all 18 CSV rows have 11 complete fields and become 18 catalogue entries.
- [ ] All 18 image paths work, while the HTML still contains a useful missing-image fallback.
- [ ] Each entry shows information that is relevant to a potential consumer.
- [ ] Optional metadata is hidden when the page first opens.
- [ ] A deliberate control can reveal the optional details chosen as useful.
- [ ] The catalogue opens in the consumer-friendly order you specified.
- [ ] Sort controls offer the useful alternatives you requested and use sensible tie-breakers.
- [ ] Irrelevant fields remain hidden, and you can explain that choice.
- [ ] The layout is neat, with no clipped text or sideways scrolling.
- [ ] The result is saved at `outputs/notebook1/catalogue.html`.

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
    "<b>outputs/notebook1/catalogue.html</b>.",
    "success",
)}
"""
        ),
    ]

    return cells


SETUP = '''from pathlib import Path
import sys
import random

# Works when the kernel starts at the repository root or in notebooks/.
WORKSHOP_ROOT = next(
    folder for folder in (Path.cwd(), *Path.cwd().parents)
    if (folder / "llm_workshop" / "worksheet.py").is_file()
)
if str(WORKSHOP_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSHOP_ROOT))

from IPython.display import HTML, display
from llm_workshop.prompt_card import copyable_prompt
from llm_workshop.quiz import readme_quiz
from llm_workshop.worksheet import worksheet_box
from llm_workshop.course import answer_path
'''


def build_workbooks():
    """Split at explicit lesson boundaries; preserve the global question IDs."""
    cells = build_lesson_cells()
    markers = (
        "## Try the AI interface · HuggingChat",
        "<b>Vision inside VS Code.</b>",
        "<b>Repair a broken HTML animation.</b>",
        "## Main task — Build and refine a shopping catalogue",
    )
    boundaries = [0] + [next(
        index for index, cell in enumerate(cells)
        if cell.cell_type == "markdown" and marker in cell.source
    ) for marker in markers] + [len(cells)]
    books = {}
    for index, (stem, title, questions) in enumerate(WORKBOOKS):
        question_text = (f"Questions {questions[0]}–{questions[1]}" if questions
                         else "Hands-on repair · no written submission")
        destination = (f"Submit & save writes to **tasks/{stem}/answers.json**."
                       if questions else
                       "Your result is the repaired cell and its animation. Save this notebook to keep your edit.")
        heading = markdown(readable_html(
            f"# Workbook {index + 1} · {title}\n\n{question_text}\n\n"
            + panel("START HERE", "Select the <b>.venv</b> Python kernel. "
                    "Run the setup cell below with <b>Shift + Enter</b> or its "
                    "<b>▶ play button</b>, then run each activity cell in order. "
                    "The setup code can stay collapsed. If a button does not respond "
                    "after reopening or restarting, rerun setup and that question's cell.")
            + "\n\n" + destination + "\n\n"
            "These files stay in your own Codespace unless you choose to share them. "
            "Use your own accounts and API keys for external AI services."
        ))
        section = [heading, code(SETUP, "setup", "hide-input")]
        for cell in deepcopy(cells[boundaries[index]:boundaries[index + 1]]):
            if "setup" in cell.metadata.get("tags", []):
                continue
            if cell.source.startswith("# Vibe Coding Workshop — Start Here"):
                continue  # Replaced by the standalone workbook header.
            cell.source = cell.source.replace(
                "tasks/workbook_answers.json", f"tasks/{stem}/answers.json"
            ).replace(
                "tasks → workbook_answers.json", f"tasks → {stem} → answers.json"
            ).replace("outputs/notebook1/", "outputs/05_shopping_catalogue/")
            if stem == "05_shopping_catalogue":
                cell.source = cell.source.replace("NOTEBOOK 1 · MAIN", "WORKBOOK 5 · MAIN")
            if cell.cell_type == "code" and "worksheet_box(" in cell.source:
                # Explicit per-call paths also prevent cross-talk if notebooks share a kernel.
                cell.source = cell.source.replace(
                    "    question_label=", f"    answers_path=answer_path({stem!r}),\n    question_label=", 1)
            if cell.cell_type == "markdown":
                cell.source = readable_html(cell.source)
            section.append(cell)
        if index < len(WORKBOOKS) - 1:
            next_stem, next_title, _ = WORKBOOKS[index + 1]
            section.append(markdown(readable_html(
                f"## A good stopping point\n\nSave your work before moving on. "
                f"Next: [Workbook {index + 2} · {next_title}]({next_stem}.ipynb)."
            )))
        notebook = nbf.v4.new_notebook(cells=section)
        notebook.metadata.kernelspec = {
            "display_name": "Python (.venv)", "language": "python", "name": "llm-workshop",
        }
        notebook.metadata.language_info = {"name": "python", "version": "3.12"}
        notebook.metadata.workshop = {"id": stem, "questions": questions}
        books[stem] = notebook
    return books


def main() -> None:
    for stem, notebook in build_workbooks().items():
        path = ROOT / "notebooks" / f"{stem}.ipynb"
        nbf.write(notebook, path)
        print(f"Built {path.relative_to(ROOT)} with {len(notebook.cells)} cells")


if __name__ == "__main__":
    main()
