"""MaterialPipeline — assign PBR materials to meshes."""

from __future__ import annotations

from ..config.settings import Settings
from ..models.material import Material, sanitize
from ..utils.logging import get_logger
from .base_pipeline import PipelineContext

log = get_logger(__name__)

_PRESETS: dict[str, Material] = {
    "ground": Material("ground_grass", (0.24, 0.38, 0.20, 1.0), 0.0, 0.9),
    "prop": Material("prop_default", (0.72, 0.68, 0.62, 1.0), 0.05, 0.7),
}


class MaterialPipeline:
    name = "material"

    def __init__(