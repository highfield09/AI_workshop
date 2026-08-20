# LLM Workshop Notebook

A small, classroom-style Jupyter project for experimenting with an LLM chat interface in VS Code or GitHub Codespaces. The notebook is designed to run immediately in an offline demo mode, then switch to:

- a local OpenAI-compatible service such as Ollama or vLLM;
- the existing classroom LiteLLM/vLLM gateway; or
- OpenAI or another cloud-hosted OpenAI-compatible endpoint.

The earlier full JupyterHub/vLLM deployment is preserved in [`vibe_jupyterhub_vllm_sandbox/`](vibe_jupyterhub_vllm_sandbox/). This root project is the lightweight notebook used by students.

## Open in GitHub Codespaces

1. Push this repository to GitHub.
2. Choose **Code → Codespaces → Create codespace on main**.
3. Wait for the dev container to install the notebook dependencies.
4. Open `notebooks/01_llm_chat_workshop.ipynb` and select **Python (LLM Workshop)** if VS Code asks for a kernel.

The committed notebook includes safe offline outputs, so its examples are visible in GitHub and VS Code before a live API is configured.

## Run in this VS Code workspace

```bash
cp .env.example .env
make install
```

Then open the notebook in VS Code and choose the `.venv` Python interpreter. Alternatively, start JupyterLab with:

```bash
make lab
```

## Configure an LLM

Keep secrets in `.env` or in Codespaces secrets—never in a notebook cell.

```dotenv
LLM_PROVIDER=local
LOCAL_LLM_BASE_URL=http://localhost:11434/v1
LOCAL_LLM_API_KEY=ollama
LOCAL_LLM_MODEL=qwen3:8b
```

For OpenAI cloud, set `LLM_PROVIDER=openai`, `OPENAI_API_KEY`, and `OPENAI_MODEL`. For the existing gateway, use `LLM_PROVIDER=classroom` plus the `CLASSROOM_*` variables from `.env.example`.

## Instructor workflow

The notebook is split into numbered sections with short tasks, hints, and extension prompts. Use the offline demo provider when teaching UI or prompt concepts without network access. Use `make check` before committing an iteration, and `make execute-demo` to refresh only the safe demo outputs.

The official OpenAI Python SDK reads `OPENAI_API_KEY` from the environment; the project follows the same pattern and never serializes keys into notebook output.

