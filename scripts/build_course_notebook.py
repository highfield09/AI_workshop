"""Build the learner-facing onboarding notebook from readable cell sources."""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "01_start_here.ipynb"
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
    if tags:
        cell.metadata["tags"] = list(tags)
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

**Friendly setup · 20–30 minutes · No coding experience required**

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
"""
        ),
        markdown(
            f"""
### Give the AI a result, not a vague instruction

{panel(
    "TASK",
    "For every sandbox, begin by showing or describing the target. Copy "
    "the prompt from the box below and replace the bracketed text.",
    "task",
)}
"""
        ),
        code(
            '''from llm_workshop.prompt_card import copyable_prompt

copyable_prompt(
    """I want to reproduce the attached example.

The result must:
- [describe what should visibly match]
- use the files inside [task folder]
- stay simple enough for a beginner to edit

Before writing code, ask me up to three short questions.
Then suggest the smallest file plan and help me build one step at a time."""
)''',
            "interactive",
        ),
        markdown(
            f"""
Replace the bracketed text. Attach only course files that are safe to share.

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

Before asking an AI to create anything, what should you provide first?

<details>
<summary>Show the suggested answer</summary>

Provide the target result—or a clear description of what the finished output must look like and do.

</details>

{panel(
    "STAGE 2 CHECKPOINT",
    "Provide the target result—or a clear description of what the finished "
    "output must look like and do. Check the model card, then ask in a "
    "clear and token-efficient way.",
    "success",
)}
"""
        ),
        markdown(
            f"""
## Stage 3 — Ask, compare, and question

{panel(
    "IMPORTANT",
    "Stage 3 uses <a href='https://huggingface.co/chat/'>HuggingChat</a>, "
    "a single interface that lets you chat with different available open "
    "models.",
    "info",
)}

LLMs are <a href='https://huggingface.co/docs/transformers/generation_strategies' title='Probabilistic means the model chooses among likely next pieces of text; the same request can produce different wording.' style='text-decoration:underline dotted;cursor:help'><b>probabilistic</b></a>. In simple words, they choose from several likely next pieces of text rather than retrieving one fixed sentence. Two runs may therefore use different wording or detail. Ideally, the answers should remain **semantically similar**—their central meaning should agree—even when their phrasing varies.
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

The growing workshop reference is in [**KEY_CONCEPTS.md**](../KEY_CONCEPTS.md) at the repository root. Students can open it in the Explorer and save a copy after the workshop.
"""
        ),
        code(
            """
from llm_workshop.worksheet import model_comparison_box, worksheet_box
"""
        ),
        markdown(
            f"""
{panel(
    "EXPERIMENT 1",
    "<b>A simple factual request.</b> Choose one named text model, copy the "
    "prompt below, and save its answer and your observation.",
    "task",
)}
"""
        ),
        code(
            '''from llm_workshop.prompt_card import copyable_prompt

copyable_prompt(
    """What are three things a plant needs to grow?
Answer in one clear sentence for a 10-year-old."""
)''',
            "interactive",
        ),
        code(
            """
worksheet_box(
    "simple_fact",
    answer_label="Paste the model's answer:",
    observation_label="Was the answer clear and brief?",
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
    "<b>The nearby car-wash test.</b> This is a quick common-sense logic "
    "check. Ask one named model; there is nothing to submit here.",
    "task",
)}
"""
        ),
        code(
            '''from llm_workshop.prompt_card import copyable_prompt

copyable_prompt(
    """My car is dirty and needs to be washed. The car wash is only 100 metres from my home. Should I walk there or drive?

Answer in one sentence, then add one light joke."""
)''',
            "interactive",
        ),
        markdown(
            f"""
<details style='background:#EFF8FF;border:1px solid #B2DDFF;border-radius:10px;padding:12px'>
<summary><b>Reveal the funny logic fact after asking the model</b></summary>

The useful answer is to **drive the dirty car**, because the car itself must reach the car wash. Older language models sometimes focused on “100 metres is close” and recommended walking, while missing the goal of the trip.

This is better described as a **context and common-sense reasoning** failure than purely an induction or deduction flaw. An LLM can also detect a humorous cue and generate a joke because it has learned language patterns. Modern models usually handle this small trap, but complex multi-step logic and hidden assumptions can still be difficult—so keep checking the reasoning.

</details>

{panel(
    "EXPERIMENT 4",
    "<b>Repair a broken disco script.</b> Run the next cell as written. It "
    "contains one small naming bug and is expected to show a red error.",
    "task",
)}

The HTML and animation code may look complicated; that is intentional. You do not need to understand every line. Read the **final line** of the error first.
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
{panel(
    "TROUBLESHOOTING LOOP",
    "<ol style='margin:0;padding-left:20px'>"
    "<li>Copy the broken code and its red traceback into an LLM.</li>"
    "<li>Ask for either the whole corrected block or only the exact line "
    "to replace—your choice.</li><li>Edit the broken cell manually or paste "
    "the corrected version.</li><li>Run that same cell again. A moving ASCII "
    "dancer on a neon disco floor is your reward when the repair works.</li>"
    "</ol>",
    "task",
)}
"""
        ),
        code(
            '''from llm_workshop.prompt_card import copyable_prompt

copyable_prompt(
    """I am a beginner. This Python notebook cell failed.

[PASTE THE BROKEN CODE HERE]

[PASTE THE RED ERROR / TRACEBACK HERE]

Explain the cause in plain language. Then let me choose between:
1. the full corrected code block; or
2. only the exact broken line and its replacement.

Do not change unrelated parts. Keep the answer short."""
)''',
            "interactive",
        ),
        markdown(
            f"""
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
    "FINAL REFLECTION",
    "Which task did AI handle most confidently? Where did model size, "
    "wording, logic, or technical complexity change the usefulness of its "
    "answer? Submit one short reflection.",
    "task",
)}
"""
        ),
        code(
            """
worksheet_box(
    "stage3_comparison",
    answer_label="Which response or repair was strongest?",
    observation_label="What would you ask differently next time, and where was your output saved?",
)
""",
            "interactive",
        ),
        markdown(
            f"""
{panel(
    "STAGE 3 CHECKPOINT",
    "<ul style='margin:0;padding-left:20px'>"
    "<li>separate text-first models from vision or multimodal models;</li>"
    "<li>expect probabilistic wording while checking semantic meaning;</li>"
    "<li>distinguish translation from interpretation;</li>"
    "<li>check common-sense logic before accepting a confident answer;</li>"
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
## Next — Six vibe-coding sandboxes

{panel(
    "COMING NEXT",
    "The next course iteration will add six isolated task folders. Each "
    "task will have one clear target, tiny inputs, a starting prompt, an "
    "obvious way to run the result, and a comparison checklist.",
    "task",
)}

- one clear target to copy, mimic, or reproduce;
- a tiny input file or reference;
- a friendly starting prompt;
- one obvious way to open or run the result;
- a short “does it match?” checklist.

The tasks will focus on visible HTML viewers and small scripts that trigger useful analysis on simple local data—not on API plumbing.
"""
        ),
        markdown(
            f"""
## Orientation complete

{panel(
    "READY",
    "You are ready when you can find the course folders, open one AI "
    "helper, and describe a target before asking for code.<br><br>"
    "<b>Next action:</b> wait for the instructor to introduce Sandbox "
    "Task 1.",
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
