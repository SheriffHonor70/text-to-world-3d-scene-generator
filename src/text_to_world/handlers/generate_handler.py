"""GenerateHandler — wraps SceneEngine for UI callers."""

from __future__ import annotations

from pathlib import Path

from ..config.settings import Settings
from ..core.engine import SceneEngine
from ..models.scene_graph import SceneGraph
from ..utils.logging import get_logger

log = get_logger(__name__)


class GenerateHandler:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def generate(self, prompt: str, *, seed: int | None = None, quality: str = "standard") -> SceneGraph:
        engine = SceneEngine(self._settings)
        try:
            return engine.generate(prompt=prompt, seed=seed, quality=quality)
        finally:
            engine.close()


def slugify(prompt: str, max_len: int = 48) -> str:
    keep = [c.lower() if c.isalnum() else "-" for c in prompt]
    slug = "".join(keep).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug[:max_len] or "scene"


def suggested_output(prompt: str, base: Path = Path("out")) -> Path:
    return base / f"{slugify(prompt)}.glb"