"""Verify the pinned OCR model and, when present, the exact downloaded sub-batch."""

import argparse
import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "_for_TRAINER"))
from scripts.prepare_receipt_data import DATA, HANDLE, EXPECTED_IMAGES, sha256

MODEL_SHA256 = "7d4322bd2a7749724879683fc3912cb542f19906c83bcc1a52132556427170b2"


def check_assets(require_data=False):
    model = ROOT / "_for_STUDENT/tasks/06_receipt_ocr/model/tessdata/eng.traineddata"
    assert sha256(model) == MODEL_SHA256, "OCR model differs from the pinned snapshot"
    manifest = json.loads((DATA / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["dataset"] == HANDLE
    expected_paths = {"batch1_1.csv"} | {f"batch1_1/{name}" for name in EXPECTED_IMAGES}
    assert len(manifest["files"]) == 500
    assert {row["path"] for row in manifest["files"]} == expected_paths
    if not (DATA / "batch1_1.csv").exists() and not list((DATA / "batch1_1").glob("*.jpg")):
        if require_data:
            raise AssertionError("Download the receipt data with _for_TRAINER/scripts/prepare_receipt_data.py")
        return
    for record in manifest["files"]:
        path = DATA / record["path"]
        assert path.stat().st_size == record["bytes"], f"Wrong size: {path}"
        assert sha256(path) == record["sha256"], f"Changed receipt asset: {path}"
    assert {p.name for p in (DATA / "batch1_1").glob("*.jpg")} == EXPECTED_IMAGES
    with (DATA / "batch1_1.csv").open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames == ["File Name", "Json Data", "OCRed Text"]
        rows = list(reader)
    assert len(rows) == 499 and {row["File Name"] for row in rows} == EXPECTED_IMAGES


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-data", action="store_true")
    check_assets(parser.parse_args().require_data)
    print("Receipt model and available data match their recorded provenance.")
