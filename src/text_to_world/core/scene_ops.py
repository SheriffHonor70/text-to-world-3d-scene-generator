"""Pure functions over SceneGraph. No I/O, no logging."""

from __future__ import annotations

from ..models.scene_graph import SceneNode
from ..models.transforms import Transform


def translate(node: SceneNode, delta: tuple[float, float, float]) -> SceneNode:
    x, y, z = node.transform.translation
    dx, dy, dz = delta
    return node.with_transform(node.transform.with_translation((x + dx, y + dy, z + dz)))


def scale_uniform(node: SceneNode, factor: float) -> SceneNode:
    if factor <= 0:
        raise ValueError("scale factor must be positive")
    return node.with_transform(node.transform.with_scale(node.transform.scale * factor))


def drop_to_ground(node: SceneNode, floor_y: float = 0.0) -> SceneNode:
    """Snap a node so its local origin sits at `floor_y`."""
    x, _, z = node.transform.translation
    return node.with_transform(node.transform.with_translation((x, floor_y, z)))


def identity_transform() -> Transform:
    return Transform.identity()