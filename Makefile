.PHONY: install lab check execute-demo

install:
	./_for_TRAINER/scripts/setup_environment.sh

lab:
	.venv/bin/python -m jupyter lab

check:
	.venv/bin/python -m pytest -q _for_TRAINER/tests
	.venv/bin/python _for_TRAINER/scripts/validate_notebook.py

execute-demo:
	.venv/bin/python _for_TRAINER/scripts/execute_demo.py
