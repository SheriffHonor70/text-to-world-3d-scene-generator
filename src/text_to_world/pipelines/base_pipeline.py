"""PipelineContext + Pipeline protocol."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from ..config.settings import Settings
from ..models.scene_graph import SceneGraph


@dataclass(slots=True)
class PipelineContext:
    settings: Settings
    tokens: list[int]
    quality: str
    seed: int | None
    renderer: object  # SplatRenderer; typed as object to avoid a cycle


@runtime_checkable
class Pipeline(Protocol):
    name: str

    def run(self, graph: SceneGraph, ctx: PipelineContext) -> SceneGraph: ...