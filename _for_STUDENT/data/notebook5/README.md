# Notebook 5 catalogue data

This folder is the input for the main task in `_for_STUDENT/notebooks/05_shopping_catalogue.ipynb`.

- `products.csv` contains 18 product records and 18 unique image references.
- Product IDs are deliberately shuffled rather than stored in numerical order.
- Inspect the image paths and the number of fields in each row to find the two controlled data problems.
- These controlled imperfections are part of the lesson. Do not repair the source before learners observe and handle them.
- `ASSET_PROMPTS.md` records the image-generation brief used for the set.
- The rows contain six product families with three colour variants each.
- Core card fields are `image`, `name`, `brand`, `type`, and `price`.
- Optional fields are `colour`, `release_date`, `sizes`, `country_of_origin`, and `designer`.
- `sizes` uses a `|` separator so several sizes fit safely inside one CSV field.
- ISO dates (`YYYY-MM-DD`) can be sorted without first changing their format.
- The pixel-art images are original workshop assets generated for this exercise.

The student's HTML output belongs at `_for_STUDENT/outputs/05_shopping_catalogue/catalogue.html`.
