"""Material model + tiny PBR helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Material:
    name: str
    base_color: tuple[float, float, float, float] = (0.8, 0.8, 0.8, 1.0)
    metallic: float = 0.0
    roughness: float = 0.8
    emissive: tuple[float, float, float] = (0.0, 0.0, 0.0)
    texture_ref: str | None = None

    def with_texture(self, ref: str) -> "Material":
        return Material(
            name=self.name,
            base_color=self.base_color,
            metallic=self.metallic,
            roughness=self.roughness,
            emissive=self.emissive,
            texture_ref=ref,
        )


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def sanitize(m: Material) -> Material:
    return Material(
        name=m.name,
        base_color=tuple(clamp01(c) for c in m.base_color),  # type: ignore[arg-type]
        metallic=clamp01(m.metallic),
        roughness=clamp01(m.roughness),
        emissive=tuple(clamp01(c) for c in m.emissive),  # type: ignore[arg-type]
        texture_ref=m.texture_ref,
    )