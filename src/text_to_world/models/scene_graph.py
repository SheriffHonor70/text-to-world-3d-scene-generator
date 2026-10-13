"""SceneGraph and SceneNode — the in-memory representation of a scene."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Mapping

from .transforms import Transform


@dataclass(frozen=True, slots=True)
class SceneNode:
    id: str
    kind: str  # "mesh" | "light" | "camera" | "group" | "splat"
    transform: Transform
    mesh_ref: str | None = None
    material: Mapping[str, Any] = field(default_factory=dict)
    tags: frozenset[str] = field(default_factory=frozenset)

    def with_transform(self, t: Transform) -> "SceneNode":
        return replace(self, transform=t)

    def with_tag(self, tag: str) -> "SceneNode":
        return replace(self, tags=self.tags | {tag})


@dataclass(slots=True)
class SceneGraph:
    prompt: str
    seed: int | None
    nodes: list[SceneNode] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def empty(cls, *, prompt: str, seed: int | None) -> "SceneGraph":
        return cls(prompt=prompt, seed=seed)

    def with_node(self, node: SceneNode) -> "SceneGraph":
        self.nodes.append(node)
        return self

    def with_nodes(self, nodes: list[SceneNode]) -> "SceneGraph":
        self.nodes.extend(nodes)
        return self

    def __len__(self) -> int:
        return len(self.nodes)

    def find(self, node_id: str) -> SceneNode | None:
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    def by_kind(self, kind: str) -> list[SceneNode]:
        return [n for n in self.nodes if n.kind == kind]