from llm_workshop.worksheet import (
    _read_answers,
    _write_answers,
    model_comparison_box,
)


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


def test_invalid_answer_file_is_treated_as_empty(tmp_path):
    path = tmp_path / "answers.json"
    path.write_text("not-json", encoding="utf-8")

    assert _read_answers(path) == {}


def test_model_comparison_button_saves_both_responses(tmp_path):
    path = tmp_path / "answers.json"
    box = model_comparison_box("logic", answers_path=path)
    box.children[1].value = "Model A"
    box.children[2].value = "Nine sheep remain."
    box.children[4].value = "Model B"
    box.children[5].value = "Arrr, nine!"
    box.children[6].value = "Both were correct; the tone differed."

    box.children[7].click()

    assert _read_answers(path)["logic"] == {
        "model_a": "Model A",
        "answer_a": "Nine sheep remain.",
        "model_b": "Model B",
        "answer_b": "Arrr, nine!",
        "observation": "Both were correct; the tone differed.",
    }
