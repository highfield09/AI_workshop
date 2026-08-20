# Vibe Coding Workshop

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/highfield09/AI_workshop)

A beginner-friendly workshop for learning how to reproduce a clear output with help from an AI interface. The emphasis is on finding files, describing a target, making a small change, opening the result, and refining it—not on memorizing technical syntax.

## Start here

1. Open the repository in GitHub Codespaces.
2. Wait for the development container to finish rebuilding.
3. Open notebooks/01_start_here.ipynb.
4. Select **Python (Vibe Workshop)** if VS Code asks for a kernel.
5. Run the notebook from the top.

### Do learners need Python on their laptops?

No, not when they use GitHub Codespaces. Python, Jupyter, the extensions, and all course packages run inside the online Codespace.

If the notebook asks for a kernel, choose **Python (Vibe Workshop)**. Someone running the project entirely on their own laptop will need Python 3.12; Codespaces users do not.

The first notebook contains:

- **Stage 1:** a friendly VS Code and directory-tree orientation with an interactive quiz;
- **Stage 2:** AI links, a visual model-card guide, token efficiency, model-effort controls, and prompting references;
- **Stage 3:** Google AI Mode fact retrieval, HuggingChat model selection, Gemini reasoning comparisons, locally saved worksheets, and an AI-assisted repair challenge;
- **Experiment 6:** a GitHub Copilot brief that turns supplied CSV data and original pixel-art apparel into a browser catalogue.

Open [KEY_CONCEPTS.md](KEY_CONCEPTS.md) for the growing student take-home reference.

## Workshop folders

| Folder | What belongs there |
|---|---|
| notebooks/ | Course lessons |
| tasks/ | One self-contained folder per sandbox |
| data/ | Small course input files |
| outputs/ | Reference results and instructor examples |
| Resources/ | Optional student reading and reports |
| scripts/ | Reusable instructions and course checks |

The older deployment material remains in the repository for reference but is hidden from the default VS Code Explorer view.

The Codespace also installs GitHub Copilot Chat and VS Code Live Preview. Copilot access depends on the GitHub account signed into VS Code.

## Local VS Code setup

From the repository root:

    make install
    make lab

Use make check before committing an iteration. Use make execute-demo to rebuild the safe committed notebook outputs.

## Course design rule

Each sandbox should give learners one clear target, tiny isolated inputs, a starting prompt, an obvious way to open or run the result, and a short comparison checklist.

Secrets belong in Codespaces secrets or a local .env file. The .env file is Git-ignored and must never be committed.
