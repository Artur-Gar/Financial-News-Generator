# Gigachat Synthetic News

## Description
This is a work project for generating synthetic financial news with GigaChat LLM.
The codebase is organized as a Python package in `src/gigachat_synthetic_news` with separate pipeline entrypoints in `scripts/`.
The workflow has two stages: base synthetic news generation and additional short/medium/long rewrites.
The project focuses on practicing prompt-driven dataset generation in a clean `src/` repository structure.

## Setup
```bash
poetry install
poetry shell
```

## Usage
Generate base dataset:
```bash
python scripts/generate_news.py base
```

Generate additional rewrites:
```bash
python scripts/generate_news.py additional
```

Run both stages:
```bash
python scripts/generate_news.py all
```

## Structure
- `src/gigachat_synthetic_news/`: package code (config, LLM helpers, pipelines, utils).
- `scripts/`: single CLI entrypoint with subcommands (`base`, `additional`, `all`).
- `configs/`: runtime settings and prompt templates.
- `data/raw/`: source input files.
- `data/processed/`: generated output datasets.
- `notebooks/`: exploratory notebooks.
- `docs/`: supplementary project materials.

## Notes
- Set valid credentials in `configs/config.yml` before running generation commands.
- Add `--dry-run` to any subcommand to validate paths without API calls.
