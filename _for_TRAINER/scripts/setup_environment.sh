#!/usr/bin/env sh
set -eu

project_root="$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)"
cd "$project_root"

./_for_TRAINER/scripts/create_venv.sh
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m ipykernel install --user --name llm-workshop --display-name "Python (.venv)"
.venv/bin/python _for_TRAINER/scripts/check_environment.py
