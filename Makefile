.PHONY: install lab check execute-demo

install:
	./scripts/setup_environment.sh

lab:
	.venv/bin/python -m jupyter lab

check:
	.venv/bin/python -m pytest -q
	.venv/bin/python scripts/validate_notebook.py

execute-demo:
	.venv/bin/python scripts/execute_demo.py
