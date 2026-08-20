import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "notebook1"


def test_catalogue_csv_maps_six_unique_images():
    with (DATA_DIR / "products.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 6
    assert len({row["id"] for row in rows}) == 6
    assert len({row["image"] for row in rows}) == 6
    for row in rows:
        image = DATA_DIR / row["image"]
        assert image.suffix == ".png"
        assert image.is_file()
        assert image.stat().st_size > 100_000
        assert float(row["price"]) > 0
