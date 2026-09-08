"""Download and verify the pinned official GLM-OCR snapshot inside the project."""
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
MODEL_ROOT = ROOT / '_for_STUDENT/tasks/06_receipt_ocr/model'
MANIFEST = MODEL_ROOT / 'glm-ocr-manifest.json'
SNAPSHOT = MODEL_ROOT / 'glm-ocr'


def digest(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def verify_snapshot(require=False, destination=SNAPSHOT, manifest_path=MANIFEST):
    manifest = json.loads(manifest_path.read_text())
    if not destination.exists() and not require:
        return False
    for record in manifest['files']:
        path = destination / record['path']
        if not path.is_file() or path.stat().st_size != record['bytes'] or digest(path) != record['sha256']:
            raise RuntimeError(f'Missing or changed GLM-OCR file: {path}. Run prepare_glm_ocr.py; preserve changed files separately before retrying.')
    return True


def prepare(destination=SNAPSHOT, manifest_path=MANIFEST):
    import requests
    manifest = json.loads(manifest_path.read_text())
    destination.mkdir(parents=True, exist_ok=True)
    missing_bytes = sum(r['bytes'] for r in manifest['files'] if not (destination / r['path']).exists())
    if shutil.disk_usage(destination).free < missing_bytes + 512 * 1024**2:
        raise RuntimeError('Not enough disk space for the model download plus 512 MB headroom.')
    for record in manifest['files']:
        target = destination / record['path']
        if target.exists():
            if target.stat().st_size != record['bytes'] or digest(target) != record['sha256']:
                raise RuntimeError(f'Existing file differs from the manifest; left unchanged: {target}')
            continue
        temporary = target.with_suffix(target.suffix + '.part')
        url = f"https://huggingface.co/{manifest['model']}/resolve/{manifest['revision']}/{record['path']}"
        print(f"Downloading {record['path']} ({record['bytes'] / 1024**2:.1f} MiB)", flush=True)
        with requests.get(url, stream=True, timeout=(30, 120)) as response:
            response.raise_for_status()
            with temporary.open('wb') as handle:
                for chunk in response.iter_content(1024**2):
                    handle.write(chunk)
        if temporary.stat().st_size != record['bytes'] or digest(temporary) != record['sha256']:
            raise RuntimeError(f'Download verification failed: {temporary}; no model file was replaced.')
        temporary.replace(target)
    verify_snapshot(True, destination, manifest_path)
    print(f'GLM-OCR ready: {destination}')


if __name__ == '__main__':
    prepare()
