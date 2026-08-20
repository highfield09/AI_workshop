"""Build the learner-facing onboarding notebook from readable cell sources."""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "01_start_here.ipynb"


def markdown(source: str):
    return nbf.v4.new_markdown_cell(source.strip())


def code(source: str, *tags: str):
    cell = nbf.v4.new_code_cell(source.strip())
    if tags:
        cell.metadata["tags"] = list(tags)
    return cell


def main() -> None:
    cells = [
        markdown(
            """
# Vibe Coding Workshop — Start Here

**Friendly setup · 20–30 minutes · No coding experience required**

This short notebook helps you get comfortable in VS Code, find the course files, and choose an AI helper. After this orientation, you will work through six small challenges where you reproduce a visible result.

> Run each cell from top to bottom. Nothing in Stages 1 or 2 sends data to an API.
"""
        ),
        markdown(
            """
### The simple workflow

1. **Look** at the result you want to recreate.
2. **Describe** what should match.
3. **Ask** an AI helper for the smallest useful next step.
4. **Make** or change a file.
5. **Open** the result and compare it with the target.
6. **Refine** one thing at a time.

You do not need to memorize commands. The aim is to learn where things live and how to ask for a clear outcome.
"""
        ),
        markdown(
            """
## Stage 1 — Find your way around

### Five friendly terms

| Term | What it means here |
|---|---|
| **Editor** | The main VS Code area where you open and change a file. |
| **Script** | A saved list of instructions that makes the computer do a repeatable task. |
| **Data type** | The shape of information, such as text, a number, a table, JSON, or CSV. |
| **Terminal** | The small command area where you can ask the computer to run something. |
| **Directory tree** | The folder-and-file map shown in the Explorer on the left. |

**Tip:** If you feel lost, return to the Explorer and look for the folder named in the task.
"""
        ),
        markdown(
            """
### Your workshop map

~~~text
AI_workshop/
├── notebooks/   ← lessons like this one
├── tasks/       ← one isolated folder for each challenge
├── data/        ← small input files supplied by the course
├── outputs/     ← viewers, reports, and other results you create
├── scripts/     ← reusable instructions that run a task
└── README.md    ← the project welcome page
~~~

Keep each challenge self-contained inside its own task folder. Put shared source files in **data/** and finished examples in **outputs/**.
"""
        ),
        markdown(
            """
### See where you are

Run the next cell. It reports your current folder and shows the top-level workshop items. This is a safe way to answer: “Where am I?” and “What files are here?”
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
            """
### Quick check

Choose an answer and press **Submit answer**. The notebook will tell you immediately whether you are correct.
"""
        ),
        code(
            """
import ipywidgets as widgets
from IPython.display import display

stage1_question = widgets.HTML(
    "<b>A task gives you a small CSV file that several exercises will use. "
    "Where should you keep it?</b>"
)
stage1_choices = widgets.RadioButtons(
    options=[
        ("In notebooks/", "notebooks"),
        ("In data/", "data"),
        ("Inside .git/", "git"),
    ],
    value=None,
)
stage1_submit = widgets.Button(description="Submit answer", button_style="primary")
stage1_feedback = widgets.HTML("<small>Choose one answer.</small>")

def check_stage1(_button):
    if stage1_choices.value == "data":
        stage1_feedback.value = (
            "<b style='color:#18794e'>Correct!</b> "
            "Shared source files belong in <b>data/</b>."
        )
        stage1_submit.button_style = "success"
    elif stage1_choices.value is None:
        stage1_feedback.value = "<b>Choose an answer first.</b>"
    else:
        stage1_feedback.value = (
            "<b style='color:#b42318'>Not quite.</b> "
            "Look at the workshop map and try again."
        )

stage1_submit.on_click(check_stage1)
display(widgets.VBox([
    stage1_question,
    stage1_choices,
    stage1_submit,
    stage1_feedback,
]))
""",
            "interactive",
        ),
        markdown(
            """
### Stage 1 complete when you can…

- find the **Explorer**, **editor**, and **terminal**;
- point to the **notebooks**, **tasks**, **data**, and **outputs** folders;
- explain the difference between an input file and something you created.

That is enough orientation to begin vibe coding.
"""
        ),
        markdown(
            """
## Stage 2 — Choose an AI helper

Use any interface available to you. These links open the official web experiences in a browser:

| AI interface | Open it |
|---|---|
| **ChatGPT** | [Open ChatGPT ↗](https://chatgpt.com/) |
| **Claude** | [Open Claude ↗](https://claude.ai/) |
| **Gemini** | [Open Gemini ↗](https://gemini.google.com/) |
| **HuggingChat** | [Open HuggingChat ↗](https://huggingface.co/chat/) |
| **Google AI Mode** | [Open Google AI Mode ↗](https://www.google.com/search?udm=50) |

Access can depend on your account, organization, or region. It is fine if the class uses a mixture of tools.
"""
        ),
        markdown(
            """
### Give the AI a result, not a vague instruction

For every sandbox, begin by showing or describing the target. Then use this lightweight prompt:

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
            """
### Your role while using AI

- **You choose the target.**
- **The AI proposes a step.**
- **You place files in the correct folder.**
- **You run or open the result.**
- **You compare and decide what changes next.**

If the answer becomes too technical, say: “Explain that in plain language and give me only the next action.”
"""
        ),
        markdown(
            """
### Stage 2 mini-check

Before asking an AI to create anything, what should you provide first?

<details>
<summary>Show the suggested answer</summary>

Provide the target result—or a clear description of what the finished output must look like and do.

</details>
"""
        ),
        markdown(
            """
## Stage 3 — Ask, compare, and question

Stage 3 uses [HuggingChat](https://huggingface.co/chat/), a single interface that lets you chat with different available open models.

HuggingChat may begin with **Omni**, which automatically routes a request to a model. For this comparison, choose named models directly:

1. open [HuggingChat Models](https://huggingface.co/chat/models);
2. choose any available named model and start a fresh chat;
3. run the prompt and record the model name and answer as **Model A**;
4. choose a different named model, start another fresh chat, and run the identical prompt;
5. record it as **Model B**, compare the responses, and press **Save comparison**.

Use the same prompt without correcting either model midway. Availability changes, so use models shown in the interface rather than looking for a particular name.

Your worksheet is saved locally as tasks/stage3_answers.json. It is ignored by Git, so personal answers are not committed.
"""
        ),
        code(
            """
from llm_workshop.worksheet import model_comparison_box, worksheet_box
"""
        ),
        markdown(
            """
### Experiment 1 — A simple factual request

Copy this prompt:

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
            """
### Experiment 2 — Translate a short Sanskrit sentence

Copy this prompt:

~~~text
Translate this Sanskrit sentence into clear English.
Then explain its meaning in one short sentence:

विद्या ददाति विनयम्।
~~~

The literal idea is **“Knowledge gives humility.”** Notice whether the AI separates translation from interpretation.
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
            """
### Experiment 3 — Logic with a silly voice

Copy this prompt:

~~~text
A farmer has 17 sheep. All but 9 run away.
How many sheep remain?

Give the correct answer first, then explain it like a pirate.
~~~

The logic answer is **9**. Observe whether the AI gets the logic right before becoming playful.
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
            """
### Experiment 4 — Make an intimidating error understandable

Copy the whole prompt:

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

A useful answer should explain that the table does not contain a column named exactly region at that moment, then suggest checking column names, spelling, spaces, and the loaded file.
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
            """
### Stage 3 comparison

Now compare the four responses. Which task did the AI handle most confidently? Where did tone, ambiguity, or technical complexity change the quality of its answer?
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
            """
### Stage 3 complete when you can…

- ask for a simple format and audience;
- distinguish translation from interpretation;
- check logic before accepting a confident answer;
- ask for plain-language explanations and safe next steps;
- question, compare, and refine an AI response.

AI can help with questions and answers, but you still decide whether the result is useful and trustworthy.
"""
        ),
        markdown(
            """
## Next — Six vibe-coding sandboxes

The next course iteration will add six isolated task folders. Each task will have:

- one clear target to copy, mimic, or reproduce;
- a tiny input file or reference;
- a friendly starting prompt;
- one obvious way to open or run the result;
- a short “does it match?” checklist.

The tasks will focus on visible HTML viewers and small scripts that trigger useful analysis on simple local data—not on API plumbing.
"""
        ),
        markdown(
            """
## Orientation complete

You are ready when you can find the course folders, open one AI helper, and describe a target before asking for code.

**Next action:** wait for the instructor to introduce Sandbox Task 1.
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
