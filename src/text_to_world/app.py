"""PySide6 desktop shell. Thin — all real work lives in the engine."""

from __future__ import annotations

import sys

from .config.settings import Settings, load_settings
from .handlers.export_handler import ExportHandler
from .handlers.generate_handler import GenerateHandler
from .utils.logging import get_logger

log = get_logger(__name__)


def run(settings: Settings | None = None) -> int:
    """Launch the Qt app. Returns process exit code."""
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError:
        log.error("PySide6 not installed. `pip install -e .` to pull GUI deps.")
        return 2

    from .ui.main_window import MainWindow

    settings = settings or load_settings()
    app = QApplication(sys.argv)
    app.setApplicationName("text-to-world")

    window = MainWindow(
        settings=settings,
        generate_handler=GenerateHandler(settings),
        export_handler=ExportHandler(settings),
    )
    window.show()
    return app.exec()