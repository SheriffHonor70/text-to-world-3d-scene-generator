"""SceneEngine — the orchestrator. Prompt in, SceneGraph out, GLB on disk."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from ..config.settings import Settings
from ..models.scene_graph import SceneGraph
from ..pipelines.base_pipeline import PipelineContext
from ..pipelines.layout_pipeline import LayoutPipeline
from ..pipelines.material_pipeline import MaterialPipeline
from ..renderers.splat_renderer import SplatRenderer
from ..services.exporter import Exporter
from ..services.prompt_encoder import PromptEncoder
from ..utils.logging import get_logger

log = get_logger(__name__)


class SceneEngine:
    """High-level facade. Owns the pipeline list and the exporter."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.encoder = PromptEncoder(settings)
        self.renderer = SplatRenderer(settings)
        self.exporter = Exporter(settings)
        self.pipelines = [
            LayoutPipeline(settings),
            MaterialPipeline(settings),
        ]

    def generate(
        self,
        prompt: str,
        *,
        seed: int | None = None,
        quality: str | None = None,
    ) -> SceneGraph:
        quality = quality or self.settings.default_quality
        started = time.perf_counter()

        tokens = self.encoder.encode(prompt)
        log.info("encoded prompt: %d tokens, quality=%s", len(tokens), quality)

        graph = SceneGraph.empty(prompt=prompt, seed=seed)
        ctx = PipelineContext(
            settings=self.settings,
            tokens=tokens,
            quality=quality,
            seed=seed,
            renderer=self.renderer,
        )
        for pipeline in self.pipelines:
            graph = pipeline.run(graph, ctx)

        log.info("scene built in %.2fs (%d nodes)", time.perf_counter() - started, len(graph.nodes))
        return graph

    def export(self, graph: SceneGraph, destination: Path) -> Path:
        return self.exporter.write(graph, destination)

    def close(self) -> None:
        self.renderer.release()
        self.encoder.release()