.PHONY: install lab check execute-demo

install:
	./scripts/create_venv.sh
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -r requirements.txt
	.venv/bin/python -m ipykernel install --user --name llm-workshop --display-name "Python (LLM Workshop)"

lab:
	.venv/bin/python -m jupyter lab

check:
	.venv/bin/python -m pytest -q
	.venv/bin/python scripts/validate_notebook.py

execute-demo:
	.venv/bin/python scripts/execute_demo.py
