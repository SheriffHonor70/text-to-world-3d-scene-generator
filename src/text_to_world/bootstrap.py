"""Runtime bootstrap: directories, device probe, manifest warm-up."""

from __future__ import annotations

from pathlib import Path

from platformdirs import user_cache_dir, user_config_dir, user_data_dir

from .config.settings import Settings
from .utils.logging import get_logger

log = get_logger(__name__)


class RuntimePaths:
    """Resolved on-disk locations for the running app."""

    def __init__(self, settings: Settings) -> None:
        self.config_dir = Path(user_config_dir("text-to-world"))
        self.cache_dir = Path(user_cache_dir("text-to-world"))
        self.data_dir = Path(user_data_dir("text-to-world"))
        self.plugin_dir = self.data_dir / "plugins"
        self.checkpoint_dir = settings.checkpoint_dir

    def ensure(self) -> None:
        for path in (
            self.config_dir,
            self.cache_dir,
            self.data_dir,
            self.plugin_dir,
            self.checkpoint_dir,
        ):
            path.mkdir(parents=True, exist_ok=True)


_RUNTIME: RuntimePaths | None = None


def initialize_runtime(settings: Settings) -> RuntimePaths:
    """Idempotent bootstrap. Safe to call from CLI, GUI, and tests."""
    global _RUNTIME
    if _RUNTIME is not None:
        return _RUNTIME

    paths = RuntimePaths(settings)
    paths.ensure()
    log.debug("runtime dirs: config=%s cache=%s data=%s", paths.config_dir, paths.cache_dir, paths.data_dir)
    _RUNTIME = paths
    return paths


def get_runtime() -> RuntimePaths:
    if _RUNTIME is None:
        raise RuntimeError("initialize_runtime() must run before get_runtime()")
    return _RUNTIME