# Earlier combined-workbook output

The shopping task now lives in Workbook 5. New work should go to
`outputs/05_shopping_catalogue/catalogue.html`. Existing files in this folder
are left untouched. The notes below describe the previous location.

Create `catalogue.html` here during Notebook 1's main task. Ask GitHub Copilot
Chat to return code, then create this file and paste the code yourself.

Open `catalogue.html` in VS Code, right-click inside the editor, and choose
**Open with Live Server**. Serving the page over HTTP lets it load
`../../data/notebook1/products.csv` and resolve image filenames from
`../../data/notebook1/`.

The source is deliberately imperfect: IDs are out of numerical order and one
CSV image reference does not match a file. Keep all 18 products visible and
show a helpful fallback for the missing image rather than deleting the row.

Start with only the core product details. Then use short follow-up prompts to
add or remove metadata, introduce a details toggle, and sort the 18 products.
Make one change at a time and preview after every change.

`catalogue.html` is ignored by Git so each learner can experiment without committing personal work.
