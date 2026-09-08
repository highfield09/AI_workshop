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


def test_full_text_limits_and_model_reuse_without_heavy_dependencies(tmp_path, monkeypatch):
    from contextlib import nullcontext
    from types import SimpleNamespace
    import sys
    module = helper()
    image = tmp_path / 'image.jpg'
    image.write_bytes(b'fixture')
    (tmp_path / 'model.safetensors').write_bytes(b'fixture')
    loads, generations = [], []
    processor = SimpleNamespace(
        image_processor=SimpleNamespace(size={}),
        apply_chat_template=lambda *a, **k: {'input_ids': SimpleNamespace(shape=(1, 4))},
        decode=lambda *a, **k: 'complete full text',
    )
    def generate(**kwargs):
        generations.append(kwargs)
        return [[1, 2, 3, 4, 5, 9]]
    model = SimpleNamespace(generate=generate, generation_config=SimpleNamespace(eos_token_id=[9]))
    model.eval = lambda: model
    def load(*args, **kwargs):
        loads.append(kwargs)
        return model
    monkeypatch.setitem(sys.modules, 'torch', SimpleNamespace(
        float32='float32', set_num_threads=lambda n: None, inference_mode=nullcontext))
    monkeypatch.setitem(sys.modules, 'transformers', SimpleNamespace(
        AutoProcessor=SimpleNamespace(from_pretrained=lambda *a, **k: processor),
        AutoModelForImageTextToText=SimpleNamespace(from_pretrained=load)))
    monkeypatch.setattr(module, 'available_memory', lambda: 16 * 1024**3)
    assert module.read_image(image, 'Text Recognition:', model_path=tmp_path, max_new_tokens=4096, max_time=600) == 'complete full text'
    # Loading used memory; reusing an existing model must not recheck startup headroom.
    monkeypatch.setattr(module, 'available_memory', lambda: 0)
    assert module.read_image(image, 'Text Recognition:', model_path=tmp_path) == 'complete full text'
    assert len(loads) == 1 and module._load_model.cache_info().hits == 1
    assert generations[0]['max_new_tokens'] == 4096 and generations[0]['max_time'] == 600
    for kwargs in ({'max_new_tokens':4097}, {'max_time':601}, {'max_new_tokens':True}):
        with pytest.raises(ValueError):
            module.read_image(image, 'Text Recognition:', model_path=tmp_path, **kwargs)
    model.generate = lambda **k: [[1, 2, 3, 4, 5]]
    with pytest.raises(RuntimeError, match='partial data'):
        module.read_image(image, 'Text Recognition:', model_path=tmp_path)
