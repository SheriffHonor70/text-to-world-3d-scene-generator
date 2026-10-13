"""Well-known subpaths used across the app."""

from __future__ import annotations

from pathlib import Path

CHECKPOINTS_SUBDIR = "checkpoints"
SCENES_SUBDIR = "scenes"
THUMBNAILS_SUBDIR = "thumbnails"
PROMPT_LOG = "prompts.jsonl"


def scene_output_dir(base: Path, slug: str) -> Path:
    """Resolve the per-scene output dir for a given slug."""
    return base / SCENES_SUBDIR / slug


def thumbnail_path(base: Path, slug: str) -> Path:
    return base / THUMBNAILS_SUBDIR / f"{slug}.png"