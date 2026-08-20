"""Provider-neutral chat helpers for the classroom notebook.

The live providers all expose an OpenAI-compatible ``/v1`` API.  This keeps
the notebook UI identical whether the model is hosted locally, behind a
classroom gateway, or by a cloud provider.  Demo mode is deterministic and
never makes a network request.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from html import escape
import os
from pathlib import Path
from typing import Callable, Mapping, MutableSequence, Sequence


Message = dict[str, str]
Responder = Callable[[Sequence[Message], "ProviderConfig"], str]


class ConfigurationError(ValueError):
    """Raised when a live provider is missing required environment values."""


@dataclass(frozen=True)
class ProviderConfig:
    """Connection settings for one demo or OpenAI-compatible provider."""

    provider: str
    model: str
    api_key: str | None = None
    base_url: str | None = None

    @property
    def is_demo(self) -> bool:
        return self.provider == "demo"

    @property
    def label(self) -> str:
        return f"{self.provider} / {self.model}"


def load_environment(path: str | Path = ".env") -> bool:
    """Load a local ``.env`` file without replacing existing environment values."""

    from dotenv import load_dotenv

    return bool(load_dotenv(dotenv_path=Path(path), override=False))


def load_config(
    provider: str | None = None,
    environ: Mapping[str, str] | None = None,
) -> ProviderConfig:
    """Build a validated provider configuration from environment variables.

    ``cloud`` is accepted as a friendly alias for ``openai``.  Demo mode needs
    no credentials and is deliberately the default.
    """

    env = os.environ if environ is None else environ
    selected = (provider or env.get("LLM_PROVIDER", "demo")).strip().lower()
    selected = "openai" if selected == "cloud" else selected

    if selected == "demo":
        return ProviderConfig(provider="demo", model="offline-demo")

    prefixes = {
        "openai": "OPENAI",
        "local": "LOCAL_LLM",
        "classroom": "CLASSROOM",
        "custom": "CUSTOM_LLM",
    }
    if selected not in prefixes:
        choices = ", ".join(["demo", *prefixes])
        raise ConfigurationError(
            f"Unknown LLM_PROVIDER {selected!r}. Choose one of: {choices}."
        )

    prefix = prefixes[selected]
    model = env.get(f"{prefix}_MODEL", "").strip()
    api_key = env.get(f"{prefix}_API_KEY", "").strip()
    base_url = env.get(f"{prefix}_BASE_URL", "").strip() or None

    missing: list[str] = []
    if not model:
        missing.append(f"{prefix}_MODEL")
    if not api_key:
        missing.append(f"{prefix}_API_KEY")
    if selected != "openai" and not base_url:
        missing.append(f"{prefix}_BASE_URL")
    if missing:
        raise ConfigurationError(
            f"Provider {selected!r} needs: {', '.join(missing)}. "
            "Add them to .env or Codespaces secrets."
        )

    return ProviderConfig(
        provider=selected,
        model=model,
        api_key=api_key,
        base_url=base_url,
    )


def _validate_messages(messages: Sequence[Message]) -> None:
    if not messages:
        raise ValueError("At least one message is required.")
    valid_roles = {"system", "user", "assistant"}
    for message in messages:
        if message.get("role") not in valid_roles:
            raise ValueError(f"Invalid message role: {message.get('role')!r}")
        if not isinstance(message.get("content"), str):
            raise ValueError("Every message needs string content.")


def _demo_complete(messages: Sequence[Message]) -> str:
    latest = next(
        (message["content"] for message in reversed(messages) if message["role"] == "user"),
        "",
    )
    turn_count = sum(message["role"] == "user" for message in messages)
    preview = " ".join(latest.split())[:120]
    return (
        f"Demo assistant (turn {turn_count}): I received ‘{preview}’. "
        "A live model would answer here using the same chat history. "
        "Try making the request more specific by adding a goal, context, and output format."
    )


def complete(
    messages: Sequence[Message],
    config: ProviderConfig,
    *,
    temperature: float = 0.2,
    max_tokens: int = 500,
) -> str:
    """Return one assistant message without exposing credentials in output."""

    _validate_messages(messages)
    if config.is_demo:
        return _demo_complete(messages)

    # Import lazily so offline demo mode remains useful during setup.
    from openai import OpenAI

    client_kwargs: dict[str, str] = {"api_key": config.api_key or ""}
    if config.base_url:
        client_kwargs["base_url"] = config.base_url
    client = OpenAI(**client_kwargs)
    response = client.chat.completions.create(
        model=config.model,
        messages=list(messages),
        temperature=temperature,
        max_tokens=max_tokens,
    )
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("The provider returned an empty assistant message.")
    return content


@dataclass
class ChatSession:
    """A minimal in-memory conversation with explicit, inspectable history."""

    config: ProviderConfig
    system_prompt: str = "You are a concise and helpful classroom assistant."
    responder: Responder = complete
    history: MutableSequence[Message] = field(default_factory=list)

    @property
    def messages(self) -> list[Message]:
        return [
            {"role": "system", "content": self.system_prompt},
            *[dict(message) for message in self.history],
        ]

    def send(self, text: str) -> str:
        cleaned = text.strip()
        if not cleaned:
            raise ValueError("Enter a message before sending.")
        user_message = {"role": "user", "content": cleaned}
        reply = self.responder([*self.messages, user_message], self.config)
        self.history.extend(
            [user_message, {"role": "assistant", "content": reply}]
        )
        return reply

    def reset(self) -> None:
        self.history.clear()


def _render_history(history: Sequence[Message]) -> str:
    if not history:
        return "<p><em>No messages yet. Start the conversation below.</em></p>"
    blocks = []
    for message in history:
        role = "You" if message["role"] == "user" else "Assistant"
        content = escape(message["content"]).replace("\n", "<br>")
        blocks.append(f"<p><strong>{role}:</strong> {content}</p>")
    return "".join(blocks)


def build_chat_widget(session: ChatSession):
    """Create a small ipywidgets chatbox bound to ``session``."""

    import ipywidgets as widgets

    heading = widgets.HTML(
        f"<b>Provider:</b> {escape(session.config.label)}"
    )
    transcript = widgets.HTML(value=_render_history(session.history))
    entry = widgets.Textarea(
        placeholder="Write a message…",
        layout=widgets.Layout(width="100%", height="80px"),
    )
    send = widgets.Button(description="Send", button_style="primary")
    reset = widgets.Button(description="Reset")
    status = widgets.HTML(value="<small>Ready.</small>")

    def on_send(_button) -> None:
        send.disabled = True
        status.value = "<small>Thinking…</small>"
        try:
            session.send(entry.value)
        except Exception as exc:  # Display a useful classroom error without secrets.
            status.value = f"<small style='color:#b42318'>{escape(str(exc))}</small>"
        else:
            entry.value = ""
            transcript.value = _render_history(session.history)
            status.value = "<small>Ready.</small>"
        finally:
            send.disabled = False

    def on_reset(_button) -> None:
        session.reset()
        transcript.value = _render_history(session.history)
        status.value = "<small>Conversation reset.</small>"

    send.on_click(on_send)
    reset.on_click(on_reset)
    controls = widgets.HBox([send, reset])
    return widgets.VBox([heading, transcript, entry, controls, status])
