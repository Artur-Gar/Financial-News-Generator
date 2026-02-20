"""Unified CLI for synthetic news generation workflows."""

from __future__ import annotations

import argparse
from pathlib import Path

from gigachat_synthetic_news.config import DEFAULT_GENERATED_OUTPUT_PATH, DEFAULT_SYNTHETIC_OUTPUT_PATH
from gigachat_synthetic_news.generation import generate_additional_news, generate_synthetic_news


def _add_common_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", type=Path, default=None, help="Path to config.yml")
    parser.add_argument("--skip-stub", action="store_true", help="Disable warm-up request")
    parser.add_argument("--no-progress", action="store_true", help="Disable progress bar")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate paths and arguments without calling the LLM API.",
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate synthetic financial news datasets.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    base = subparsers.add_parser("base", help="Generate base synthetic news dataset.")
    _add_common_flags(base)
    base.add_argument("--few-shot", type=Path, default=None, help="Path to few-shot Excel file")
    base.add_argument("--output", type=Path, default=None, help="Base output Excel path")
    base.add_argument("--temperature", type=float, default=1.2, help="GigaChat temperature")

    additional = subparsers.add_parser("additional", help="Generate additional synthetic rewrites.")
    _add_common_flags(additional)
    additional.add_argument("--input", type=Path, default=None, help="Input synthetic_news.xlsx path")
    additional.add_argument("--output", type=Path, default=None, help="Additional output Excel path")
    additional.add_argument("--temperature", type=float, default=1.5, help="GigaChat temperature")

    all_cmd = subparsers.add_parser("all", help="Run both base and additional generation.")
    _add_common_flags(all_cmd)
    all_cmd.add_argument("--few-shot", type=Path, default=None, help="Path to few-shot Excel file")
    all_cmd.add_argument("--base-output", type=Path, default=None, help="Base output Excel path")
    all_cmd.add_argument(
        "--additional-input",
        type=Path,
        default=None,
        help="Input path for additional generation (defaults to base output).",
    )
    all_cmd.add_argument("--additional-output", type=Path, default=None, help="Additional output Excel path")
    all_cmd.add_argument("--base-temperature", type=float, default=1.2, help="Base generation temperature")
    all_cmd.add_argument(
        "--additional-temperature",
        type=float,
        default=1.5,
        help="Additional generation temperature",
    )

    return parser


def _run_base(args: argparse.Namespace) -> None:
    output = args.output or DEFAULT_SYNTHETIC_OUTPUT_PATH
    if args.dry_run:
        print(f"Dry run OK. mode=base few_shot={Path(args.few_shot) if args.few_shot else None} output={Path(output)}")
        return

    generate_synthetic_news(
        config_path=args.config,
        few_shot_path=args.few_shot,
        output_path=output,
        temperature=args.temperature,
        run_stub=not args.skip_stub,
        show_progress=not args.no_progress,
    )


def _run_additional(args: argparse.Namespace) -> None:
    input_path = args.input or DEFAULT_SYNTHETIC_OUTPUT_PATH
    output = args.output or DEFAULT_GENERATED_OUTPUT_PATH
    if args.dry_run:
        print(f"Dry run OK. mode=additional input={Path(input_path)} output={Path(output)}")
        return

    generate_additional_news(
        config_path=args.config,
        input_path=input_path,
        output_path=output,
        temperature=args.temperature,
        run_stub=not args.skip_stub,
        show_progress=not args.no_progress,
    )


def _run_all(args: argparse.Namespace) -> None:
    base_output = args.base_output or DEFAULT_SYNTHETIC_OUTPUT_PATH
    additional_input = args.additional_input or base_output
    additional_output = args.additional_output or DEFAULT_GENERATED_OUTPUT_PATH

    if args.dry_run:
        print(
            "Dry run OK. "
            f"mode=all "
            f"few_shot={Path(args.few_shot) if args.few_shot else None} "
            f"base_output={Path(base_output)} "
            f"additional_input={Path(additional_input)} "
            f"additional_output={Path(additional_output)}"
        )
        return

    generate_synthetic_news(
        config_path=args.config,
        few_shot_path=args.few_shot,
        output_path=base_output,
        temperature=args.base_temperature,
        run_stub=not args.skip_stub,
        show_progress=not args.no_progress,
    )
    generate_additional_news(
        config_path=args.config,
        input_path=additional_input,
        output_path=additional_output,
        temperature=args.additional_temperature,
        run_stub=False,
        show_progress=not args.no_progress,
    )


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "base":
        _run_base(args)
        return
    if args.command == "additional":
        _run_additional(args)
        return
    _run_all(args)


if __name__ == "__main__":
    main()
