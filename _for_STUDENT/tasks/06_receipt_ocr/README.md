# Workbook 6 · Build your receipt pipeline in four iterations

Create and refine `receipt_reader.py` with your coding agent. Implement one
iteration at a time; a completed pipeline is deliberately not provided.

1. **Full text:** read `batch1-0001.jpg`, save `raw/batch1-0001.txt` unchanged,
   and compare it with the image. These are JPG invoices, not PDF files.
2. **Excel:** reuse that text to create `first_receipt.xlsx`: one **Items** row
   per purchased line, including numeric quantity, and one **Receipts** summary
   row per document. Convert decimal commas carefully; preserve IDs/dates as
   text. Use `review_status` and `review_note` to record checks and uncertainty.
3. **Batch:** select exactly the first 20 JPG filenames in sorted order, ending
   at `batch1-0020.jpg`. Process sequentially, cache raw text, avoid duplicate
   item rows, preserve human reviews, and account for all files in `batch_run.csv`.
   Save combined tables in `receipts_20.xlsx`; do not overwrite the first example.
4. **Analysis:** use checked item rows from Excel, not another OCR call. Sum
   quantity by item description; save `item_quantity_summary.csv` and a labelled
   bar chart `item_quantities.png`. Explain exclusions and sample limitations.

Source directory: `_for_STUDENT/data/notebook6/batch1_1/`.
All generated files belong under `_for_STUDENT/outputs/06_receipt_ocr/` and are
Git-ignored. Source JPGs and reference CSV must remain unchanged. The CSV is only
for checking afterwards, never a substitute for reading the images.

Use [GLM-OCR](https://huggingface.co/zai-org/GLM-OCR) through the supplied helper:

```python
from model.glm_reader import read_image
text = read_image(image_path, "Text Recognition:", max_new_tokens=4096, max_time=600)
```

See [model setup](model/README.md). Use a 16 GB environment; allow roughly 40
minutes or longer for 20 uncached pages. The helper reuses one model in the same
process. Do not edit it or start parallel model copies. Ask your agent to anchor
file paths to the script rather than the terminal's current folder.

Q19–Q24 in the notebook each save separately to this workbook's `answers.json`.
