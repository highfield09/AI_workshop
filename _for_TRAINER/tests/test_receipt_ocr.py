from pathlib import Path

import pytest

from llm_workshop import receipt_support
from llm_workshop.course import ROOT
from scripts.build_course_notebook import build_workbooks
from scripts.check_receipt_assets import check_assets
from scripts.prepare_receipt_data import EXPECTED_IMAGES, REMOTE_IMAGES, REMOTE_CSV, prepare


def test_ocr_lesson_is_one_image_and_has_attribution_and_hints():
    book = build_workbooks()["06_receipt_ocr"]
    source = "\n".join(c.source for c in book.cells)
    assert "osama hosam Abdellatif" in source
    assert "version 3" in source and "Database: Open Database" in source
    assert "499 images in batch1_1" in source
    assert "exactly one data row" in source
    assert "receipt_reader.py" in source and "first_receipt.xlsx" in source
    assert "<details>" in source and "Hint · Build your prompt" in source
    assert "Do not process the whole folder yet" in source
    assert "Do not let the script copy answers from" in source
    assert "from llm_workshop.receipt_support" in book.cells[1].source
    assert source.index("DATASET AND CREDIT") < source.index("show_receipt_preview()")


def test_model_and_dataset_manifest_are_valid():
    check_assets()


def test_downloader_requests_only_explicit_first_subbatch_files(tmp_path, monkeypatch):
    import kagglehub
    cache = tmp_path / "cache"
    cache.mkdir()
    calls = []
    def fake_download(handle, *, path):
        assert "/versions/3" in handle
        calls.append(path)
        file = cache / Path(path).name
        file.write_bytes(b"test fixture")
        return str(file)
    monkeypatch.setattr(kagglehub, "dataset_download", fake_download)
    dest = tmp_path / "data"
    prepare(dest)
    expected = {REMOTE_CSV} | {f"{REMOTE_IMAGES}/{name}" for name in EXPECTED_IMAGES}
    assert set(calls) == expected and len(calls) == 500
    calls.clear()
    prepare(dest)
    assert calls == []  # Reuse all verified local files.
    (dest / "batch1_1/batch1-0001.jpg").write_bytes(b"changed")
    with pytest.raises(RuntimeError, match="differs"):
        prepare(dest)
    assert (dest / "batch1_1/batch1-0001.jpg").read_bytes() == b"changed"


def test_excel_preview_is_safe_and_demo_does_not_read_personal_data(tmp_path, monkeypatch):
    from openpyxl import Workbook
    path = tmp_path / "first_receipt.xlsx"
    workbook = Workbook()
    workbook.active.append(["seller_name", "grand_total"])
    workbook.active.append(["<script>PRIVATE TEST VALUE</script>", 6204.19])
    workbook.save(path)
    shown = []
    monkeypatch.setattr(receipt_support, "display", lambda content: shown.append(content.data))
    monkeypatch.setenv("WORKSHOP_DEMO_ANSWERS", str(tmp_path))
    receipt_support.preview_spreadsheet(path)
    assert "PRIVATE TEST VALUE" not in shown[-1]
    monkeypatch.delenv("WORKSHOP_DEMO_ANSWERS")
    receipt_support.preview_spreadsheet(path)
    assert "6204.19" in shown[-1]
    assert "&lt;script&gt;PRIVATE TEST VALUE&lt;/script&gt;" in shown[-1]
    assert "<script>PRIVATE TEST VALUE" not in shown[-1]
    path.write_bytes(b"not an Excel file")
    receipt_support.preview_spreadsheet(path)
    assert "Could not open the spreadsheet" in shown[-1]


def test_preview_handles_missing_receipt_without_downloading(tmp_path, monkeypatch):
    shown = []
    monkeypatch.setattr(receipt_support, "display", lambda content: shown.append(content.data))
    receipt_support.show_receipt_preview(tmp_path / "missing.jpg")
    assert "prepare_receipt_data.py" in shown[-1]


def test_local_ocr_to_excel_smoke_on_first_real_invoice(tmp_path, monkeypatch):
    """Check runtime availability without publishing a field-extraction solution."""
    from tesserocr import PyTessBaseAPI, OEM
    image = receipt_support.FIRST_IMAGE
    if not image.is_file():
        pytest.skip("Optional 499-image dataset has not been downloaded")
    model = ROOT / "_for_STUDENT/tasks/06_receipt_ocr/model/tessdata"
    with PyTessBaseAPI(path=str(model), lang="eng", oem=OEM.LSTM_ONLY) as api:
        api.SetImageFile(str(image))
        text = api.GetUTF8Text()
    assert len(text.split()) > 20
