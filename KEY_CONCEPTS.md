# Vibe Coding Workshop — Master Key Concepts

This is the workshop's growing take-home reference. Open it from the VS Code Explorer at any time. You can keep it in your repository, download it from GitHub, or save your own copy after the workshop.

## Stage 1 — Know your workspace

**Key concept: know where files live before you run or change anything.**

- The Explorer shows the directory tree.
- `notebooks/` contains lessons.
- `tasks/` contains isolated challenges and learner worksheets.
- `data/` contains shared input files.
- `outputs/` contains results you create.
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

## Stage 3 — Question, compare, and trace outputs

**Key concept: always know where your output is going and where to find it.**

- HuggingChat's image badge identifies a vision or multimodal model.
- A model without an image badge is usually text-first; check its card.
- The hammer badge means tool calling.
- Provider badges describe where or how the model runs, not a new skill.
- LLM outputs are probabilistic: wording can vary even when the intended meaning is similar.
- Compare the answer itself; a larger model is not automatically correct.
- Use a troubleshooting loop: run, read the last error line, make one repair, and rerun.
- In Stage 3, **Submit & save** triggers the instructions in `llm_workshop/worksheet.py`.
- Stage 3 worksheet output is written to `tasks/stage3_answers.json`; the button does not choose that destination automatically.

## Before accepting any AI-assisted result

- Where did the input come from?
- Which model type fits it?
- What exact result did I request?
- Where will the output be written?
- How will I open or run it?
- Did I verify the result instead of trusting confident wording?
- Could I ask the same useful question with less unnecessary context?

More stage concepts will be added as the six sandbox tasks are built.
