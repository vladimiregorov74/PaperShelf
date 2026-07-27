from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget


@dataclass(slots=True)
class AppActions:
    download: QAction
    open_folder: QAction
    library: QAction
    refresh_library: QAction
    sort_by_date: QAction
    sort_by_title: QAction
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
    
    refresh_library = QAction("🔄 Обновить библиотеку", parent,)
    
    sort_by_date = QAction("📅 По дате", parent,)
    
    sort_by_title = QAction("🔤 По названию", parent,)

    settings = QAction("⚙ Настройки", parent)

    exit_action = QAction("Выход", parent)
    exit_action.setShortcut("Ctrl+Q")

    about = QAction("О программе", parent)
    
    return AppActions(
        download=download,
        open_folder=open_folder,
        library=library,
        
        refresh_library=refresh_library,
        sort_by_date=sort_by_date,
        sort_by_title=sort_by_title,
        
        settings=settings,
        exit=exit_action,
        about=about,
    )