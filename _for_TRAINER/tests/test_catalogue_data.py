import csv
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "_for_STUDENT" / "data" / "notebook5"

EXPECTED_MESSY_ID_ORDER = [
    "NB014",
    "NB006",
    "NB015",
    "NB018",
    "NB002",
    "NB005",
    "NB003",
    "NB011",
    "NB008",
    "NB007",
    "NB016",
    "NB013",
    "NB017",
    "NB001",
    "NB004",
    "NB012",
    "NB009",
    "NB010",
]

def load_rows():
    with (DATA_DIR / "products.csv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_catalogue_csv_maps_eighteen_unique_images():
    rows = load_rows()

    assert len(rows) == 18
    ids = [row["id"] for row in rows]
    assert set(ids) == {f"NB{number:03d}" for number in range(1, 19)}
    assert ids == EXPECTED_MESSY_ID_ORDER
    assert len({row["image"] for row in rows}) == 18
    assert set(Counter(row["type"] for row in rows).values()) == {3}

    missing_images = []
    for row in rows:
        image = DATA_DIR / row["image"]
        assert image.suffix == ".png"
        if image.is_file():
            assert image.stat().st_size > 100_000
        else:
            missing_images.append(row["image"])
        assert float(row["price"]) > 0

    assert missing_images == ["ice-harbour-jacket.png"]
    assert (DATA_DIR / "ice-jacket.png").is_file()


def test_catalogue_contains_one_controlled_merged_metadata_row():
    rows = load_rows()

    malformed = [row for row in rows if row["sizes"] is None]
    assert [row["id"] for row in malformed] == ["NB012"]
    assert len(malformed[0]["release_date"]) > 100
    assert malformed[0]["country_of_origin"] is None
    assert malformed[0]["designer"] is None

    for row in rows:
        assert row["colour"]
        if row["id"] == "NB012":
            continue
        assert date.fromisoformat(row["release_date"])
        assert row["sizes"]
        assert row["country_of_origin"]
        assert row["designer"]
