"""Dataset generation pipelines extracted from notebooks."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

from .config import (
    DEFAULT_FEW_SHOT_PATH,
    DEFAULT_GENERATED_OUTPUT_PATH,
    DEFAULT_SYNTHETIC_OUTPUT_PATH,
    load_settings,
)
from .llm import gigachat_stub, llm_output
from .utils import drop_unnamed_columns, extract_number, strip_enumeration_prefix

try:
    from tqdm.auto import tqdm
except ImportError:  # pragma: no cover
    tqdm = None


def _iter_with_progress(items: Iterable[str], show_progress: bool) -> Iterable[str]:
    if show_progress and tqdm is not None:
        return tqdm(list(items))
    return items


def _clean_generation(output: str) -> list[str]:
    lines = []
    for raw_line in output.replace("\n\n", "\n").splitlines():
        line = strip_enumeration_prefix(raw_line)
        if line:
            lines.append(line)
    return lines


def generate_synthetic_news(
    config_path: str | Path | None = None,
    few_shot_path: str | Path | None = None,
    output_path: str | Path | None = None,
    temperature: float = 1.2,
    run_stub: bool = True,
    show_progress: bool = True,
) -> pd.DataFrame:
    """Generate base synthetic news and save it to Excel."""
    settings = load_settings(config_path)
    resolved_few_shot_path = Path(few_shot_path) if few_shot_path else DEFAULT_FEW_SHOT_PATH
    resolved_output_path = Path(output_path) if output_path else DEFAULT_SYNTHETIC_OUTPUT_PATH

    few_shot = pd.read_excel(resolved_few_shot_path)
    system_prompt_news_template = settings.read_template("system_prompt_news_path")
    prompt_template = settings.read_template("prompt_path")
    type_of_news = settings.read_template("type_of_news_path")

    type_of_news_map = {f"{i + 1}": news for i, news in enumerate(type_of_news.splitlines())}
    all_prompts: dict[str, str] = {}

    for i in range(1, len(type_of_news.splitlines()) + 1):
        news_filter = (few_shot.iloc[:, 1] == i).tolist()
        two_shots = few_shot.iloc[news_filter, 0].reset_index(drop=True)

        if type_of_news_map[f"{i}"][0] != "#":
            all_prompts[f"{i}_pos"] = system_prompt_news_template.format(
                num_and_sign="10 positive",
                news_type=type_of_news_map[f"{i}"],
                News_1=two_shots[0],
                News_2=two_shots[1],
            )
            all_prompts[f"{i}_neg"] = system_prompt_news_template.format(
                num_and_sign="10 negative",
                news_type=type_of_news_map[f"{i}"],
                News_1=two_shots[0],
                News_2=two_shots[1],
            )
        else:
            all_prompts[f"{i}"] = system_prompt_news_template.format(
                num_and_sign="20",
                news_type=type_of_news_map[f"{i}"][1:],
                News_1=two_shots[0],
                News_2=two_shots[1],
            )

    if run_stub:
        gigachat_stub(settings.creds, settings.model, settings.config_path)()

    frames: list[pd.DataFrame] = []
    for prompt_key in _iter_with_progress(all_prompts.keys(), show_progress):
        news_type = type_of_news_map[extract_number(prompt_key)]
        output = llm_output(
            news_type,
            all_prompts[prompt_key],
            prompt_template,
            temperature=temperature,
            creds=settings.creds,
            model=settings.model,
            config_path=settings.config_path,
        )
        cleaned_output = _clean_generation(output)
        frames.append(
            pd.DataFrame(
                {
                    "type": [news_type] * len(cleaned_output),
                    "No": list(range(1, len(cleaned_output) + 1)),
                    "text": cleaned_output,
                }
            )
        )

    final_df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=["type", "No", "text"])

    weights = [
        1,
        1,
        1,
        0.4,
        0.8,
        0.7,
        0.4,
        0.2,
        0.8,
        0.5,
        0.8,
        1,
        0.8,
        0.4,
        0.3,
        0.6,
        0.7,
        0.5,
        1,
        0.2,
        0.6,
        0.8,
        0.8,
        0.6,
        1,
        1,
        0.8,
        0.7,
        0.4,
        0.2,
        0.6,
    ]
    news_types = type_of_news.splitlines()
    weight_map = {news_types[i]: weights[i] for i in range(min(len(news_types), len(weights)))}
    final_df["impact"] = final_df["type"].map(weight_map)
    final_df["type"] = final_df["type"].str.replace("#", "", regex=False)

    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_excel(resolved_output_path, index=False)
    return final_df


def generate_additional_news(
    config_path: str | Path | None = None,
    input_path: str | Path | None = None,
    output_path: str | Path | None = None,
    temperature: float = 1.5,
    run_stub: bool = True,
    show_progress: bool = True,
) -> pd.DataFrame:
    """Generate short/medium/long variants for each base synthetic news row."""
    settings = load_settings(config_path)
    resolved_input_path = Path(input_path) if input_path else DEFAULT_SYNTHETIC_OUTPUT_PATH
    resolved_output_path = Path(output_path) if output_path else DEFAULT_GENERATED_OUTPUT_PATH

    source_df = pd.read_excel(resolved_input_path)
    source_df = drop_unnamed_columns(source_df)

    system_prompt_template = settings.read_template("system_prompt_path")
    prompt_template = settings.read_template("prompt_path")

    length_labels = (
        ("short", "50-70"),
        ("medium", "80-110"),
        ("long", "120-150"),
    )

    if run_stub:
        gigachat_stub(settings.creds, settings.model, settings.config_path)()

    records: list[dict[str, object]] = []
    row_indices = list(source_df.index)
    iterable = _iter_with_progress(row_indices, show_progress)
    for row_idx in iterable:
        row = source_df.loc[row_idx]
        text = str(row["text"])
        impact = row["impact"] if "impact" in source_df.columns else None
        news_type = row["type"] if "type" in source_df.columns else int(row_idx) + 1

        records.append(
            {
                "No": 1,
                "text": text,
                "is_synthetic": 1,
                "impact": impact,
                "news_type": news_type,
            }
        )

        for no, (_, length_bounds) in enumerate(length_labels, start=2):
            rewritten_prompt = system_prompt_template.format(length_bounds=length_bounds)
            try:
                output = llm_output(
                    text,
                    rewritten_prompt,
                    prompt_template,
                    temperature=temperature,
                    creds=settings.creds,
                    model=settings.model,
                    config_path=settings.config_path,
                )
            except Exception:
                output = None

            records.append(
                {
                    "No": no,
                    "text": output,
                    "is_synthetic": 0,
                    "impact": impact,
                    "news_type": news_type,
                }
            )

    final_df = pd.DataFrame(records)
    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_excel(resolved_output_path, index=False)
    return final_df
