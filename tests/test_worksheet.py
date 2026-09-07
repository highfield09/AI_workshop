import pytest

from llm_workshop.worksheet import _read_answers, _write_answers, worksheet_box


def test_answers_round_trip_as_utf8_json(tmp_path):
    path = tmp_path / "answers.json"
    answers = {
        "translation": {
            "answer": "Knowledge gives humility.",
            "observation": "The wording was concise.",
        }
    }

    _write_answers(path, answers)

    assert _read_answers(path) == answers


@pytest.mark.parametrize("invalid", ["not-json", "[]", "null"])
def test_invalid_answer_file_is_preserved(tmp_path, invalid):
    path = tmp_path / "answers.json"
    path.write_text(invalid, encoding="utf-8")

    with pytest.raises(ValueError):
        _read_answers(path)
    box = worksheet_box("new", question_label="Test", answers_path=path)
    box.children[1].children[1].value = "Keep this response"
    box.children[2].click()
    assert path.read_text() == invalid
    assert "Not saved" in box.children[3].value
    assert box.children[1].children[1].value == "Keep this response"
    assert box.children[2].description != "Saved"


def test_valid_answers_survive_additional_saves_and_reload(tmp_path):
    path = tmp_path / "answers.json"
    _write_answers(path, {"earlier": {"response": "Earlier work"}})
    box = worksheet_box("new", question_label="New", answers_path=path)
    box.children[1].children[1].value = "Later work"
    box.children[2].click()
    assert _read_answers(path)["earlier"]["response"] == "Earlier work"
    reopened = worksheet_box("new", question_label="New", answers_path=path)
    assert reopened.children[1].children[1].value == "Later work"


def test_atomic_save_failure_does_not_destroy_existing_file(tmp_path, monkeypatch):
    path = tmp_path / "answers.json"
    original = '{"earlier": {"response": "Keep me"}}'
    path.write_text(original)
    def fail(*args):
        raise OSError("Simulated write failure")
    monkeypatch.setattr("llm_workshop.worksheet.os.replace", fail)
    box = worksheet_box("new", question_label="New", answers_path=path)
    box.children[2].click()
    assert path.read_text() == original
    assert "Not saved" in box.children[3].value
    assert not list(tmp_path.glob(".answers-*.tmp"))




def test_long_worksheet_label_is_shown_above_field(tmp_path):
    path = tmp_path / "answers.json"
    label = "QUESTION 7 · Compare Answer A with Answer B"

    box = worksheet_box(
        "reflection",
        question_label=label,
        response_label="Which answer is more informative?",
        answers_path=path,
    )

    assert label in box.children[0].value
    assert "Which answer is more informative?" in box.children[1].children[0].value
    assert box.children[1].children[1].description == ""
    assert box.layout.max_width == "100%"
    assert box.layout.min_width == "0"


def test_single_answer_submission_saves_and_points_to_output(tmp_path):
    path = tmp_path / "answers.json"
    label = "QUESTION TEST-Q1 · Plant needs"
    box = worksheet_box("fact", question_label=label, answers_path=path)
    box.children[1].children[1].value = "Plants need light, water, and nutrients."

    box.children[2].click()

    assert _read_answers(path)["fact"] == {
        "question": label,
        "response": "Plants need light, water, and nutrients.",
    }
    assert path.as_posix() in box.children[3].value
    assert "VS Code Explorer" in box.children[3].value


def test_key_tip_stays_hidden_until_submission(tmp_path):
    path = tmp_path / "answers.json"
    box = worksheet_box(
        "tip",
        question_label="QUESTION TEST-Q2 · Explain the change",
        reveal_html="<div><b>KEY TIP</b> Clear targets improve answers.</div>",
        answers_path=path,
    )

    assert box.children[4].layout.display == "none"
    assert box.children[4].value == ""

    box.children[2].click()

    assert box.children[4].layout.display == "block"
    assert "KEY TIP" in box.children[4].value
