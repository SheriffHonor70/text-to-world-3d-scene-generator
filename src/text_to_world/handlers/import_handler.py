"""ImportHandler — load an existing scene file back into a SceneGraph."""

from __future__ import annotations

from pathlib import Path

import trimesh  # note: trimesh >= 4.4 required for the GLTF2 scene API

from ..models.scene_graph import SceneGraph, SceneNode
from ..models.transforms import Transform


class ImportError_(RuntimeError):
    pass


class ImportHandler:
    def load(self, source: Path) -> SceneGraph:
        if not source.exists():
            raise ImportError_(f"no such file: {source}")
        try:
            loaded = trimesh.load(source, force="scene")
        except Exception as exc:  # noqa: BLE001 - trimesh raises a zoo
            raise ImportError_(str(exc)) from exc

        graph = SceneGraph.empty(prompt=f"imported:{source.name}", seed=None)
        for name, geom in loaded.geometry.items():
            node = SceneNode(
                id=f"import/{name}",
                kind="mesh",
                transform=Transform.from_matrix(loaded.graph.get(name)[0]),
                mesh_ref=name,
                tags={"source": source.suffix.lstrip(".")},
            )
            graph = graph.with_node(node)
        return graph