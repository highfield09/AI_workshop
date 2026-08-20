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
        "font-weight:700;letter-spacing:0.04em;white-space:nowrap'>"
        f"{label}</span>"
    )


def panel(label: str, body: str, tone: str = "info") -> str:
    colors = PALETTES[tone]
    return (
        f"<div style='background:{colors['background']};"
        f"border:1px solid {colors['border']};border-left:5px solid "
        f"{colors['accent']};border-radius:12px;padding:15px 17px;"
        "margin:12px 0;color:#344054;line-height:1.55'>"
        f"{chip(label, tone)}"
        f"<div style='margin-top:9px'>{body}</div></div>"
    )


def main() -> None:
    cells = [
        markdown(
            f"""
# Vibe Coding Workshop — Start Here

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
    "overflow:auto'>AI_workshop/\n"
    "├── notebooks/   ← lessons like this one\n"
    "├── tasks/       ← one isolated folder for each challenge\n"
    "├── data/        ← small input files supplied by the course\n"
    "├── outputs/     ← viewers, reports, and other results you create\n"
    "├── scripts/     ← reusable instructions that run a task\n"
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
### Give the AI a result, not a vague instruction

{panel(
    "TASK",
    "For every sandbox, begin by showing or describing the target. Copy "
    "the lightweight prompt below and replace the bracketed text.",
    "task",
)}

~~~text
I want to reproduce the attached example.

The result must:
- [describe what should visibly match]
- use the files inside [task folder]
- stay simple enough for a beginner to edit

Before writing code, ask me up to three short questions.
Then suggest the smallest file plan and help me build one step at a time.
~~~

Replace the bracketed text. Attach only course files that are safe to share.
"""
        ),
        markdown(
            f"""
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
    "output must look like and do.",
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

HuggingChat may begin with **Omni**, which automatically routes a request to a model. For this comparison, choose named models directly:

1. open [HuggingChat Models](https://huggingface.co/chat/models);
2. choose any available named model and start a fresh chat;
3. run the prompt and record the model name and answer as **Model A**;
4. choose a different named model, start another fresh chat, and run the identical prompt;
5. record it as **Model B**, compare the responses, and press **Save comparison**.

Use the same prompt without correcting either model midway. Availability changes, so use models shown in the interface rather than looking for a particular name.

{panel(
    "YOUR WORKSHEET",
    "Answers are saved locally as <b>tasks/stage3_answers.json</b>. The "
    "file is ignored by Git, so personal answers are not committed.",
    "info",
)}
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
    "<b>A simple factual request.</b> Copy the exact prompt into two named "
    "HuggingChat models and compare their answers.",
    "task",
)}

~~~text
What are three things a plant needs to grow?
Answer in one clear sentence for a 10-year-old.
~~~

Look for a direct answer, simple wording, and no unnecessary detail.
"""
        ),
        code(
            """
model_comparison_box(
    "simple_fact",
    observation_label="Was the answer clear and brief?",
)
""",
            "interactive",
        ),
        markdown(
            f"""
{panel(
    "EXPERIMENT 2",
    "<b>Translate a short Sanskrit sentence.</b> Run the exact same text "
    "through two named models.",
    "task",
)}

~~~text
Translate this Sanskrit sentence into clear English.
Then explain its meaning in one short sentence:

विद्या ददाति विनयम्।
~~~

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
    observation_label="Did it separate translation and meaning?",
)
""",
            "interactive",
        ),
        markdown(
            f"""
{panel(
    "EXPERIMENT 3",
    "<b>Logic with a silly voice.</b> Check correctness before comparing "
    "how playful each model becomes.",
    "task",
)}

~~~text
A farmer has 17 sheep. All but 9 run away.
How many sheep remain?

Give the correct answer first, then explain it like a pirate.
~~~

{panel(
    "CHECKPOINT",
    "The logic answer is <b>9</b>. Observe whether each model gets the "
    "logic right before becoming playful.",
    "success",
)}
"""
        ),
        code(
            """
model_comparison_box(
    "funny_logic",
    observation_label="Was it correct, serious, silly—or all three?",
)
""",
            "interactive",
        ),
        markdown(
            f"""
{panel(
    "EXPERIMENT 4",
    "<b>Make an intimidating error understandable.</b> Copy the whole "
    "prompt into both models without changing the trace.",
    "task",
)}

~~~text
I am a beginner. Explain this error in plain language.
Tell me the most likely causes, give me three safe checks,
and recommend the next step. Do not invent columns that
are not shown.

Traceback (most recent call last):
  File "/workspaces/task4/analyse.py", line 28, in <module>
    summary = sales.groupby("region")["revenue"].mean()
  File ".../pandas/core/frame.py", line 9190, in groupby
    return DataFrameGroupBy(...)
  File ".../pandas/core/groupby/grouper.py", line 1043, in get_grouper
    raise KeyError(gpr)
KeyError: 'region'
~~~

{panel(
    "CHECKPOINT",
    "A useful answer explains that the table does not contain a column "
    "named exactly <b>region</b> at that moment, then suggests checking "
    "column names, spelling, spaces, and the loaded file.",
    "success",
)}
"""
        ),
        code(
            """
model_comparison_box(
    "error_explanation",
    observation_label="Did it explain a safe next step?",
)
""",
            "interactive",
        ),
        markdown(
            f"""
{panel(
    "FINAL COMPARISON",
    "Compare the four responses. Which task did the AI handle most "
    "confidently? Where did tone, ambiguity, or technical complexity "
    "change the quality of its answer?",
    "task",
)}
"""
        ),
        code(
            """
worksheet_box(
    "stage3_comparison",
    answer_label="Which response was strongest?",
    observation_label="What would you ask differently next time?",
)
""",
            "interactive",
        ),
        markdown(
            f"""
{panel(
    "STAGE 3 CHECKPOINT",
    "<ul style='margin:0;padding-left:20px'>"
    "<li>ask for a simple format and audience;</li>"
    "<li>distinguish translation from interpretation;</li>"
    "<li>check logic before accepting a confident answer;</li>"
    "<li>ask for plain-language explanations and safe next steps;</li>"
    "<li>question, compare, and refine an AI response.</li></ul>"
    "<p style='margin:10px 0 0'>AI can help with questions and answers, "
    "but you still decide whether the result is useful and trustworthy.</p>",
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
