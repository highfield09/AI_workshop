# GLM-OCR · local vision-language model

[GLM-OCR by Z.ai](https://huggingface.co/zai-org/GLM-OCR) reads document images
and can produce text or structured fields. It combines vision and language,
rather than only recognising individual printed characters. It is specialised
for document tasks, not a general-purpose chat assistant.

- Official snapshot: `zai-org/GLM-OCR` at `ca5d8b3e287e52589e37c28385d9655ee4372f9d`.
- Local snapshot directory: `glm-ocr/` (downloaded, Git-ignored).
- Weight file: **2,650,579,464 bytes**; snapshot including tokenizer about **2.66 GB**.
- Provenance/checksums: [glm-ocr-manifest.json](glm-ocr-manifest.json).
- Model licence: **MIT**, as stated in the [official model card](https://huggingface.co/zai-org/GLM-OCR#license).
  Its unchanged upstream README is included in the downloaded snapshot.
- Tested runtime: Python 3.12 on Linux, PyTorch 2.14.0 CPU, Torchvision 0.29.0 CPU, Transformers 5.16.1.
- [Official Transformers documentation](https://huggingface.co/docs/transformers/model_doc/glm_ocr).

From the repository root:

```bash
sh _for_TRAINER/scripts/setup_glm_ocr.sh
```

Allow **at least 6 GB of spare disk** for model/runtime installation (extra
package cache space may be needed), and use a **16 GB RAM environment**.
In Codespaces, that memory belongs to the cloud machine, not your laptop.
The supplied CPU helper refuses to start when Linux reports less than 8 GiB
available. No GPU, API key, inference credits, server or remote model code is needed.
Installation/download needs internet; inference uses local files only.

Our first-invoice test on Linux/AMD EPYC, limited to four CPU threads, took about
47 seconds for inference and peaked at 6.6 GiB RAM. This is not a laptop-speed
guarantee. The helper limits image resolution and answer length to keep one
receipt manageable; do not launch several model processes at once.

`glm_reader.py` is provided support code; students do not need to edit it.
From `receipt_reader.py` in the parent folder:

```python
from model.glm_reader import read_image
raw_response = read_image(image_path, prompt_with_json_schema)
```

For full-page text, use `read_image(image_path, "Text Recognition:", max_new_tokens=4096, max_time=600)`.
The default 320-token/180-second limits remain suitable for small field schemas;
full-page transcription needs the larger allowance. The helper caches one loaded
model for sequential calls in the same process, not across separate script runs.
Do not start parallel workers. Restart the kernel/process to release the model.

The student script saves the raw response, builds item and receipt tables,
validates numbers, batches the first five inputs, and charts checked data.
An intermediate JSON schema is optional for structuring, not required for full
transcription. Responses may contain Markdown fences, omit keys,
normalise dates or misread values. Missing fields should remain blank and be
flagged, not filled by guessing. A cleaner format is not proof of correct data.
