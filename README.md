# Vibe Coding Workshop

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/highfield09/AI_workshop)

A beginner-friendly workshop for learning how to reproduce a clear output with help from an AI interface. The emphasis is on finding files, describing a target, making a small change, opening the result, and refining it—not on memorizing technical syntax.

## Start here

1. Open the repository in GitHub Codespaces.
2. Wait for the development container to finish rebuilding.
3. Open [Workbook 1](notebooks/01_start_here.ipynb).
4. Select the Python kernel marked **.venv** (for example, **Python 3.12 (.venv)**) if VS Code asks for one.
5. Run the setup cell at the top with **Shift + Enter** or its **▶ play button**, then run each activity cell in order. Each workbook has its own setup; you can reopen it independently.

If a question is visible but its button does not respond after reopening or restarting the kernel, rerun the setup cell and that question's cell. Saved answers will reload.

### Do learners need Python on their laptops?

No, not when they use GitHub Codespaces. Python, Jupyter, the extensions, and all course packages run inside the online Codespace.

If the notebook asks for a kernel, choose the Python interpreter marked **.venv**. Codespaces users do not need to install Python locally.

## Five short workbooks

| Workbook | Focus | Questions / result |
|---|---|---|
| [1 · Start here](notebooks/01_start_here.ipynb) | Workspace, prompting, tokens and Google AI Mode | Q1–Q4 |
| [2 · Models and reasoning](notebooks/02_models_and_reasoning.ipynb) | HuggingChat model cards, translation and source checking | Q5–Q9 |
| [3 · Vision and context](notebooks/03_vision_and_context.ipynb) | Vision in Copilot, request costs and Gemini effort comparisons | Q10–Q16 |
| [4 · Debugging](notebooks/04_debugging.ipynb) | Ask for a small repair, rerun and inspect | Repaired cell and animation |
| [5 · Shopping catalogue](notebooks/05_shopping_catalogue.ipynb) | Build HTML from messy CSV data; repair, sort and refine | Q17–Q18 and your catalogue |

Open [KEY_CONCEPTS.md](KEY_CONCEPTS.md) for the growing student take-home reference.

## Your work belongs to your Codespace

Each student should open their **own Codespace** and use their own AI accounts and keys. Separate Codespaces have separate filesystems: saving an answer or repairing the CSV in yours does not change another student's copy or the shared repository. [GitHub explains Codespaces isolation here](https://docs.github.com/en/codespaces/reference/security-in-github-codespaces).

Each **Submit & save** button writes to `tasks/<workbook-name>/answers.json`, for example `tasks/02_models_and_reasoning/answers.json`. Files appear on the first save; answers reload when you rerun the question. Q1 and Q2 are quick self-checks, not saved responses. Workbook 4 has no written-answer form: save its notebook to preserve your repaired code.

Create the catalogue at `outputs/05_shopping_catalogue/catalogue.html`. Answer JSON and generated HTML are Git-ignored. Previously created `tasks/workbook_answers.json` and `outputs/notebook1/` files stay where they are; they are not deleted or automatically merged into the new workbooks.

Saving is not the same as publishing. Do not push personal responses, keys, or notebook outputs to the shared course repository. A notebook you save can contain your answers in its widget state even though the separate JSON is ignored. Shared Codespaces/Live Share sessions and deliberately shared files are not private per student. Requests sent to AI services are handled by those services, not kept only inside the Codespace.

Download a copy of work you want to retain before deleting your Codespace; creating a new Codespace does not copy uncommitted work from the old one.

## Workshop folders

| Folder | What belongs there |
|---|---|
| notebooks/ | Course lessons |
| tasks/ | Separate saved-answer folder for each workbook |
| data/ | Small course input files |
| outputs/ | Viewers, reports and catalogue files you create |
| Resources/ | Optional student reading and reports |
| scripts/ | Reusable instructions and course checks |

The older deployment material remains in the repository for reference but is hidden from the default VS Code Explorer view.

The Codespace also installs GitHub Copilot Chat and Live Server by Ritwick Dey. Copilot access depends on the GitHub account signed into VS Code.

## Course design rule

Each sandbox should give learners one clear target, tiny isolated inputs, a starting prompt, an obvious way to open or run the result, and a short comparison checklist.

Secrets belong in Codespaces secrets or a local .env file. The .env file is Git-ignored and must never be committed.
