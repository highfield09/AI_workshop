from html import unescape

from llm_workshop.prompt_card import copyable_prompt


def test_prompt_card_copies_during_the_browser_click_with_fallback():
    card = copyable_prompt("""
        First line.
        Second line.
    """)
    rendered = unescape(card.data)

    assert "First line.\nSecond line." in rendered
    assert "Copy prompt" in rendered
    assert 'addEventListener("click"' in rendered
    assert 'document.execCommand("copy")' in rendered
    assert "navigator.clipboard.writeText(area.value)" in rendered
    assert "Ctrl+C" in rendered
    assert "width:100%;max-width:100%" in rendered
