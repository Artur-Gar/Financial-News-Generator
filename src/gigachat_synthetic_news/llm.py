"""GigaChat integration primitives."""

from __future__ import annotations

from pathlib import Path

from .config import load_settings


def _resolve_credentials(
    creds: str | None,
    model: str | None,
    config_path: str | Path | None = None,
) -> tuple[str, str]:
    settings = load_settings(config_path)
    return creds or settings.creds, model or settings.model


def _langchain_symbols():
    try:
        from langchain.chat_models.gigachat import GigaChat
        from langchain.schema import HumanMessage, SystemMessage
    except ImportError as exc:
        raise ImportError(
            "langchain with GigaChat support is required. "
            "Install dependencies from requirements.txt."
        ) from exc

    return GigaChat, HumanMessage, SystemMessage


class gigachat_stub:
    """Warm-up request; keeps compatibility with the original notebook code."""

    def __init__(
        self,
        creds: str | None = None,
        model: str | None = None,
        config_path: str | Path | None = None,
    ):
        self.creds, self.model = _resolve_credentials(creds, model, config_path)

    def __call__(self) -> str:
        GigaChat, HumanMessage, SystemMessage = _langchain_symbols()

        messages = [
            SystemMessage(content="You are the editor of a business magazine focused on investments and finance."),
            HumanMessage(content="Tell me about the company Rosbank."),
        ]

        try:
            chat = GigaChat(
                credentials=self.creds,
                verify_ssl_certs=False,
                model=self.model,
                scope="GIGACHAT_API_CORP",
                profanity_check="false",
                temperature=0.5,
                max_tokens=10,
            )
            res = chat(messages)
        except Exception:
            chat = GigaChat(
                credentials=self.creds,
                verify_ssl_certs=False,
                model="GigaChat-Pro",
                scope="GIGACHAT_API_CORP",
                profanity_check="false",
                temperature=0.5,
                max_tokens=10,
            )
            res = chat(messages)

        print(res.content)
        return res.content


def llm_output(
    text_news: str,
    system_prompt_template: str,
    prompt_template: str,
    temperature: float,
    creds: str | None = None,
    model: str | None = None,
    config_path: str | Path | None = None,
) -> str:
    """Generate one response from GigaChat."""
    GigaChat, HumanMessage, SystemMessage = _langchain_symbols()
    resolved_creds, resolved_model = _resolve_credentials(creds, model, config_path)

    messages = [SystemMessage(content=system_prompt_template)]
    messages.append(HumanMessage(content=prompt_template.format(text_news)))

    chat = GigaChat(
        credentials=resolved_creds,
        verify_ssl_certs=False,
        model=resolved_model,
        scope="GIGACHAT_API_CORP",
        profanity_check="false",
        temperature=temperature,
        max_tokens=1024,
        top_p=0.1,
        update_interval=2,
    )
    res = chat(messages)
    return res.content
