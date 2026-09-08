import hashlib
import importlib.util
import json
from pathlib import Path

import pytest
from llm_workshop.course import ROOT
from scripts.prepare_glm_ocr import prepare, verify_snapshot, MANIFEST


def helper():
    spec = importlib.util.spec_from_file_location('glm_test_helper', ROOT / '_for_STUDENT/tasks/06_receipt_ocr/model/glm_reader.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_helper_explains_missing_inputs_and_memory(tmp_path, monkeypatch):
    module = helper()
    image = tmp_path / 'receipt.jpg'
    with pytest.raises(FileNotFoundError, match='Image not found'):
        module.read_image(image, '{}', model_path=tmp_path)
    image.write_bytes(b'fixture')
    with pytest.raises(FileNotFoundError, match='setup_glm_ocr.sh'):
        module.read_image(image, '{}', model_path=tmp_path)
    (tmp_path / 'model.safetensors').write_bytes(b'fixture')
    with pytest.raises(ValueError, match='JSON schema'):
        module.read_image(image, '', model_path=tmp_path)
    monkeypatch.setattr(module, 'available_memory', lambda: 1024**3)
    with pytest.raises(RuntimeError, match='16 GB'):
        module.read_image(image, '{}', model_path=tmp_path)


def test_model_provenance_pins_official_weights():
    manifest = json.loads(MANIFEST.read_text())
    assert manifest['model'] == 'zai-org/GLM-OCR'
    assert manifest['revision'] == 'ca5d8b3e287e52589e37c28385d9655ee4372f9d'
    weights = next(r for r in manifest['files'] if r['path'] == 'model.safetensors')
    assert weights['bytes'] == 2650579464
    assert weights['sha256'] == 'a16eb0de98d199293371c560f95f83130d2a2c9612449df16839f08ff9498815'
    assert not any(r['path'].endswith('.py') for r in manifest['files'])


def test_snapshot_is_optional_and_changed_files_are_preserved(tmp_path):
    data = b'local model fixture'
    manifest = tmp_path / 'manifest.json'
    manifest.write_text(json.dumps({'model':'zai-org/GLM-OCR','revision':'test','files':[
        {'path':'model.safetensors','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}]}))
    destination = tmp_path / 'snapshot'
    assert verify_snapshot(False, destination, manifest) is False
    destination.mkdir()
    weights = destination / 'model.safetensors'
    weights.write_bytes(data)
    assert verify_snapshot(True, destination, manifest)
    prepare(destination, manifest)  # Already present: no request to the network.
    weights.write_bytes(b'changed')
    with pytest.raises(RuntimeError, match='left unchanged'):
        prepare(destination, manifest)
    assert weights.read_bytes() == b'changed'


def test_helper_keeps_inference_local_and_bounded():
    source = (ROOT / '_for_STUDENT/tasks/06_receipt_ocr/model/glm_reader.py').read_text()
    assert source.count('local_files_only=True') == 2
    assert source.count('trust_remote_code=False') == 2
    for text in ['max_new_tokens=320', 'max_time=180', 'do_sample=False', 'torch.set_num_threads(4)', 'torch.float32']:
        assert text in source
