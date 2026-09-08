# Workbook 6 · Build your receipt reader

Use your coding agent to create `receipt_reader.py` in this folder. There is deliberately no completed extraction script supplied: describing, running and checking that script is your task.

Start with only `_for_STUDENT/data/notebook6/batch1_1/batch1-0001.jpg`. Use
[GLM-OCR](https://huggingface.co/zai-org/GLM-OCR) through the provided
`model/glm_reader.py`. Import `read_image` from `model.glm_reader`, then call
`read_image(image_path, prompt)` with a prompt containing a JSON schema.
See [model setup](model/README.md): 16 GB RAM recommended, 2.66 GB model download,
CPU-only inference, no API key. Do not edit the provided model helper.

The agent should anchor paths to the script's location, not assume a particular terminal folder. Request these outputs:

- `_for_STUDENT/outputs/06_receipt_ocr/first_receipt.xlsx` — one extracted invoice row.
- `_for_STUDENT/outputs/06_receipt_ocr/first_receipt_ocr.txt` — raw model response for checking mistakes.

Columns: `source_file`, `invoice_number`, `invoice_date`, `seller_name`, `tax_total`, `grand_total`, `currency_mark`, `review_note`.

Keep uncertain or missing values blank and explain them in `review_note`. Read the image, not the provided reference CSV, to produce the extracted row. The CSV is for checking afterwards; match on `File Name`, not row position.

Request the final SUMMARY row's Net worth, VAT and Gross worth, not a Tax Id.
Map VAT to `tax_total` and Gross worth to `grand_total`, and check net + tax =
total. Validate JSON and missing fields; flag any date normalisation. Never
invent an omitted currency symbol. Structured output still needs inspection.

Run from the repository root:

```bash
python _for_STUDENT/tasks/06_receipt_ocr/receipt_reader.py
```

The student-created script, spreadsheet, raw text and worksheet answers are Git-ignored. They stay in your own Codespace unless you choose to share them.
