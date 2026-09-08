# Workbook 6 · Your pipeline outputs

- `raw/batch1-0001.txt` (and later one per image): unchanged full-page responses.
- `first_receipt.xlsx`: checked first-document **Items** and **Receipts** sheets.
- `receipts_20.xlsx`: combined item and receipt tables for the first 20 inputs.
- `batch_run.csv`: one status row per selected document, including failed cases.
- `item_quantity_summary.csv`: grouped quantities used in the chart.
- `item_quantities.png`: top-10 item bar chart, or a clearly labelled alternative.

Open Excel with **SpreadJS XLSX Editor** by **MESCIUS** or use the notebook's
read-only sheet previews. Open TXT/CSV/PNG files directly in Explorer.

These outputs are local to your Codespace and Git-ignored. Preserve source
filenames, raw evidence, review decisions and failure records. Do not count an
invoice total once for every item, treat missing values as zero, or use
unreviewed rows in the final analysis. Keep first-iteration outputs rather than
overwriting them when adding the batch. Older `first_receipt_ocr.txt` files are
not automatically removed or migrated.
