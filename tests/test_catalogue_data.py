import csv
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "notebook1"


def load_rows():
    with (DATA_DIR / "products.csv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_catalogue_csv_maps_eighteen_unique_images():
    rows = load_rows()

    assert len(rows) == 18
    assert len({row["id"] for row in rows}) == 18
    assert len({row["image"] for row in rows}) == 18
    assert set(Counter(row["type"] for row in rows).values()) == {3}
    for row in rows:
        image = DATA_DIR / row["image"]
        assert image.suffix == ".png"
        assert image.is_file()
        assert image.stat().st_size > 100_000
        assert float(row["price"]) > 0


def test_catalogue_rows_include_optional_display_metadata():
    rows = load_rows()

    for row in rows:
        assert row["colour"]
        assert date.fromisoformat(row["release_date"])
        assert row["sizes"]
        assert row["country_of_origin"]
        assert row["designer"]
