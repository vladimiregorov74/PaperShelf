from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget
from .resources.icons import icon



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
    supported_sites: QAction
    


def create_actions(parent: QWidget) -> AppActions:
    """Создать все QAction приложения."""
    
    # ------------------------------------------------------------------
    # Файл
    # ------------------------------------------------------------------
    
    download = QAction(
	    icon("download"),
	    "Скачать",
	    parent,
	)
    download.setShortcut("Ctrl+D")
    download.setStatusTip("Скачать статью")
    
    open_folder = QAction(
	    icon("folder-open"),
	    "Открыть папку",
	    parent
    )
    open_folder.setShortcut("Ctrl+O")
    
    exit_action = QAction(
	    icon("exit"),
	    "Выход",
	    parent
    )
    exit_action.setShortcut("Ctrl+Q")
    
    # ------------------------------------------------------------------
    # Библиотека
    # ------------------------------------------------------------------
    
    library = QAction(
	    icon("library"),
	    "Библиотека",
	    parent
    )
    
    refresh_library = QAction(
	    icon("refresh"),
        "Обновить библиотеку",
        parent,
    )
    
    sort_by_date = QAction(
        icon("calendar"),
        "По дате",
        parent,
    )
    
    sort_by_title = QAction(
        icon("sort"),
        "По названию",
        parent,
    )
    
    # ------------------------------------------------------------------
    # Настройки
    # ------------------------------------------------------------------
    
    settings = QAction(
        icon("settings"),
        "Настройки",
        parent,
    )
    
    supported_sites = QAction(
        icon("earth"),
        "Поддерживаемые сайты...",
        parent,
    )
    
    # ------------------------------------------------------------------
    # Справка
    # ------------------------------------------------------------------
    
    about = QAction(
        icon("info"),
        "О программе",
        parent,
    )
    
    return AppActions(
        download=download,
        open_folder=open_folder,
        library=library,
        refresh_library=refresh_library,
        sort_by_date=sort_by_date,
        sort_by_title=sort_by_title,
        settings=settings,
        supported_sites=supported_sites,
        exit=exit_action,
        about=about,
    )