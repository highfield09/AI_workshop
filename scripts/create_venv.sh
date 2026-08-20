#!/usr/bin/env sh
set -eu

if [ -x .venv/bin/python ] && .venv/bin/python -m pip --version >/dev/null 2>&1; then
    exit 0
fi

if python3 -m venv --clear .venv >/dev/null 2>&1; then
    exit 0
fi

# Some minimal Debian hosts omit ensurepip. Keep the workaround project-local
# instead of requiring sudo; Codespaces normally succeeds in the branch above.
python3 -m venv --clear --without-pip .venv
installer="$(mktemp /tmp/llm-workshop-get-pip.XXXXXX.py)"
trap 'rm -f "$installer"' EXIT
curl -fsSL https://bootstrap.pypa.io/get-pip.py -o "$installer"
.venv/bin/python "$installer"
