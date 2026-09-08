# Course support — trainer maintained

This directory is distributed to every student Codespace. **It is not private.**
It contains the machinery needed to run the workbooks, not completed model-answer
tools. Store private answer keys outside the shared repository.

- **scripts/** — environment setup, notebook builders, demo execution and validation.
- **llm_workshop/** — shared widgets, readable panels and answer-saving functions.
- **tests/** — maintenance checks.
- **vibe_jupyterhub_vllm_sandbox/** — older deployment reference, not the classroom workflow.

Students may run setup/data-preparation commands when instructed. They do not
need to modify these files. Root-level `requirements.txt`, `Makefile`, `pytest.ini`
and hidden `.devcontainer`/`.vscode` configuration are also trainer maintained;
they remain at the root so Codespaces and developer tools can find them.

From the repository root, refresh course materials with:

```bash
.venv/bin/python _for_TRAINER/scripts/build_course_notebook.py
.venv/bin/python _for_TRAINER/scripts/execute_demo.py
make check
```

Demo execution uses blank temporary answers. Never publish personal widget state
or learner-generated files. The model snapshot is supplied as a student input,
but the large OCR image sub-batch is downloaded independently per Codespace.
