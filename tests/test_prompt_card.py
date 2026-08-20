from llm_workshop.prompt_card import copyable_prompt


def test_prompt_card_is_selectable_and_has_copy_icon():
    card = copyable_prompt("""
        First line.
        Second line.
    """)

    assert card.children[1].value == "First line.\nSecond line."
    copy_button = card.children[2].children[0]
    assert copy_button.description == "Copy prompt"
    assert copy_button.icon == "copy"
    assert "Ctrl+A" in card.children[2].children[1].value
