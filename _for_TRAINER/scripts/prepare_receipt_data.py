"""Download only the 499-image first sub-batch and its matching CSV."""

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import shutil


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "_for_STUDENT" / "data" / "notebook6"
HANDLE = "osamahosamabdellatif/high-quality-invoice-images-for-ocr/versions/3"
REMOTE_IMAGES = "batch_1/batch_1/batch1_1"
REMOTE_CSV = "batch_1/batch_1/batch1_1.csv"
EXPECTED_IMAGES = {f"batch1-{number:04d}.jpg" for number in range(1, 500)}


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prepare(data=DATA):
    import kagglehub

    data = Path(data)
    image_dir = data / "batch1_1"
    image_dir.mkdir(parents=True, exist_ok=True)
    csv_path = data / "batch1_1.csv"
    if not csv_path.exists():
        cached_csv = Path(kagglehub.dataset_download(HANDLE, path=REMOTE_CSV))
        shutil.copy2(cached_csv, csv_path)
    def download_image(name):
        target = image_dir / name
        if not target.exists():
            # Use explicit files: some KaggleHub versions cannot download a directory.
            cached = Path(kagglehub.dataset_download(HANDLE, path=f"{REMOTE_IMAGES}/{name}"))
            shutil.copy2(cached, target)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for count, _ in enumerate(pool.map(download_image, sorted(EXPECTED_IMAGES)), 1):
            if count % 50 == 0:
                print(f"Checked/downloaded {count}/499 images", flush=True)
    if {p.name for p in image_dir.glob("*.jpg")} != EXPECTED_IMAGES:
        raise RuntimeError("Local image folder contains unexpected or missing files.")
    files = [csv_path, *sorted(image_dir.glob("*.jpg"))]
    records = [{"path": p.relative_to(data).as_posix(), "bytes": p.stat().st_size,
                "sha256": sha256(p)} for p in files]
    manifest = data / "manifest.json"
    if manifest.exists():
        expected = json.loads(manifest.read_text(encoding="utf-8"))["files"]
        if records != expected:
            raise RuntimeError("Local receipt data differs from the recorded manifest; no existing file was overwritten.")
    else:
        manifest.write_text(json.dumps({"dataset": HANDLE, "image_count": 499, "files": records}, indent=2) + "\n", encoding="utf-8")
    print(f"Ready: 499 images and batch1_1.csv in {data}")
    return image_dir, csv_path


if __name__ == "__main__":
    prepare()
