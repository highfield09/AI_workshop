from llm_workshop.quiz import stage1_quiz


def test_wrong_answer_turns_quiz_red():
    quiz = stage1_quiz()
    quiz.children[1].value = "notebooks"

    quiz.children[2].click()

    assert "#FEF3F2" in quiz.children[0].value
    assert "Not quite" in quiz.children[3].value
    assert quiz.layout.border == "2px solid #F04438"
    assert quiz.children[2].button_style == "danger"


def test_correct_answer_turns_quiz_green_and_reveals_widget_note():
    quiz = stage1_quiz()
    quiz.children[1].value = "data"

    quiz.children[2].click()

    assert "#ECFDF3" in quiz.children[0].value
    assert "QUESTION S1-Q1" in quiz.children[0].value
    assert "Correct" in quiz.children[3].value
    assert "ipywidgets" in quiz.children[3].value
    assert quiz.layout.border == "2px solid #12B76A"
    assert quiz.children[2].button_style == "success"
    assert quiz.layout.max_width == "100%"
    assert quiz.layout.min_width == "0"
