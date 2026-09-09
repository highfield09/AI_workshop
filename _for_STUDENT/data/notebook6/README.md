# Workbook 6 · Invoice images and traceability

Source: [High-Quality Invoice Images for OCR](https://www.kaggle.com/datasets/osamahosamabdellatif/high-quality-invoice-images-for-ocr), uploaded by **osama hosam Abdellatif** (`osamahosamabdellatif`). This workshop uses **version 3**, last updated 9 May 2025.

The 499-image set is the first sub-batch, `batch_1/batch_1/batch1_1`, with its corresponding `batch_1/batch_1/batch1_1.csv`. The larger top-level Batch 1 contains other sub-batches, which this workshop does not download.

The Kaggle listing identifies the licence as **Database: Open Database, Contents: Database Contents**. See the [dataset page](https://www.kaggle.com/datasets/osamahosamabdellatif/high-quality-invoice-images-for-ocr) for its licence and provenance. Attribution is to the uploader; it is not a claim that the uploader created every document.

Run from the repository root:

```bash
python _for_TRAINER/scripts/prepare_receipt_data.py
```

- `batch1_1/` — first five original JPG images, unchanged, named batch1-0001.jpg through batch1-0005.jpg.
- `batch1_1.csv` — original reference CSV, unchanged.
- `manifest.json` — source version, local filenames, sizes and SHA-256 hashes.

Only five images and the unchanged 499-row reference CSV are downloaded into each student's own Codespace and are Git-ignored. Existing older downloads are preserved, but the exercise selects only the first five. Only this documentation and the six-file manifest travel with the course repository. If Kaggle requires authentication, use your own account and the documented Kaggle token mechanism; never paste a token into a notebook or chat.

Start with `batch1_1/batch1-0001.jpg`. Keep the reference CSV separate from OCR input: use it to check provenance and results, not to copy an answer into the extracted spreadsheet.
