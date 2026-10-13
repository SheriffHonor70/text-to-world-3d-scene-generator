"""Typed settings loaded from env + user config file."""

from __future__ import annotations

import json
import os
from pathlib import Path

from platformdirs import user_config_dir
from pydantic import BaseModel, Field, field_validator

DEFAULT_CHECKPOINT_DIR = Path(os.environ.get("T2W_CHECKPOINT_DIR", "models/checkpoints"))


class Settings(BaseModel):
    """Runtime configuration for the scene generator."""

    model_config = {"extra": "forbid"}

    checkpoint_dir: Path = Field(default=DEFAULT_CHECKPOINT_DIR)
    cache_dir: Path | None = None
    device: str = Field(default="auto")
    max_prompt_tokens: int = Field(default=4096, ge=64, le=16384)
    default_quality: str = Field(default="standard")
    enable_gpu: bool = Field(default=True)
    telemetry_enabled: bool = Field(default=False)
    layout_model: str = Field(default="layout-planner-v2")
    texture_model: str = Field(default="matdiffuse-xl")
    geometry_backend: str = Field(default="splat")

    @field_validator("device")
    @classmethod
    def _check_device(cls, value: str) -> str:
        if value not in {"auto", "cpu", "cuda", "cuda:0", "mps", "dml"}:
            raise ValueError(f"unsupported device: {value}")
        return value

    @field_validator("default_quality")
    @classmethod
    def _check_quality(cls, value: str) -> str:
        if value not in {"draft", "standard", "high"}:
            raise ValueError(f"unsupported quality: {value}")
        return value


def _config_path() -> Path:
    return Path(user_config_dir("text-to-world")) / "settings.json"


def load_settings() -> Settings:
    """Load settings from `<config_dir>/settings.json`, falling back to defaults."""
    path = _config_path()
    if not path.exists():
        return Settings()
    raw = json.loads(path.read_text(encoding="utf-8"))
    return Settings.model_validate(raw)


def save_settings(settings: Settings) -> None:
    path = _config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(settings.model_dump_json(indent=2), encoding="utf-8")