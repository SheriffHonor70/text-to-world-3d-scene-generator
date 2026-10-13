"""CLI bootstrap. `python -m text_to_world` lands here."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .bootstrap import initialize_runtime
from .config.settings import load_settings
from .core.engine import SceneEngine
from .utils.logging import configure_logging, get_logger


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="text-to-world",
        description="Generate an explorable 3D scene from a text prompt.",
    )
    parser.add_argument("prompt", nargs="?", help="Text prompt describing the scene.")
    parser.add_argument("-o", "--out", type=Path, default=Path("out/scene.glb"))
    parser.add_argument("--gui", action="store_true", help="Launch the desktop GUI.")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--quality", choices=["draft", "standard", "high"], default="standard")
    parser.add_argument("--verbose", "-v", action="count", default=0)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    configure_logging(verbosity=args.verbose)
    log = get_logger(__name__)

    settings = load_settings()
    initialize_runtime(settings)

    if args.gui or args.prompt is None:
        from .app import run as run_gui

        return run_gui(settings)

    engine = SceneEngine(settings)
    try:
        scene = engine.generate(
            prompt=args.prompt,
            seed=args.seed,
            quality=args.quality,
        )
        engine.export(scene, args.out)
    except Exception as exc:  # noqa: BLE001 - top-level CLI guard
        log.exception("scene generation failed")
        print(f"error: {exc}", file=sys.stderr)
        return 1
    finally:
        engine.close()

    log.info("wrote %s", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())