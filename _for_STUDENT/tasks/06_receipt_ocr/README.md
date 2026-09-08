# Workbook 6 · Build your receipt reader

Use your coding agent to create `receipt_reader.py` in this folder. There is deliberately no completed extraction script supplied: describing, running and checking that script is your task.

Start with only `_for_STUDENT/data/notebook6/batch1_1/batch1-0001.jpg`. Use the Tesseract English model in `model/tessdata/eng.traineddata` through the installed `tesserocr` Python package. No API key, paid service or GPU is needed for OCR.

The agent should anchor paths to the script's location, not assume a particular terminal folder. Request these outputs:

- `_for_STUDENT/outputs/06_receipt_ocr/first_receipt.xlsx` — one extracted invoice row.
- `_for_STUDENT/outputs/06_receipt_ocr/first_receipt_ocr.txt` — raw OCR text for checking mistakes.

Columns: `source_file`, `invoice_number`, `invoice_date`, `seller_name`, `tax_total`, `grand_total`, `currency_mark`, `review_note`.

Keep uncertain or missing values blank and explain them in `review_note`. Read the image, not the provided reference CSV, to produce the extracted row. The CSV is for checking afterwards; match on `File Name`, not row position.

Run from the repository root:

```bash
python _for_STUDENT/tasks/06_receipt_ocr/receipt_reader.py
```

The student-created script, spreadsheet, raw text and worksheet answers are Git-ignored. They stay in your own Codespace unless you choose to share them.
