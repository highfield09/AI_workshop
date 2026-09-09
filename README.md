# Vibe Coding Workshop

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/highfield09/AI_workshop)

A beginner-friendly workshop for learning how to reproduce a clear output with help from an AI interface. The emphasis is on finding files, describing a target, making a small change, opening the result, and refining it—not on memorizing technical syntax.

## Start here

1. Open the repository in GitHub Codespaces.
2. Wait for the development container to finish rebuilding.
3. Open [Workbook 1](_for_STUDENT/notebooks/01_start_here.ipynb).
4. Select the Python kernel marked **.venv** (for example, **Python 3.12 (.venv)**) if VS Code asks for one.
5. Run the setup cell at the top with **Shift + Enter** or its **▶ play button**, then run each activity cell in order. Each workbook has its own setup; you can reopen it independently.

If a question is visible but its button does not respond after reopening or restarting the kernel, rerun the setup cell and that question's cell. Saved answers will reload.

### Do learners need Python on their laptops?

No, not when they use GitHub Codespaces. Python, Jupyter, the extensions, and all course packages run inside the online Codespace.

If the notebook asks for a kernel, choose the Python interpreter marked **.venv**. Codespaces users do not need to install Python locally.

## Six short workbooks

| Workbook | Focus | Questions / result |
|---|---|---|
| [1 · Start here](_for_STUDENT/notebooks/01_start_here.ipynb) | Workspace, prompting, tokens and Google AI Mode | Q1–Q4 |
| [2 · Models and reasoning](_for_STUDENT/notebooks/02_models_and_reasoning.ipynb) | HuggingChat model cards, translation and source checking | Q5–Q9 |
| [3 · Vision and context](_for_STUDENT/notebooks/03_vision_and_context.ipynb) | Vision in Copilot, request costs and Gemini effort comparisons | Q10–Q15 |
| [4 · Debugging](_for_STUDENT/notebooks/04_debugging.ipynb) | Repair manually in Ask mode, then review an Agent edit | Two repaired cells and animations |
| [5 · Shopping catalogue](_for_STUDENT/notebooks/05_shopping_catalogue.ipynb) | Build HTML from messy CSV data; repair, sort and refine | Q16 and your catalogue |
| [6 · Receipt OCR](_for_STUDENT/notebooks/06_receipt_ocr.ipynb) | Full text → checked item tables → 5 receipts → chart | Q17–Q22, spreadsheets and chart |

Open [KEY_CONCEPTS.md](_for_STUDENT/KEY_CONCEPTS.md) for the growing student take-home reference.

Workbooks 1–4 and 6 finish with a four-question interactive mini quiz. Click
**Submit quiz** for explanations, then retry as needed. These practice choices
are not saved to worksheet JSON files; rerun the quiz cell after a restart.
Workbook 5 has no mini quiz. For Workbook 3, put your chosen image in
`_for_STUDENT/data/notebook3/`; learner images are Git-ignored.

### Workbook 6 · One-time preparation

Use a **16 GB RAM environment** for this workbook. GLM-OCR is a local
vision-language model that returns document fields, not just unstructured OCR
text. Its optional runtime is installed only when you start Workbook 6:

```bash
./_for_TRAINER/scripts/setup_environment.sh
source .venv/bin/activate
sh _for_TRAINER/scripts/setup_glm_ocr.sh
python _for_TRAINER/scripts/prepare_receipt_data.py
```

The data download is about **101 MB**. The pinned [GLM-OCR snapshot](https://huggingface.co/zai-org/GLM-OCR)
is about **2.66 GB**, stored at `_for_STUDENT/tasks/06_receipt_ocr/model/glm-ocr/`.
Both downloads are Git-ignored and stay in your own Codespace. Allow at least
**6 GB spare disk** for model and runtime, plus possible package-cache space.
Model provenance and SHA-256 hashes are committed; the large weights are not.
Inference needs no API key or GPU and runs locally after installation. Our
four-thread CPU sample took about 47 seconds and peaked at 6.6 GiB RAM; hardware
and prompts affect results. An 8 GB default Codespace may not have enough
headroom. The notebook documents setup and cites the model and Kaggle uploader.

Use your coding agent to build `_for_STUDENT/tasks/06_receipt_ocr/receipt_reader.py`
in four iterations. First transcribe the whole `batch1-0001.jpg` image into
`raw/batch1-0001.txt`, then create `first_receipt.xlsx` with separate **Items**
and **Receipts** sheets. Next process the first 5 filenames into `receipts_5.xlsx`
and `batch_run.csv`. Finally save `item_quantity_summary.csv` and
`item_quantities.png`. All outputs go under `_for_STUDENT/outputs/06_receipt_ocr/`.
The supplied documents are JPGs, not PDFs; PDF conversion is not part of this lesson.
Allow roughly 10–15 minutes for five similar uncached receipts; reuse saved text
when refining Excel or charts. The model helper supports longer full-text responses
and reuses one loaded model sequentially. Matplotlib is included in the optional
Workbook 6 setup. This is a student exercise, so a completed pipeline is not supplied.

To view Excel files, install **SpreadJS XLSX Editor** by **MESCIUS** from Extensions, or use Workbook 6's built-in read-only spreadsheet preview. The script, spreadsheet, raw model response and written answers are Git-ignored. No Microsoft Excel installation is needed.

## Your work belongs to your Codespace

Each student should open their **own Codespace** and use their own AI accounts and keys. Separate Codespaces have separate filesystems: saving an answer or repairing the CSV in yours does not change another student's copy or the shared repository. [GitHub explains Codespaces isolation here](https://docs.github.com/en/codespaces/reference/security-in-github-codespaces).

Each **Submit & save** button writes to `_for_STUDENT/tasks/<workbook-name>/answers.json`, for example `_for_STUDENT/tasks/02_models_and_reasoning/answers.json`. Files appear on the first save; answers reload when you rerun the question. Q1 and Q2 are quick self-checks, not saved responses. Workbook 4 has no written-answer form: save its notebook to preserve your repaired code.

Create the catalogue at `_for_STUDENT/outputs/05_shopping_catalogue/catalogue.html`. Answer JSON and generated HTML are Git-ignored. Previously created `_for_STUDENT/tasks/workbook_answers.json` and `_for_STUDENT/outputs/notebook1/` files stay where they are; they are not deleted or automatically merged into the new workbooks.

Saving is not the same as publishing. Do not push personal responses, keys, or notebook outputs to the shared course repository. A notebook you save can contain your answers in its widget state even though the separate JSON is ignored. Shared Codespaces/Live Share sessions and deliberately shared files are not private per student. Requests sent to AI services are handled by those services, not kept only inside the Codespace.

Download a copy of work you want to retain before deleting your Codespace; creating a new Codespace does not copy uncommitted work from the old one.

## Workshop folders

Start in **_for_STUDENT**. The **_for_TRAINER** folder contains the code that
supports the notebooks; students may run the documented setup commands but do
not need to edit those support files. These labels describe purpose, not access
permissions. Both folders are distributed with the course; neither contains
private model-answer tools.

| Folder | What belongs there |
|---|---|
| _for_STUDENT/notebooks/ | Course lessons |
| _for_STUDENT/tasks/ | Separate saved-answer folder for each workbook |
| _for_STUDENT/data/ | Small course input files |
| _for_STUDENT/outputs/ | Viewers, reports and catalogue files you create |
| _for_STUDENT/Resources/ | Optional student reading and reports |
| _for_STUDENT/KEY_CONCEPTS.md | Student take-home reference |
| _for_TRAINER/scripts/ | Reusable instructions and course checks |
| _for_TRAINER/llm_workshop/ | Notebook widgets and output-saving support |
| _for_TRAINER/tests/ | Course maintenance checks, not student exercises |

The root README, requirements, Makefile and hidden VS Code/Codespaces settings
stay at the repository root because they configure the environment. Treat them
as trainer-maintained files, not exercise inputs.

**Updating an existing Codespace:** notebook paths now begin with
`_for_STUDENT/`. Reopen the notebooks there and select the `.venv` kernel.
Old Git-ignored work in `tasks/`, `outputs/` or `data/` is not automatically
migrated by Git. Keep it as a backup, or manually copy the files you want into
the corresponding `_for_STUDENT/` folder after checking for name conflicts.
Do not overwrite a new exercise input with a previously repaired copy unless
you intend to resume that exercise.

The older deployment material remains in the repository for reference but is hidden from the default VS Code Explorer view.

The Codespace also installs GitHub Copilot Chat and Live Server by Ritwick Dey. Copilot access depends on the GitHub account signed into VS Code.

## Course design rule

Each sandbox should give learners one clear target, tiny isolated inputs, a starting prompt, an obvious way to open or run the result, and a short comparison checklist.

Secrets belong in Codespaces secrets or a local .env file. The .env file is Git-ignored and must never be committed.
