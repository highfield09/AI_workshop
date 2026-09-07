import json
import re

import pytest

from llm_workshop import course
from llm_workshop.presentation import readable_html
from llm_workshop.worksheet import worksheet_box
from scripts.build_course_notebook import build_workbooks


def test_split_boundaries_and_independent_setup():
    books = build_workbooks()
    assert list(books) == [x[0] for x in course.WORKBOOKS]
    expected_counts = [2, 5, 7, 0, 2]
    for (stem, _, questions), count in zip(course.WORKBOOKS, expected_counts):
        book = books[stem]
        setups = [c for c in book.cells if "setup" in c.metadata.get("tags", [])]
        assert len(setups) == 1
        assert book.cells[1] is setups[0]
        assert "WORKSHOP_ROOT" in setups[0].source
        assert "from llm_workshop.course import answer_path" in setups[0].source
        worksheets = [c for c in book.cells if c.cell_type == "code" and "worksheet_box(" in c.source]
        assert len(worksheets) == count
        for cell in worksheets:
            assert f"answers_path=answer_path({stem!r})" in cell.source
            assert cell.metadata.jupyter.source_hidden
        all_sources = "\n".join(c.source for c in book.cells)
        labels = set(map(int, re.findall(r"QUESTION (\d+) ·", all_sources)))
        assert labels == (set(range(questions[0], questions[1] + 1)) if questions else set())
        assert "tasks/workbook_answers.json" not in all_sources
        assert "outputs/notebook1/catalogue.html" not in all_sources
        for cell in book.cells:
            if cell.cell_type == "code":
                compile(cell.source, stem, "exec")
            else:
                assert 'class="workshop-reading"' in cell.source
    assert "expected-error" in str(books["04_debugging"])
    assert "expected-error" not in str(books["05_shopping_catalogue"])


def test_workspaces_and_workbooks_do_not_share_answers(tmp_path, monkeypatch):
    monkeypatch.delenv("WORKSHOP_DEMO_ANSWERS", raising=False)
    destinations = []
    for student in ("student-a", "student-b"):
        monkeypatch.setattr(course, "ROOT", tmp_path / student)
        for stem in ("01_start_here", "02_models_and_reasoning"):
            path = course.answer_path(stem)
            destinations.append(path)
            box = worksheet_box("same-id", question_label="Test", answers_path=path)
            assert box.children[1].children[1].value == ""
            box.children[1].children[1].value = f"{student}/{stem}"
            box.children[2].click()
    assert len(set(destinations)) == 4
    for path in destinations:
        saved = json.loads(path.read_text())
        assert saved["same-id"]["response"] == f"{path.parents[2].name}/{path.parent.name}"


def test_demo_answers_ignore_existing_personal_work(tmp_path, monkeypatch):
    monkeypatch.setattr(course, "ROOT", tmp_path / "student")
    monkeypatch.delenv("WORKSHOP_DEMO_ANSWERS", raising=False)
    personal = course.answer_path("01_start_here")
    personal.parent.mkdir(parents=True)
    personal.write_text('{"q": {"response": "PRIVATE TEST ANSWER"}}')
    before = personal.read_bytes()
    monkeypatch.setenv("WORKSHOP_DEMO_ANSWERS", str(tmp_path / "demo"))
    demo = course.answer_path("01_start_here")
    box = worksheet_box("q", question_label="Test", answers_path=demo)
    assert demo != personal
    assert box.children[1].children[1].value == ""
    assert personal.read_bytes() == before
    assert str(tmp_path) not in box.children[3].value


def test_unknown_workbook_cannot_escape_answer_root():
    with pytest.raises(ValueError):
        course.answer_path("../../someone-else")


def test_reading_surface_has_explicit_colours_and_scoped_styles():
    html = readable_html("<p>A clear instruction</p>")
    assert 'style="background:#FFFFFF;color:#1D2939;' in html
    assert ".workshop-reading a" in html
    assert "color:#1849A9" in html
    assert ".workshop-widget textarea" in html
    assert "color-scheme:light" in html


@pytest.mark.parametrize("foreground,background", [
    ("1D2939", "FFFFFF"), ("344054", "EFF8FF"), ("1849A9", "FFFFFF"),
    ("FFFFFF", "175CD3"), ("FFFFFF", "067647"), ("B54708", "FFFAEB"),
    ("5925DC", "F4F3FF"), ("B42318", "FEF3F2"), ("667085", "F8FAFC"),
])
def test_core_text_colours_meet_wcag_aa_contrast(foreground, background):
    def luminance(colour):
        channels = [int(colour[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        linear = [c / 12.92 if c <= 0.04045 else ((c + .055) / 1.055) ** 2.4 for c in channels]
        return sum(c * w for c, w in zip(linear, (.2126, .7152, .0722)))
    lighter, darker = sorted([luminance(foreground), luminance(background)], reverse=True)
    assert (lighter + .05) / (darker + .05) >= 4.5
