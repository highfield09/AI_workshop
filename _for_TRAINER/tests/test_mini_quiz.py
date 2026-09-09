import pytest

from llm_workshop.mini_quiz import QUESTIONS, mini_quiz
from llm_workshop.quiz import readme_quiz
from scripts.build_course_notebook import build_workbooks


@pytest.mark.parametrize("stem", QUESTIONS)
def test_quiz_feedback_retry_and_no_preselected_answers(stem):
    quiz = mini_quiz(stem)
    cards = quiz.children[1:5]
    submit, summary = quiz.children[-2:]
    assert len(QUESTIONS[stem]) == 4
    assert all(card.children[1].value is None for card in cards)
    submit.click()
    assert "4 unanswered" in summary.value
    for card, (_, options, answer, explanation) in zip(cards, QUESTIONS[stem]):
        assert 0 <= answer < len(options)
        card.children[1].value = (answer + 1) % len(options)
    submit.click()
    assert "0/4 correct" in summary.value
    assert all("Not quite" in card.children[2].value for card in cards)
    for card, (_, _, answer, _) in zip(cards, QUESTIONS[stem]):
        card.children[1].value = answer
    assert "Submit to check" in summary.value
    submit.click()
    assert "4/4 correct" in summary.value
    assert all("Correct!" in card.children[2].value for card in cards)
    assert all(card.children[1].value is None for card in mini_quiz(stem).children[1:5])


def test_quizzes_are_hidden_end_of_lesson_cells_except_workbook_five():
    for stem, book in build_workbooks().items():
        indices = [i for i, cell in enumerate(book.cells) if "mini-quiz" in cell.metadata.get("tags", [])]
        if stem == "05_shopping_catalogue":
            assert not indices
            continue
        assert len(indices) == 1
        index = indices[0]
        assert index >= len(book.cells) - 2
        assert book.cells[index].metadata.jupyter.source_hidden
        assert book.cells[index].source == f"mini_quiz({stem!r})"
        assert "from llm_workshop.mini_quiz import mini_quiz" in book.cells[1].source


def test_resource_paths_vision_followups_and_billing_location():
    books = build_workbooks()
    assert "https://huggingface.co/chat/models" in books["02_models_and_reasoning"].cells[0].source
    vision = "\n".join(c.source for c in books["03_vision_and_context"].cells)
    debugging = "\n".join(c.source for c in books["04_debugging"].cells)
    assert "- **Route:**" not in vision
    assert "What programs can be used to visualise and generate these files?" in vision
    assert "_for_STUDENT/data/notebook3/" in vision
    assert "KEY CONCEPT · CONTEXT IS A RUNNING WINDOW" in vision
    assert "Compare with GitHub-provided Copilot usage" not in vision
    assert "Compare with GitHub-provided Copilot usage" not in debugging
    assert "TRACE THE PROVIDER" not in vision
    question = readme_quiz().children[0].value
    assert "./README.md" in question
    assert "_for_STUDENT/" in question and "_for_TRAINER/" in question


def test_model_observations_and_ec_claims_are_inside_the_worksheets():
    book = build_workbooks()["02_models_and_reasoning"]
    q8 = next(c for c in book.cells if 'question_label="QUESTION 8' in c.source)
    q9 = next(c for c in book.cells if 'question_label="QUESTION 9' in c.source)
    assert q8.source.count("<li>") == 4
    assert "other formatting?" in q8.source
    assert not any("While both models work" in c.source for c in book.cells if c.cell_type == "markdown")
    for text in ("EC 1.14.19.17", "EC 1.14.18.6", "enzyme.expasy.org/EC/1.14.18.5"):
        assert text in q9.source.split("reveal_html=")[0]


def test_agent_gif_exercise_fails_then_runs_with_one_name_repair(monkeypatch):
    import IPython.display
    book = build_workbooks()["04_debugging"]
    errors = [c for c in book.cells if "expected-error" in c.metadata.get("tags", [])]
    assert len(errors) == 2
    cell = next(c for c in errors if "agent-repair" in c.metadata.tags)
    with pytest.raises(NameError, match="Images"):
        exec(cell.source, {})
    shown = []
    monkeypatch.setattr(IPython.display, "display", shown.append)
    exec(cell.source.replace("display(Images(", "display(Image("), {})
    assert len(shown) == 1
    assert shown[0].width == 300
    assert shown[0].url == "https://media.giphy.com/media/sIIhZliB2McAo/giphy.gif"
    assert "<img" in shown[0]._repr_html_()
    source = "\n".join(c.source for c in book.cells)
    assert source.index("Experiment 5B") < source.index("mini_quiz(")


def test_openrouter_setup_and_cost_caveat_are_explicit():
    book = build_workbooks()["03_vision_and_context"]
    source = "\n".join(c.source for c in book.cells)
    assert "generate a key and click <b>Copy</b>" in source
    assert "Manage Models" in source and "Add Models → OpenRouter" in source
    assert "4. Drag **Screenshot" in source
    assert "free account does" in source
    assert "not** make every model free" in source
    assert "prices shown will not be charged" not in source


def test_removed_worksheets_and_updated_paths():
    books = build_workbooks()
    all_sources = "\n".join(c.source for b in books.values() for c in b.cells)
    assert "vision_cost" not in all_sources
    assert "catalogue_brief_prompt" not in all_sources
    assert "image_source.txt" not in all_sources
    assert "data/notebook1/" not in all_sources
    assert "data/notebook3/Screenshot" in all_sources
    assert "../../data/notebook5/products.csv" in all_sources
    assert "Before editing SBML" not in all_sources
    book = books["02_models_and_reasoning"]
    answer = next(i for i,c in enumerate(book.cells) if '"ec_number_fact_check"' in c.source)
    explanation = next(i for i,c in enumerate(book.cells) if "QUESTION 9 · FACT-CHECK THE EC NUMBERS" in c.source)
    assert explanation == answer + 1
    assert "EC 1.14.18.<b>5</b>" in book.cells[answer].source


def test_fair_comparison_and_vision_quiz_answers():
    q = QUESTIONS["02_models_and_reasoning"][1]
    assert q[1][q[2]] == "Give each model the same task and evaluation criteria"
    assert "Prompts may be adapted" in q[3]
    vision = QUESTIONS["03_vision_and_context"]
    assert vision[0][2] == 0 and "supports vision" in vision[0][1][0]
    assert vision[3][2] == 0 and "tokens processed" in vision[3][1][0]
