"""Confirm that the learner-facing Python environment is ready."""

from __future__ import annotations

from importlib.util import find_spec
from pathlib import Path
import sys

from jupyter_client.kernelspec import KernelSpecManager


ROOT = Path(__file__).resolve().parents[2]
EXPECTED_ENV = (ROOT / ".venv").resolve()
REQUIRED_MODULES = ["ipykernel", "ipywidgets", "nbformat", "PIL", "openpyxl", "kagglehub"]


def main() -> None:
    if Path(sys.prefix).resolve() != EXPECTED_ENV:
        raise SystemExit(
            f"Expected project environment {EXPECTED_ENV}, but Python uses {sys.prefix}"
        )

    missing = [name for name in REQUIRED_MODULES if find_spec(name) is None]
    if missing:
        raise SystemExit(f"Missing notebook packages: {', '.join(missing)}")

    kernels = KernelSpecManager().find_kernel_specs()
    if "llm-workshop" not in kernels:
        raise SystemExit("The llm-workshop Jupyter kernel is not registered.")

    print("Environment ready: Python (.venv)")
    print(f"Interpreter: {sys.executable}")


if __name__ == "__main__":
    main()
