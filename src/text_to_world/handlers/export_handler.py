"""ExportHandler — validate and route scene exports."""

from __future__ import annotations

from pathlib import Path

from ..config.settings import Settings
from ..models.scene_graph import SceneGraph
from ..services.exporter import Exporter

_SUPPORTED = {".glb", ".gltf", ".usd", ".usda", ".ply", ".splat"}


class UnsupportedFormatError(ValueError):
    pass


class ExportHandler:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._exporter = Exporter(settings)

    def export(self, graph: SceneGraph, destination: Path) -> Path:
        suffix = destination.suffix.lower()
        if suffix not in _SUPPORTED:
            raise UnsupportedFormatError(
                f"{suffix!r} not supported. Pick one of: {sorted(_SUPPORTED)}"
            )
        destination.parent.mkdir(parents=True, exist_ok=True)
        return self._exporter.write(graph, destination)

    def supported_formats(self) -> frozenset[str]:
        return frozenset(_SUPPORTED)