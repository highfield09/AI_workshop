from llm_workshop.worksheet import (
    _read_answers,
    _write_answers,
    effort_comparison_box,
    model_comparison_box,
    worksheet_box,
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
    box.children[2].children[1].value = "Nine sheep remain."
    box.children[4].value = "Model B"
    box.children[5].children[1].value = "Arrr, nine!"
    box.children[6].children[1].value = "Both were correct; the tone differed."

    box.children[7].click()

    assert _read_answers(path)["logic"] == {
        "model_a": "Model A",
        "answer_a": "Nine sheep remain.",
        "model_b": "Model B",
        "answer_b": "Arrr, nine!",
        "observation": "Both were correct; the tone differed.",
    }
    assert "Saved" in box.children[8].value
    assert path.as_posix() in box.children[8].value
    assert box.layout.border == "2px solid #12B76A"


def test_long_worksheet_label_is_shown_above_field(tmp_path):
    path = tmp_path / "answers.json"
    label = "Which answer seems more well put together or informative?"

    box = worksheet_box(
        "reflection",
        observation_label=label,
        answers_path=path,
    )

    assert label in box.children[1].children[0].value
    assert box.children[1].children[1].description == ""
    assert box.layout.max_width == "100%"
    assert box.layout.min_width == "0"


def test_single_answer_submission_saves_and_points_to_output(tmp_path):
    path = tmp_path / "answers.json"
    box = worksheet_box("fact", answers_path=path)
    box.children[0].children[1].value = "Plants need light, water, and nutrients."
    box.children[1].children[1].value = "It was clear."

    box.children[2].click()

    assert _read_answers(path)["fact"] == {
        "answer": "Plants need light, water, and nutrients.",
        "observation": "It was clear.",
    }
    assert path.as_posix() in box.children[3].value
    assert "VS Code Explorer" in box.children[3].value


def test_effort_comparison_saves_answers_and_token_counts(tmp_path):
    path = tmp_path / "answers.json"
    box = effort_comparison_box(
        "castle_effort",
        model_name="Gemini 3.6 Flash",
        answers_path=path,
    )
    box.children[1].children[1].value = "Low-effort castle"
    box.children[2].children[0].value = "120"
    box.children[2].children[1].value = "210"
    box.children[4].children[1].value = "High-effort castle"
    box.children[5].children[0].value = "120"
    box.children[5].children[1].value = "450"
    box.children[6].children[1].value = "High followed every rule."

    box.children[7].click()

    assert _read_answers(path)["castle_effort"] == {
        "model": "Gemini 3.6 Flash",
        "low": {
            "effort": "Low",
            "answer": "Low-effort castle",
            "input_tokens": "120",
            "output_tokens": "210",
        },
        "high": {
            "effort": "High",
            "answer": "High-effort castle",
            "input_tokens": "120",
            "output_tokens": "450",
        },
        "observation": "High followed every rule.",
    }
    assert box.layout.border == "2px solid #12B76A"
