"""Configuration loading helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "config.yml"
DEFAULT_FEW_SHOT_PATH = PROJECT_ROOT / "data" / "raw" / "few_shot_2_each.xlsx"
DEFAULT_SYNTHETIC_OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "synthetic_news.xlsx"
DEFAULT_GENERATED_OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "generated_news.xlsx"


@dataclass(frozen=True)
class Settings:
    """Typed view over ``configs/config.yml``."""

    config_path: Path
    creds: str
    model: str
    system_prompt_news_path: Path
    system_prompt_path: Path
    prompt_path: Path
    type_of_news_path: Path

    def read_template(self, field_name: str) -> str:
        path = getattr(self, field_name)
        if not isinstance(path, Path):
            raise TypeError(f"{field_name} is not a path field")
        return path.read_text(encoding="utf-8")


def _resolve_path(base_dir: Path, value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate
    return (base_dir / candidate).resolve()


def load_settings(config_path: str | Path | None = None) -> Settings:
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    path = path.resolve()

    with path.open("r", encoding="utf-8") as fh:
        raw: dict[str, Any] = yaml.load(fh, Loader=yaml.FullLoader)

    required_keys = (
        "creds",
        "model",
        "system_prompt_news_path",
        "system_prompt_path",
        "prompt_path",
        "type_of_news_path",
    )
    missing = [key for key in required_keys if key not in raw]
    if missing:
        raise KeyError(f"Missing keys in {path}: {', '.join(missing)}")

    base_dir = path.parent
    return Settings(
        config_path=path,
        creds=str(raw["creds"]),
        model=str(raw["model"]),
        system_prompt_news_path=_resolve_path(base_dir, str(raw["system_prompt_news_path"])),
        system_prompt_path=_resolve_path(base_dir, str(raw["system_prompt_path"])),
        prompt_path=_resolve_path(base_dir, str(raw["prompt_path"])),
        type_of_news_path=_resolve_path(base_dir, str(raw["type_of_news_path"])),
    )
