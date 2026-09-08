# Local OCR model snapshot

- Model: **Tesseract tessdata_fast English**, an integer LSTM text-recognition model.
- Maintainer: [tesseract-ocr](https://github.com/tesseract-ocr/tessdata_fast).
- Pinned revision: `87416418657359cb625c412a48b6e1d6d41c29bd`.
- [Original model file](https://github.com/tesseract-ocr/tessdata_fast/blob/87416418657359cb625c412a48b6e1d6d41c29bd/eng.traineddata).
- Local file: `tessdata/eng.traineddata` — **4,113,088 bytes**.
- SHA-256: `7d4322bd2a7749724879683fc3912cb542f19906c83bcc1a52132556427170b2`.
- Licence: **Apache-2.0**, reproduced unchanged in [LICENSE](LICENSE).

This is an OCR model, not a chat LLM. It recognises text; your script still needs to identify fields such as the invoice date and total. The model is distributed unchanged and does not download weights at runtime.

The workshop's Linux/Python 3.12 environment uses the `tesserocr` binary wheel with Tesseract 5.5.1. Use `PyTessBaseAPI(path=..., lang="eng", oem=OEM.LSTM_ONLY)` and point `path` at this `tessdata` folder. Do not use the legacy OCR engine with this model. See the [tesserocr API example](https://github.com/sirfz/tesserocr#usage).
