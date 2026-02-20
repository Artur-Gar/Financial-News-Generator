"""Public package interface for synthetic news generation with GigaChat."""

from .config import DEFAULT_CONFIG_PATH, PROJECT_ROOT, Settings, load_settings
from .generation import generate_additional_news, generate_synthetic_news
from .llm import gigachat_stub, llm_output

__all__ = [
    "DEFAULT_CONFIG_PATH",
    "PROJECT_ROOT",
    "Settings",
    "generate_additional_news",
    "generate_synthetic_news",
    "gigachat_stub",
    "llm_output",
    "load_settings",
]
