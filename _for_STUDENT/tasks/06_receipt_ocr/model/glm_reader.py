"""Provided local VLM plumbing; students choose the schema and write the Excel tool."""
from pathlib import Path

MODEL = Path(__file__).resolve().parent / 'glm-ocr'


def available_memory():
    """Account for a Linux container limit, not just the host's memory."""
    try:
        info = dict(line.split(':', 1) for line in Path('/proc/meminfo').read_text().splitlines())
        available = int(info['MemAvailable'].strip().split()[0]) * 1024
        limit = Path('/sys/fs/cgroup/memory.max')
        if limit.is_file() and limit.read_text().strip() != 'max':
            remaining = int(limit.read_text()) - int(Path('/sys/fs/cgroup/memory.current').read_text())
            available = min(available, remaining)
        return available
    except (OSError, ValueError, KeyError):
        return None


def read_image(image_path, prompt, *, model_path=MODEL):
    """Return raw model text, not guaranteed JSON or verified field values.

    CPU-only, local files only; no automatic downloads or remote model code.
    Bounded to one image, ~2 megapixels, four CPU threads and 320 new tokens.
    """
    image_path = Path(image_path).resolve()
    model_path = Path(model_path).resolve()
    if not image_path.is_file():
        raise FileNotFoundError(f'Image not found: {image_path}')
    if not (model_path / 'model.safetensors').is_file():
        raise FileNotFoundError('GLM-OCR is not downloaded. Run sh _for_TRAINER/scripts/setup_glm_ocr.sh from the repository root.')
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError('Provide a prompt containing your required JSON schema.')
    available = available_memory()
    if available is not None and available < 8 * 1024**3:
        raise RuntimeError('GLM-OCR needs memory headroom: use a 16 GB environment and close other models. Less than 8 GiB is currently available.')
    try:
        import torch
        from transformers import AutoProcessor, AutoModelForImageTextToText
    except ImportError as exc:
        raise RuntimeError('Install the optional runtime with sh _for_TRAINER/scripts/setup_glm_ocr.sh, then restart the kernel.') from exc
    torch.set_num_threads(4)
    processor = AutoProcessor.from_pretrained(model_path, local_files_only=True, trust_remote_code=False)
    processor.image_processor.size = {'shortest_edge': 12544, 'longest_edge': 2007040}
    model = AutoModelForImageTextToText.from_pretrained(
        model_path, local_files_only=True, trust_remote_code=False,
        dtype=torch.float32, attn_implementation='sdpa',
    ).eval()
    messages = [{'role': 'user', 'content': [
        {'type': 'image', 'url': str(image_path)}, {'type': 'text', 'text': prompt},
    ]}]
    inputs = processor.apply_chat_template(messages, tokenize=True, add_generation_prompt=True,
                                          return_dict=True, return_tensors='pt')
    inputs.pop('token_type_ids', None)
    with torch.inference_mode():
        result = model.generate(**inputs, max_new_tokens=320, max_time=180, do_sample=False)
    generated = result[0][inputs['input_ids'].shape[1]:]
    text = processor.decode(generated, skip_special_tokens=True)
    eos = model.generation_config.eos_token_id
    eos = eos if isinstance(eos, list) else [eos]
    if len(generated) == 0 or int(generated[-1]) not in eos:
        raise RuntimeError('Model stopped before completing its answer. Do not write a partial answer into Excel; simplify the schema and retry.')
    return text
