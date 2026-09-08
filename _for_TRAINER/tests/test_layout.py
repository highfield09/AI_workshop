import json
from pathlib import Path
import subprocess

from llm_workshop.course import ROOT, answer_path
from scripts.build_course_notebook import build_workbooks


def test_labelled_layout_and_codespaces_setup():
    assert (ROOT / '_for_STUDENT/KEY_CONCEPTS.md').is_file()
    assert not (ROOT / 'ASTRA_PROJECT_SEED.md').exists()
    config = json.loads((ROOT / '.devcontainer/devcontainer.json').read_text())
    setup = ROOT / config['postCreateCommand']
    assert setup.is_file()
    assert '_for_TRAINER/scripts/create_venv.sh' in setup.read_text()
    subprocess.run(['sh', '-n', str(setup)], check=True)
    assert answer_path('06_receipt_ocr').relative_to(ROOT).as_posix() == '_for_STUDENT/tasks/06_receipt_ocr/answers.json'
    assert not list(ROOT.glob('**/products.cleaned.csv'))
    for book in build_workbooks().values():
        assert '"_for_TRAINER" / "llm_workshop"' in book.cells[1].source


def test_current_and_legacy_student_outputs_stay_git_ignored():
    examples = [
        '_for_STUDENT/tasks/06_receipt_ocr/receipt_reader.py',
        '_for_STUDENT/tasks/06_receipt_ocr/answers.json',
        '_for_STUDENT/outputs/06_receipt_ocr/first_receipt.xlsx',
        '_for_STUDENT/outputs/05_shopping_catalogue/catalogue.html',
        '_for_STUDENT/data/notebook6/batch1_1.csv',
        '_for_STUDENT/tasks/06_receipt_ocr/model/glm-ocr/model.safetensors',
        'tasks/01_start_here/answers.json', 'outputs/notebook1/catalogue.html',
        'data/notebook6/batch1_1.csv',
    ]
    for path in examples:
        assert subprocess.run(['git', 'check-ignore', '-q', path], cwd=ROOT).returncode == 0
