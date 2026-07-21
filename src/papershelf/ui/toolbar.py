from __future__ import annotations

from PySide6.QtWidgets import QToolBar

from papershelf.ui.actions import AppActions


class MainToolBar(QToolBar):
    """Главная панель инструментов."""

    def __init__(self, actions: AppActions) -> None:
        super().__init__("Главная")

        self.setMovable(False)

        self.addAction(actions.download)

        self.addSeparator()

        self.addAction(actions.open_folder)
        self.addAction(actions.library)

        self.addSeparator()

        self.addAction(actions.settings)