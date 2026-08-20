import pytest

from llm_workshop.chat import (
    ChatSession,
    ConfigurationError,
    ProviderConfig,
    _render_history,
    complete,
    load_config,
)


def test_demo_is_the_safe_default():
    config = load_config(environ={})

    assert config == ProviderConfig(provider="demo", model="offline-demo")
    assert config.is_demo


def test_cloud_alias_loads_openai_settings():
    config = load_config(
        provider="cloud",
        environ={"OPENAI_API_KEY": "test-key", "OPENAI_MODEL": "test-model"},
    )

    assert config.provider == "openai"
    assert config.base_url is None
    assert config.api_key == "test-key"


def test_live_provider_reports_every_missing_setting():
    with pytest.raises(ConfigurationError) as error:
        load_config(provider="local", environ={})

    assert "LOCAL_LLM_MODEL" in str(error.value)
    assert "LOCAL_LLM_API_KEY" in str(error.value)
    assert "LOCAL_LLM_BASE_URL" in str(error.value)


def test_demo_completion_is_deterministic_and_counts_turns():
    config = load_config(environ={})
    messages = [
        {"role": "system", "content": "Be helpful."},
        {"role": "user", "content": "Explain temperature."},
    ]

    first = complete(messages, config)
    second = complete(messages, config)

    assert first == second
    assert "turn 1" in first
    assert "Explain temperature" in first


def test_session_adds_memory_only_after_successful_reply():
    seen = []

    def fake_responder(messages, _config):
        seen.extend(messages)
        return "A short answer."

    session = ChatSession(load_config(environ={}), responder=fake_responder)
    reply = session.send("  Hello  ")

    assert reply == "A short answer."
    assert seen[-1] == {"role": "user", "content": "Hello"}
    assert session.history == [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "A short answer."},
    ]


def test_transcript_escapes_untrusted_html():
    rendered = _render_history(
        [{"role": "user", "content": "<script>alert(1)</script>"}]
    )

    assert "<script>" not in rendered
    assert "&lt;script&gt;" in rendered
