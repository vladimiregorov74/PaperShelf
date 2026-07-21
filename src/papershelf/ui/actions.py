from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget


@dataclass(slots=True)
class AppActions:
    download: QAction
    open_folder: QAction
    library: QAction
    settings: QAction
    exit: QAction
    about: QAction


def create_actions(parent: QWidget) -> AppActions:
    """Создать все QAction приложения."""

    download = QAction("📥 Скачать", parent)
    download.setShortcut("Ctrl+D")
    download.setStatusTip("Скачать статью")

    open_folder = QAction("📂 Открыть папку", parent)
    open_folder.setShortcut("Ctrl+O")

    library = QAction("📚 Библиотека", parent)

    settings = QAction("⚙ Настройки", parent)

    exit_action = QAction("Выход", parent)
    exit_action.setShortcut("Ctrl+Q")

    about = QAction("О программе", parent)

    return AppActions(
        download=download,
        open_folder=open_folder,
        library=library,
        settings=settings,
        exit=exit_action,
        about=about,
    )