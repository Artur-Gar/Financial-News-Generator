"""General utility functions used across generation pipelines."""

from __future__ import annotations

import re

import pandas as pd


def extract_number(value: str) -> str:
    """Extract the leading integer part from keys like ``'12_short'``."""
    match = re.match(r"(\d+)", value)
    return match.group(1) if match else value


def strip_enumeration_prefix(line: str) -> str:
    """Remove typical list numbering like ``'1. '`` or ``'2) '``."""
    return re.sub(r"^\s*\d+\s*[\.\)\-:]\s*", "", line).strip()


def drop_unnamed_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Drop accidental Excel index columns (``Unnamed: ...``)."""
    return df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed:")]
