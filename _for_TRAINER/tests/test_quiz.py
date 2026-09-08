from llm_workshop.quiz import readme_quiz


def test_wrong_answer_turns_quiz_red():
    quiz = readme_quiz()
    quiz.children[1].value = "syntax"

    quiz.children[2].click()

    assert "#FEF3F2" in quiz.children[0].value
    assert "Not quite" in quiz.children[3].value
    assert quiz.layout.border == "2px solid #F04438"
    assert quiz.children[2].button_style == "danger"


def test_correct_answer_turns_quiz_green_and_reveals_widget_note():
    quiz = readme_quiz()
    assert quiz.children[1].layout.min_height == "96px"
    assert quiz.children[1].layout.overflow == "visible"
    quiz.children[1].value = "workflow"

    quiz.children[2].click()

    assert "#ECFDF3" in quiz.children[0].value
    assert "QUESTION 1" in quiz.children[0].value
    assert "Correct" in quiz.children[3].value
    assert "READ THE README FIRST" in quiz.children[3].value
    assert "ipywidgets" in quiz.children[3].value
    assert quiz.layout.border == "2px solid #12B76A"
    assert quiz.children[2].button_style == "success"
    assert quiz.layout.max_width == "100%"
    assert quiz.layout.min_width == "0"
