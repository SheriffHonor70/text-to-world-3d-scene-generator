"""Lighting rigs keyed by scene mood."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LightSpec:
    kind: str  # "directional" | "point" | "spot" | "hdri"
    intensity: float
    color: tuple[float, float, float]
    position: tuple[float, float, float] | None = None
    hdri_name: str | None = None


_MOODS: dict[str, tuple[LightSpec, ...]] = {
    "golden_hour": (
        LightSpec("directional", 3.2, (1.0, 0.82, 0.58), position=(10.0, 6.0, -4.0)),
        LightSpec("hdri", 1.0, (1.0, 1.0, 1.0), hdri_name="sunset_field_4k"),
    ),
    "overcast": (
        LightSpec("hdri", 1.4, (0.92, 0.94, 0.98), hdri_name="soft_studio_2k"),
    ),
    "night_neon": (
        LightSpec("point", 2.0, (0.20, 0.80, 1.00), position=(0.0, 3.0, 0.0)),
        LightSpec("point", 1.6, (1.00, 0.20, 0.70), position=(4.0, 2.5, -3.0)),
    ),
    "interior_warm": (
        LightSpec("point", 1.8, (1.00, 0.85, 0.70), position=(0.0, 2.8, 0.0)),
    ),
}


def rig_for_mood(mood: str) -> tuple[LightSpec, ...]:
    return _MOODS.get(mood, _MOODS["overcast"])


def known_moods() -> tuple[str, ...]:
    return tuple(_MOODS)