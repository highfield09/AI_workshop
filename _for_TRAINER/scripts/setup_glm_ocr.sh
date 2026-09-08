#!/usr/bin/env sh
set -eu
project_root="$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)"
cd "$project_root"
if [ ! -x .venv/bin/python ]; then
    echo 'Run ./_for_TRAINER/scripts/setup_environment.sh first.'
    exit 1
fi
echo 'Workbook 6: allow several GB of disk; use a 16 GB RAM environment.'
.venv/bin/python -m pip install 'torch==2.14.0' 'torchvision==0.29.0' --index-url https://download.pytorch.org/whl/cpu
.venv/bin/python -m pip install -r _for_TRAINER/requirements-glm-ocr.txt
.venv/bin/python _for_TRAINER/scripts/prepare_glm_ocr.py
