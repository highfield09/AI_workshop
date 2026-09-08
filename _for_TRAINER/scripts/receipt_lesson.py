"""Four small iterations: transcribe, structure, batch and analyse invoices."""


def receipt_lesson_cells(markdown, code, panel):
    def question(number, key, title, prompt, tip):
        return code(f'''worksheet_box(
    {key!r},
    question_label={f"QUESTION {number} · {title}"!r},
    response_label={prompt!r},
    reveal_html={panel("TAKEAWAY", tip, "success")!r},
)''', "interactive")

    return [
        markdown(f"""
## From invoice images to a checked chart

{panel("DATASET AND CREDIT", "<b>High-Quality Invoice Images for OCR</b>, uploaded by "
    "<b>osama hosam Abdellatif</b> (<code>osamahosamabdellatif</code>) on "
    "<a href='https://www.kaggle.com/datasets/osamahosamabdellatif/high-quality-invoice-images-for-ocr'>Kaggle</a>. "
    "We use <b>version 3</b> (9 May 2025): the <b>499 images in batch1_1</b> and "
    "matching <b>batch1_1.csv</b>, not the other sub-batches. The listing's licence is "
    "<b>Database: Open Database, Contents: Database Contents</b>. Provenance is in "
    "<code>_for_STUDENT/data/notebook6/README.md</code>.")}

{panel("FOUR SMALL ITERATIONS", "<b>1. Read</b> one whole document into text → "
    "<b>2. Table</b> its items in Excel → <b>3. Repeat</b> for 20 receipts → "
    "<b>4. Explore</b> the checked data in a chart. Improve the same script one "
    "step at a time; inspect each result before moving on.", "task")}

**These source documents are JPG invoice images, not PDFs.** Read the entire
image as a document page. A PDF would first need its pages converted to images;
that extra step is outside this exercise. We call the documents receipts below.

[**GLM-OCR by Z.ai**](https://huggingface.co/zai-org/GLM-OCR) is a document-focused
**vision-language model (VLM)**: it reads an image and generates text or fields.
**OCR** means optical character recognition. The model is MIT-licensed and runs
locally after setup—no inference API key, paid service or GPU is needed.

{panel("BEFORE YOU START", "Use a <b>16 GB RAM</b> laptop environment or Codespace "
    "and allow <b>at least 6 GB spare disk</b> plus possible package-cache space. "
    "The snapshot is about <b>2.66 GB</b>. Our four-thread CPU test took about "
    "<b>115 seconds for full-page text</b> and used <b>6.6 GiB RAM</b>. "
    "Twenty similar pages could take roughly <b>40 minutes</b>, and your hardware "
    "or documents may take longer. Plan a break or a second session. "
    "In Codespaces, the cloud machine supplies the memory. Run one model process at a time.")}

From the repository root, prepare once:

```bash
source .venv/bin/activate
sh _for_TRAINER/scripts/setup_glm_ocr.sh
python _for_TRAINER/scripts/prepare_receipt_data.py
```

The model is downloaded into `_for_STUDENT/tasks/06_receipt_ocr/model/glm-ocr/`.
Model weights, downloaded images and learner outputs are Git-ignored. Downloads
are pinned and checked. If Kaggle requests login, use your own
[Kaggle API token](https://www.kaggle.com/settings/api) as a Codespaces secret
named `KAGGLE_API_TOKEN`; never paste it into a notebook or chat.

Open a fresh Copilot Chat. Use **Agent** mode to create your script, or **Ask**
mode to receive code you paste yourself. Use public classroom documents only.
Your script will be `_for_STUDENT/tasks/06_receipt_ocr/receipt_reader.py`.
Keep the provided model helper and original JPG/CSV files unchanged.
"""),
        markdown(f"""
### Iteration 1 · Read the whole document, then inspect

**Input:** `_for_STUDENT/data/notebook6/batch1_1/batch1-0001.jpg`—first by filename,
not first CSV row. **Output:** `_for_STUDENT/outputs/06_receipt_ocr/raw/batch1-0001.txt`.

Ask your coding agent to create the script to transcribe **all visible text**:
headings, seller/client details, item descriptions, quantities and totals.
Do not request a short list of fields yet. Preserve the raw model response;
do not silently clean or replace it. Do not process the whole folder yet.

<details>
<summary><b>Hint · Build your prompt in small steps</b></summary>

1. Start: "Within `_for_STUDENT/tasks/06_receipt_ocr`, generate a Python script named `receipt_reader.py`. Implement only Iteration 1."
2. Give the input and output paths above. Ask it to find paths relative to the script and create the output folder.
3. Use the supplied helper: `from model.glm_reader import read_image`.
4. Call `read_image(image_path, "Text Recognition:", max_new_tokens=4096, max_time=600)`. No JSON schema is needed for this full-text pass.
5. Save the returned text unchanged and print the destination. If the helper reports an incomplete response, show the error; do not mark it as successful.
6. Ask for the run command. Run the script yourself, then open the text and original image side by side.

</details>

Run the next cell to preview the image. Zoom into the original in Explorer,
then check the text section by section. A model can finish normally and still
miss a clearly printed detail. Do not judge only by how tidy its output looks.
"""),
        code("show_receipt_preview()", "hide-input"),
        question(19, "receipt_full_text_review", "Inspect the full transcription",
                 "Which sections were captured? Identify one missing, changed or uncertain detail, and name the file where you saved the raw text.",
                 "Check the source image, not just a reference answer. A complete-looking response can still omit text; retain the raw output as evidence."),
        markdown(f"""
### Iteration 2 · Turn the checked text into Excel tables

Modify the same script to **reuse the saved text** instead of rerunning the VLM
whenever you change the spreadsheet. Save a new `first_receipt.xlsx` under
`_for_STUDENT/outputs/06_receipt_ocr/`. Keep the raw text unchanged.

| Excel sheet | What one row represents | Columns to request |
|---|---|---|
| **Items** | One purchased line item | `source_file`, `invoice_number`, `line_number`, `description`, `quantity`, `unit`, `unit_net_price`, `line_net_total`, `vat_rate`, `line_gross_total`, `review_status`, `review_note` |
| **Receipts** | One source document | `source_file`, `invoice_number`, `invoice_date`, `seller_name`, `client_name`, `net_total`, `tax_total`, `grand_total`, `currency_mark`, `review_status`, `review_note` |

The first sample has **seven item rows** and **one receipt row**, excluding
headers. Do not repeat an invoice's grand total as though it were each item's price.
Use `unreviewed`, `needs_review` or `checked` in `review_status`. Mark rows
`checked` only after inspecting them against the source; a successful model call
must not automatically count as human review. Preserve review decisions on reruns.

#### Fix number formats—not the evidence

| Printed text | Numeric cell | Meaning |
|---|---|---|
| `3,00` | `3` | Quantity, not three hundred |
| `1 394,67` | `1394.67` | Spaces separate thousands; comma is the decimal mark |
| `10%` | `0.10`, displayed as `10%` | Tax rate, not the tax amount |

Ask for **real numeric Excel cells**, not strings that merely look like numbers.
Do not globally delete commas: that turns `3,00` into `300`. Preserve IDs and
dates as text. For later documents, detect unfamiliar or ambiguous formats and
flag them instead of guessing. Leave missing values blank, not zero. A printed
`$` does not establish a currency country; a **Tax Id** is not a tax amount.

<details>
<summary><b>Hint · Describe a table and its checks</b></summary>

Ask the agent to inspect the saved text, separate each item's description from
its numeric row, convert decimal-comma numbers safely, and write the two sheets
with `openpyxl`. If it uses a JSON schema as an intermediate structure, validate
required keys before exporting. Keep raw strings available for diagnosing errors.
Have it check quantity × unit price against line net total, item gross totals
against the invoice total, and summary net + tax against gross, allowing sensible
cent rounding. Discounts or extra charges on other documents may explain a
difference; flag it rather than rewriting a value to force a match.

Do not re-query GLM-OCR just to change column names or number formatting.

</details>

{panel("KEEP THE CHECK INDEPENDENT", "The reference CSV contains <b>File Name</b>, "
    "<b>Json Data</b> and <b>OCRed Text</b>. Match the source filename when checking "
    "afterwards; its rows are not sorted by image name. Do not let the script copy answers from "
    "the CSV or hard-code inspected values. The CSV may not describe every printed field.", "task")}

Run your script from the repository root:

```bash
python _for_STUDENT/tasks/06_receipt_ocr/receipt_reader.py
```

In **Extensions** (`Ctrl+Shift+X`, or `Command+Shift+X` on macOS), install
[**SpreadJS XLSX Editor** by MESCIUS](https://marketplace.visualstudio.com/items?itemName=Mescius.spreadjs-xlsx-editor)
if needed. Open `first_receipt.xlsx` in Explorer; use **Open With…** to select
the spreadsheet editor if necessary. Inspect both sheet tabs. No desktop Excel
installation is required. The next cell also previews both sheets after your
script creates them; it does not create answers for you.
"""),
        code('preview_spreadsheet(sheet_name="Items")\npreview_spreadsheet(sheet_name="Receipts")', "hide-input"),
        question(20, "receipt_numeric_cleaning", "Check the numbers",
                 "Explain how your script converted 3,00 and 1 394,67. How did you check that quantities and prices are numeric cells rather than text?",
                 "Cleaning changes representation, not meaning. Keep quantities, money, percentages and identifiers distinct, and preserve the original text."),
        question(21, "receipt_row_structure", "Check the table structure",
                 "How many item rows and receipt rows did you obtain? Which arithmetic check did you perform, and why should invoice totals not be copied into every item row?",
                 "Decide what one row means. Separate item-level and document-level data so sums do not double-count the same invoice."),
        markdown(f"""
### Iteration 3 · Scan and table the first 20 receipts

Only start once the first receipt's text, table and numbers have been checked.
Ask the agent to extend the same script—preserving the working one-receipt option.

- Select JPG files **sorted by filename**, then take the first 20: `batch1-0001.jpg` through `batch1-0020.jpg`. Print that list before starting. Do not process all 499.
- Process sequentially. Reuse the loaded model in the same Python process; the provided helper caches it. Do not start 20 model copies or parallel workers.
- Save one raw text file per image in `outputs/06_receipt_ocr/raw/` under `_for_STUDENT`. Reuse existing successful outputs on rerun; verify each belongs to the current input and settings. Ask explicitly before replacing a cached result.
- Add an audit row per selected file to `batch_run.csv`, recording source filename, `success`/`needs_review`/`failed`, extracted item count and any error. There must be **20 audit rows**, even if fewer documents succeed.
- Write `receipts_20.xlsx` with **Items** and **Receipts** sheets. Keep `source_file` in both and `(source_file, line_number)` unique in Items. Rerunning must not duplicate rows.
- Preserve `first_receipt.xlsx`. Save progress after each document so an interruption does not lose the completed work.
- Do not silently skip missing, unreadable, malformed or incomplete results. Flag missing fields and documents whose layout differs. Do not assume every invoice has seven items or the same tax rate.

<details>
<summary><b>Hint · Ask for a safe batch</b></summary>

Request a preview-only option to list the first 20 files, progress such as
`4/20`, a resumable run, clear errors and a separate audit file. Ask for the
exact command to run the updated script. Reuse saved full text to fix table
parsing without performing OCR again. Check the first, a middle and the final
receipt against their images, plus **every flagged case**. A successful model
call alone is not a successful data-quality check.

</details>

Allow roughly 40 minutes or longer for an uncached CPU run. You can pause here
and return once it finishes. Before analysis, reconcile selected, successful,
flagged and failed counts; record which rows have actually been reviewed.
"""),
        question(22, "receipt_batch_review", "Audit the 20-receipt run",
                 "How many files were selected, successful, flagged and failed? Do those counts account for all 20? Describe one check for duplicates or a changed layout, and where you would resume after an interruption.",
                 "Scaling up also scales mistakes. Keep an audit trail, reuse verified intermediate files, and never disguise failed extraction as an empty sale."),
        markdown(f"""
### Iteration 4 · Make a simple chart from the checked data

Modify the script to analyse **the saved Items sheet**, without running OCR again.
Start with a **bar chart of the top 10 item descriptions by total quantity**.
This is a clearer first choice than a histogram for named products.

1. Use valid positive numeric quantities from rows with `review_status` equal to `checked`. Exclude unresolved, unreviewed or failed records, and report the number excluded. Do not treat missing quantity as zero.
2. Group descriptions after trimming spaces and consistently handling capitalisation. Sum `quantity`—do not just count spreadsheet rows. Use a consistent unit (such as `each`) and report excluded units; do not add packs to individual units without a justified conversion. Do not merge different products just because their names seem similar.
3. Save the grouped values as `item_quantity_summary.csv` and the chart as `item_quantities.png`, both under `_for_STUDENT/outputs/06_receipt_ocr/`.
4. Label the axes **Item description** and **Total quantity**; use a horizontal bar chart if descriptions are long. State how many receipts/items were included and excluded, and any grouping assumptions.
5. Open the PNG in Explorer. Check one bar against the summary CSV and original item rows. Use `matplotlib` to create a saved image; do not require a desktop plotting window.

**Optional histogram:** instead show the distribution of quantity per item row.
Use **Quantity per line item** on the horizontal axis and **Number of item rows**
on the vertical axis. A histogram groups numeric ranges; a bar chart compares
named groups. State your bins and exclusions.

<details>
<summary><b>Hint · Specify the analysis, not just “make a graph”</b></summary>

Name the input workbook/sheet, how to identify reviewed rows, the grouping
column, the quantity to sum, exclusions, chart labels and exact output paths.
Ask the agent to keep OCR as a separate operation and preserve the existing
tables. If item names are mostly unique, say so; the chart may not reveal a
strong pattern. Use the optional histogram instead if it communicates more.

</details>
"""),
        question(23, "receipt_chart_reading", "Explain one result",
                 "What do the axes measure? Pick one bar (or histogram bin), explain its value, and trace it back to the contributing item rows. Is it counting rows or summing quantities?",
                 "A chart should answer a stated question. Verify the aggregation against the underlying rows before interpreting its appearance."),
        question(24, "receipt_analysis_limits", "Know the limits",
                 "Which records did you exclude and why? How could an OCR error, decimal conversion or product-name grouping change the chart? What can this first-20 sample not tell you about wider sales?",
                 "This is an extraction exercise, not representative market research. The first 20 files are not a random sales sample; missing data and grouping choices can distort conclusions."),
        markdown("""
### Final checkpoint

- [ ] Raw text is preserved and can be traced to each source image.
- [ ] Excel has separate item and receipt rows, with numeric quantities and amounts.
- [ ] All 20 selected files are accounted for, including failures and review flags.
- [ ] Reruns reuse appropriate results without duplicating item rows.
- [ ] The chart and summary use checked data and report exclusions.
- [ ] You can trace a plotted value back to its item rows and source receipts.
- [ ] Original JPGs/CSV are unchanged; your script and outputs remain in your own Codespace.
"""),
    ]
