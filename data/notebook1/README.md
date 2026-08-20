# Notebook 1 catalogue data

This folder is the input for the main task in `notebooks/01_start_here.ipynb`.

- `products.csv` maps 18 product records to 18 PNG image filenames.
- `ASSET_PROMPTS.md` records the image-generation brief used for the set.
- The rows contain six product families with three colour variants each.
- Core card fields are `image`, `name`, `brand`, `type`, and `price`.
- Optional fields are `colour`, `release_date`, `sizes`, `country_of_origin`, and `designer`.
- `sizes` uses a `|` separator so several sizes fit safely inside one CSV field.
- ISO dates (`YYYY-MM-DD`) can be sorted without first changing their format.
- The pixel-art images are original workshop assets generated for this exercise.

The student's HTML output belongs at `tasks/notebook1/catalogue.html`.
