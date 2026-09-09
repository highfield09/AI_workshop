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
    expected_counts = [2, 5, 6, 0, 1, 6]
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
        assert "_for_STUDENT/tasks/workbook_answers.json" not in all_sources
        assert "_for_STUDENT/outputs/notebook1/catalogue.html" not in all_sources
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
        assert saved["same-id"]["response"] == f"{path.parents[3].name}/{path.parent.name}"


def test_workflow_moves_to_catalogue_and_orientation_stays_together():
    books = build_workbooks()
    first = books["01_start_here"]
    catalogue = books["05_shopping_catalogue"]
    assert "The simple workflow" not in "\n".join(c.source for c in first.cells)
    orientation = [c for c in first.cells if "## Find your way around" in c.source]
    assert len(orientation) == 1
    for text in ("You do not need to memorize commands", "COLOUR KEY", "### Five friendly terms"):
        assert text in orientation[0].source
    assert "\n\n### Five friendly terms" in orientation[0].source
    # The first lesson cell follows the workbook header and hidden setup.
    opening = catalogue.cells[2].source
    assert "### The simple workflow" in opening
    for number, verb in enumerate(("Look", "Describe", "Ask", "Make", "Open", "Refine"), 1):
        assert f"{number}. **{verb}**" in opening
    assert opening.index("The simple workflow") < opening.index("WORKBOOK 5 · MAIN")
    assert sum("The simple workflow" in c.source for book in books.values() for c in book.cells) == 1


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


def test_resource_introductions_are_in_the_matching_workbook():
    books = build_workbooks()
    first = "\n".join(c.source for c in books["01_start_here"].cells)
    second = "\n".join(c.source for c in books["02_models_and_reasoning"].cells)
    assert "## Try the AI interface · Google AI Mode" in first
    assert "HuggingChat allowance" not in first
    assert "20 questions" not in first
    assert "## Try the AI interface · HuggingChat" in second
    assert "HuggingChat allowance" in second
    assert second.index("## Try the AI interface") < second.index("### HuggingChat models")
    assert "tasks → 02_models_and_reasoning → answers.json" in second


def test_q4_reveals_source_checking_tip_only_after_save(tmp_path):
    book = build_workbooks()["01_start_here"]
    cell = next(c for c in book.cells if c.cell_type == "code" and '"google_fact_source"' in c.source)
    destination = tmp_path / "answers.json"
    box = eval(cell.source, {"worksheet_box": worksheet_box, "answer_path": lambda _: destination})
    assert box.children[4].value == ""
    assert box.children[4].layout.display == "none"
    box.children[1].children[1].value = "About 71%; checked the original source."
    box.children[2].click()
    assert destination.is_file()
    assert box.children[4].layout.display == "block"
    assert "KEY TIP · ASK FOR A CITATION" in box.children[4].value
    assert "open it and check" in box.children[4].value
    assert "#ECFDF3" in box.children[4].value


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
