# Vibe Coding Workshop — Master Key Concepts

This is the workshop's growing take-home reference. Open it from the VS Code Explorer at any time. You can keep it in your repository, download it from GitHub, or save your own copy after the workshop.

## Stage 1 — Know your workspace

**Key concept: know where files live before you run or change anything.**

- The Explorer shows the directory tree.
- `notebooks/` contains lessons.
- `tasks/` contains isolated challenges and learner worksheets.
- `data/` contains shared input files.
- `outputs/` contains results you create.
- `Resources/` contains optional student reading and reports.
- `scripts/` and Python modules contain reusable instructions.
- Run a notebook cell with the ▶ play button or `Shift + Enter`.

## Stage 2 — Choose deliberately

**Key concept: read the model card and choose a model that fits the input and task.**

Check three things:

1. **Description:** what the model was designed to do.
2. **Parameter size:** a rough indication of scale, such as 4B or 70B. More parameters do not guarantee a better answer.
3. **Multimodality:** whether it handles only text or can also inspect images or other inputs.

Use a six-point prompt check: set the objective, be clear, add only useful context, iterate, name the audience, and evaluate the result.

### Token efficiency

**Key concept: tokens are limited resources, so use them deliberately.**

- Tokens are pieces of content processed by a model.
- Your question, relevant chat history, and attachments use input tokens.
- The answer—and sometimes extra reasoning—uses output tokens.
- Services may limit tokens, messages, requests, or credits, and prices differ.
- Model parameters and request tokens are different things.
- Large files, long conversations, detailed reasoning, and long answers can consume more tokens than expected.
- State the task and desired format clearly, include only useful context, and request an appropriate answer length.

### Model effort

**Key concept: match effort to complexity instead of automatically choosing the highest setting.**

- Some models expose Low, Medium, High, Max, or XHigh effort; other models and providers use a fixed or automatic level.
- Low effort usually prioritises speed and token efficiency for short, simple tasks.
- High effort gives difficult, multi-step work more reasoning and checking budget.
- Max or XHigh can suit long agentic or coding work when the model supports it.
- Effort is a signal, not a strict token budget or a guarantee of quality.
- Compare effort settings fairly: keep the model, prompt, and fresh-chat context identical, and change only effort.
- Use exact token counts supplied by the interface or provider. If they are not shown, record **Not shown** rather than accepting an invented estimate.

References: [Claude effort controls](https://platform.claude.com/docs/en/build-with-claude/effort) and the local [2026 Agentic Coding Trends Report](Resources/2026%20Agentic%20Coding%20Trends%20Report.pdf).

## Stage 3 — Question, compare, and trace outputs

**Key concept: always know where your output is going and where to find it.**

- HuggingChat's image badge identifies a vision or multimodal model.
- A model without an image badge is usually text-first; check its card.
- The hammer badge means tool calling.
- Provider badges describe where or how the model runs, not a new skill.
- LLM outputs are probabilistic: wording can vary even when the intended meaning is similar.
- HuggingChat's free allowance for this workshop is 20 questions; Experiment 2 deliberately uses two.
- Compare the answer itself; a larger model is not automatically correct.
- Clear-looking wording can hide assumptions. Ask what must be physically present or true for the target outcome to happen.
- A more explicit target can improve a lightweight model's answer without increasing model size or reasoning effort.
- Use a troubleshooting loop: run, read the last error line, make one repair, and rerun.
- In Stage 3, **Submit & save** triggers the instructions in `llm_workshop/worksheet.py`.
- Stage 3 worksheet output is written to `tasks/stage3_answers.json`; the button does not choose that destination automatically.

## Notebook 1 main task — Build and refine a catalogue

**Key concept: express the data, output, target, and success checks before asking a coding agent for code.**

- Data: 18 rows in `data/notebook1/products.csv` and their mapped pixel-art apparel images.
- Output: `tasks/notebook1/catalogue.html`.
- Target: a responsive shopping grid whose cards come from the CSV.
- Ask GitHub Copilot Chat to return the code; create the HTML file and paste the code yourself.
- Preview the page with VS Code Live Preview and verify both appearance and CSV-to-image mapping.
- Begin with the core card fields: image, name, brand, type, and price.
- Treat colour, release date, sizes, country of origin, and designer as optional details that can be shown or hidden for a purpose.
- Use a reiteration loop: prompt, build, open, inspect, request one change, and verify again.
- Keep each follow-up prompt small enough that you can identify what changed.
- Useful later requests include sorting by price or release date, filtering by type, and adding a details toggle.
- Do not assume that IDs arrive in order or that every file reference is valid.
- Keep an imperfect product row visible by providing a useful missing-image fallback.
- Choose and test sorting deliberately: original row order, numerical ID, price, and release date answer different questions.

## Before accepting any AI-assisted result

- Where did the input come from?
- Which model type fits it?
- What exact result did I request?
- Where will the output be written?
- How will I open or run it?
- Did I verify the result instead of trusting confident wording?
- Could I ask the same useful question with less unnecessary context?

More stage concepts will be added as the six sandbox tasks are built.
