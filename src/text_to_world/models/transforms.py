"""3D transforms. Row-major, right-handed, Y-up."""

from __future__ import annotations

import math
from dataclasses import dataclass, replace

Vec3 = tuple[float, float, float]


@dataclass(frozen=True, slots=True)
class Transform:
    translation: Vec3 = (0.0, 0.0, 0.0)
    rotation_quat: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)
    scale: float = 1.0

    @classmethod
    def identity(cls) -> "Transform":
        return cls()

    @classmethod
    def from_matrix(cls, matrix: object) -> "Transform":
        # Accepts a numpy 4x4 or a 3x3. Extraction is intentionally minimal —
        # we only need translation + uniform scale for imported nodes.
        import numpy as np

        m = np.asarray(matrix, dtype=float)
        if m.shape == (4, 4):
            translation = tuple(m[:3, 3].tolist())
            scale = float(np.cbrt(np.linalg.det(m[:3, :3])))
        elif m.shape == (3, 3):
            translation = (0.0, 0.0, 0.0)
            scale = float(np.cbrt(np.linalg.det(m)))
        else:
            raise ValueError(f"unsupported matrix shape: {m.shape}")
        return cls(translation=translation, scale=scale)  # type: ignore[arg-type]

    def with_translation(self, t: Vec3) -> "Transform":
        return replace(self, translation=t)

    def with_scale(self, s: float) -> "Transform":
        return replace(self, scale=s)

    def with_rotation_euler(self, rx: float, ry: float, rz: float) -> "Transform":
        cx, sx = math.cos(rx / 2), math.sin(rx / 2)
        cy, sy = math.cos(ry / 2), math.sin(ry / 2)
        cz, sz = math.cos(rz / 2), math.sin(rz / 2)
        qx = sx * cy * cz - cx * sy * sz
        qy = cx * sy * cz + sx * cy * sz
        qz = cx * cy * sz - sx * sy * cz
        qw = cx * cy * cz + sx * sy * sz
        return replace(self, rotation_quat=(qx, qy, qz, qw))

    def is_identity(self) -> bool:
        return (
            self.translation == (0.0, 0.0, 0.0)
            and self.rotation_quat == (0.0, 0.0, 0.0, 1.0)
            and self.scale == 1.0
        )