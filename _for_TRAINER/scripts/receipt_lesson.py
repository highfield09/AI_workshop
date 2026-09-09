"""Beginner OCR workshop: four short iterations, with optional technical hints."""


def receipt_lesson_cells(markdown, code, panel):
    def prompt(text):
        return code(f"copyable_prompt({text!r})", "interactive")

    def question(number, key, title, text, tip):
        return code(f'''worksheet_box(
    {key!r},
    question_label={f"QUESTION {number} · {title}"!r},
    response_label={text!r},
    reveal_html={panel("TAKEAWAY", tip, "success")!r},
)''', "interactive")

    return [
        markdown(f"""
## From invoice images to a checked chart

Use [GLM-OCR by Z.ai](https://huggingface.co/zai-org/GLM-OCR), a local
vision-language model, to read invoice images.

**Read one receipt → Create an Excel table → Process five receipts → Make a chart.**

Describe what you want to your coding agent, run the result, and inspect whether
it worked. Use a Codespace or computer with about **16 GB RAM**. No inference
API key is needed. These receipts are JPG images, **not PDFs**.

<details>
<summary><b>Dataset, licensing and credit</b></summary>

**High-Quality Invoice Images for OCR**, uploaded by **osama hosam Abdellatif**
(`osamahosamabdellatif`) on
[Kaggle](https://www.kaggle.com/datasets/osamahosamabdellatif/high-quality-invoice-images-for-ocr).
We use **version 3**, dated 9 May 2025: the first five images from the
499-image `batch1_1` sub-batch, plus its unchanged reference CSV for traceability.
The listed licence is **Database: Open Database, Contents: Database Contents**.
See `_for_STUDENT/data/notebook6/README.md` for provenance.

</details>

<details>
<summary><b>One-time setup: download the model and five receipts</b></summary>

From the repository root:

```bash
source .venv/bin/activate
sh _for_TRAINER/scripts/setup_glm_ocr.sh
python _for_TRAINER/scripts/prepare_receipt_data.py
```

If Kaggle asks for login, create your own
[Kaggle API token](https://www.kaggle.com/settings/api) and add
`KAGGLE_API_TOKEN` as a Codespaces secret. Never paste it into a notebook or chat.
The MIT-licensed model snapshot is saved in
`_for_STUDENT/tasks/06_receipt_ocr/model/glm-ocr/`.
It is about **2.66 GB**; allow at least **6 GB spare disk** plus package caches.
Model weights, receipt downloads and learner outputs are Git-ignored.

Our four-thread CPU test took about 115 seconds for one full page and used
6.6 GiB RAM. Allow roughly **10–15 minutes** for five similar uncached receipts;
loading time and your hardware can make it longer. Use one model process.

</details>

Open a fresh Copilot Chat in **Agent** mode. Keep the supplied helper and source
JPG/CSV files unchanged. Your script belongs in
`_for_STUDENT/tasks/06_receipt_ocr/receipt_reader.py`.
"""),
        markdown(f"""
### Iteration 1 · Read one receipt

**Goal:** turn one receipt image into raw text.

{panel("TASK · READ THE RECEIPT", "Ask your coding agent to create "
    "<code>receipt_reader.py</code> and read <b>all visible text</b> using the "
    "supplied GLM-OCR helper. Save the text, then open it beside the original "
    "image. Check the seller, client, items and summary.", "task")}
"""),
        prompt("""Input: _for_STUDENT/data/notebook6/batch1_1/batch1-0001.jpg
Output: _for_STUDENT/outputs/06_receipt_ocr/raw/batch1-0001.txt
Script: _for_STUDENT/tasks/06_receipt_ocr/receipt_reader.py
Read the entire receipt using the supplied local GLM-OCR model.
Save all recognised text. Implement only this first iteration."""),
        markdown("""
<details>
<summary><b>Hint · Build your prompt in small steps</b></summary>

1. Ask for a Python script named `receipt_reader.py` in the task folder.
2. Give the input and output paths. Ask it to create the output folder.
3. Ask it to preserve the full model response and print where it was saved.
4. Ask for the run command. Run it, then compare the image and text.

</details>

<details>
<summary><b>More detail · For the coding agent</b></summary>

Use the supplied `model.glm_reader` helper with the full-text task
`Text Recognition:`; a JSON schema is not needed yet. Full pages can need
`max_new_tokens=4096` and `max_time=600`. Keep paths relative to the script,
preserve raw text unchanged and report incomplete responses. Do not process
the whole folder yet.

</details>
"""),
        code("show_receipt_preview()", "hide-input"),
        markdown("""
### What model startup can look like

**Illustrative output—not a live download or benchmark:**

```text
Loading local GLM-OCR processor...
Loading weights: [████████████████████] 100%
Model ready. Reading batch1-0001.jpg...
```

The weights must be loaded into memory before the first image is read.
This can take time. Later images in the same process reuse the loaded model.
"""),
        question(17, "receipt_full_text_review", "Check the OCR",
                 "Compare the OCR text with the original receipt. Which main sections were captured? Give one example of either an OCR error or formatting/layout that was not preserved. Is it accurate enough for extracting invoice data? What file contains the raw OCR text?",
                 "Check the image, not just how tidy the text looks. A complete-looking response can still omit details."),
        markdown("""
### Iteration 2 · Make the spreadsheet

**Goal:** turn the saved text into structured Excel data.

Reuse the saved OCR text—do not run OCR again. Ask your agent to create
`first_receipt.xlsx` under `_for_STUDENT/outputs/06_receipt_ocr/`.
Copy the sheet requirements below into your request.
"""),
        prompt("""Create first_receipt.xlsx with these two sheets:

Items — one row per product:
source_file, invoice_number, line_number, description, quantity, unit,
unit_net_price, line_net_total, vat_rate, line_gross_total, review_status, review_note

Receipts — one row per invoice:
source_file, invoice_number, invoice_date, seller_name, client_name,
net_total, tax_total, grand_total, currency_mark, review_status, review_note

Reuse the saved raw OCR text. Do not run OCR again.
Keep missing values blank. Use numeric Excel cells for amounts and quantities.
Start review_status as unreviewed; mark checked only after comparison with the image."""),
        markdown("""
The first receipt should produce **seven item rows** and **one receipt row**.
Numbers printed as `3,00` and `1 394,67` should become numeric values
`3` and `1394.67`. Missing values stay blank.

In **Extensions** (`Ctrl+Shift+X`, or `Command+Shift+X` on macOS), install
[**Spreadsheet Viewer**](https://marketplace.visualstudio.com/items?itemName=GrapeCity.gc-excelviewer).
Open `first_receipt.xlsx` in Explorer. If needed, use **Open With… → Excel Viewer**.
Inspect both sheet tabs. The cells below also provide a notebook preview.

<details>
<summary><b>Hint · Keep the checks independent</b></summary>

Do not let the script copy answers from the reference CSV or hard-code them.
Use `openpyxl` to write numeric cells. Do not delete decimal commas blindly.
Keep IDs and dates as text; a Tax Id is not tax. Treat model text as text,
not spreadsheet formulas. Flag ambiguous values rather than guessing.
Preserve raw OCR and human review decisions when rerunning.

</details>
"""),
        code('preview_spreadsheet(sheet_name="Items")\npreview_spreadsheet(sheet_name="Receipts")', "hide-input"),
        question(18, "receipt_numeric_cleaning", "Check the numbers",
                 "Choose one product row and compare its quantity, unit price and net total with the original receipt. Were the values converted correctly? Check that quantity × unit price gives the expected net total.",
                 "For the first receipt, one check is 3 × 464.89 = 1394.67. Verify the row against the image."),
        question(19, "receipt_row_structure", "Check the spreadsheet structure",
                 "How many item rows and receipt rows were created for the first receipt? Why is the final invoice total stored with the receipt rather than repeated for every item?",
                 "There should be 7 item rows and 1 receipt row. The invoice total belongs to the whole receipt, not each product."),
        markdown("""
### Iteration 3 · Process the first 5 receipts

**Goal:** extend the working script from one receipt to five:
`batch1-0001.jpg` → `batch1-0005.jpg`.

Process one at a time using the same loaded model. Reuse saved OCR text.
Add the four new receipts and their item rows to a new combined workbook;
keep `first_receipt.xlsx` unchanged.

Save:

- one raw `.txt` file per receipt;
- `batch_run.csv` showing success, needs review or failure;
- `receipts_5.xlsx` with combined **Items** and **Receipts** sheets.

Inspect all five results, then tell your agent which rows may be marked checked.
Allow roughly **10–15 minutes** for five similar uncached receipts.

<details>
<summary><b>Hint · A reliable batch</b></summary>

Select the first five filenames in sorted order, not every image in the folder.
Keep exactly five audit rows, including failures. Use one model, save progress,
reuse valid cached text and avoid duplicate item rows on reruns. Do not silently
ignore errors or assume every invoice has seven products.

</details>
"""),
        question(20, "receipt_batch_review", "Check the 5-receipt run",
                 "Were all 5 receipts processed? How many succeeded, needed review or failed? Name one receipt that you checked against its original image.",
                 "The audit trail should account for all five inputs, even when a document needs review."),
        markdown("""
### Iteration 4 · Make a chart

**Goal:** show the top 10 item descriptions by total quantity.

Use the saved **Items** sheet—do not run OCR again.

1. Use checked rows with valid quantities.
2. Group identical item descriptions and sum their quantities.
3. Save `item_quantity_summary.csv` and `item_quantities.png` in the output folder.
4. Label the axes **Item description** and **Total quantity**.
5. Open the chart and check one value against the spreadsheet.

**Optional histogram:** show the distribution of quantity per item row instead.
A bar chart compares named categories; a histogram groups numeric values into ranges.

<details>
<summary><b>More detail · For the coding agent</b></summary>

Preserve the spreadsheet. Use a non-interactive matplotlib backend to save the PNG.
Exclude unreviewed or invalid quantities and report exclusions. Do not combine
incompatible units or merge different products by guesswork. Keep the grouped CSV
so plotted values can be checked. The first five receipts are not a random sales sample.

</details>
"""),
        question(21, "receipt_chart_reading", "Read the chart",
                 "What do the two axes show? Which item has the largest total quantity, and what does its bar mean? Check one bar against the spreadsheet.",
                 "The bar sums quantities, not the number of spreadsheet rows. Check the underlying values before interpreting it."),
        question(22, "receipt_analysis_limits", "Know one limitation",
                 "Give one reason why this chart should not be treated as a complete picture of overall sales.",
                 "Only five receipts were used. OCR errors, excluded rows or varying product descriptions can also affect the picture."),
        markdown("""
### Final checkpoint

- [ ] I checked the raw text against the image.
- [ ] I inspected the spreadsheet and checked a product calculation.
- [ ] I accounted for five receipts.
- [ ] I can explain the chart and one limitation.
"""),
    ]
