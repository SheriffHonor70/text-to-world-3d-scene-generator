"""LayoutPipeline — prompt tokens -> coarse 3D layout."""

from __future__ import annotations

import random

from ..config.settings import Settings
from ..core.lighting import rig_for_mood
from ..models.scene_graph import SceneNode
from ..models.transforms import Transform
from ..utils.logging import get_logger
from .base_pipeline import PipelineContext

log = get_logger(__name__)

# Coarse keyword -> mood mapping. The real planner is the layout-planner-v2
# checkpoint; this table is the deterministic fallback when the checkpoint
# is missing (fresh clone, CI, CPU-only machines).
_MOOD_KEYWORDS: dict[str, str] = {
    "sunset": "golden_hour",
    "dawn": "golden_hour",
    "beach": "golden_hour",
    "forest": "overcast",
    "rain": "overcast",
    "fog": "overcast",
    "neon": "night_neon",
    "cyberpunk": "night_neon",
    "night": "night_neon",
    "room": "interior_warm",
    "interior": "interior_warm",
    "kitchen": "interior_warm",
}


def _infer_mood(tokens: list[int], prompt: str) -> str:
    lowered = prompt.lower()
    for keyword, mood in _MOOD_KEYWORDS.items():
        if keyword in lowered:
            return mood
    return "overcast"


class LayoutPipeline:
    name = "layout"

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def run(self, graph, ctx: PipelineContext):
        rng = random.Random(ctx.seed)
        mood = _infer_mood(ctx.tokens, graph.prompt)
        log.debug("layout: mood=%s seed=%s", mood, ctx.seed)

        graph.metadata["mood"] = mood
        graph.metadata["planner"] = self._settings.layout_model

        for i, spec in enumerate(rig_for_mood(mood)):
            graph.with_node(
                SceneNode(
                    id=f"light/{i:02d}",
                    kind="light",
                    transform=Transform(
                        translation=spec.position or (0.0, 5.0, 0.0),
                    ),
                    tags=frozenset({spec.kind, "auto"}),
                )
            )

        # Placeholder ground plane. Real layout comes from the checkpoint.
        graph.with_node(
            SceneNode(
                id="ground/plane",
                kind="mesh",
                transform=Transform.identity(),
                mesh_ref="primitive://plane",
                tags=frozenset({"ground", "auto"}),
            )
        )

        # A couple of jittered placeholder props so the export isn't empty.
        for i in range(3):
            graph.with_node(
                SceneNode(
                    id=f"prop/{i:02d}",
                    kind="mesh",
                    transform=Transform(
                        translation=(rng.uniform(-3, 3), 0.5, rng.uniform(-3, 3)),
                    ),
                    mesh_ref="primitive://cube",
                    tags=frozenset({"prop", "placeholder"}),
                )
            )
        return graph