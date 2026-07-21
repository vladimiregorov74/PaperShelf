from __future__ import annotations

from PySide6.QtWidgets import QMenuBar

from papershelf.ui.actions import AppActions


class MainMenuBar(QMenuBar):

    def __init__(self, actions: AppActions):
        super().__init__()

        file_menu = self.addMenu("Файл")
        file_menu.addAction(actions.download)
        file_menu.addSeparator()
        file_menu.addAction(actions.open_folder)
        file_menu.addSeparator()
        file_menu.addAction(actions.exit)

        library_menu = self.addMenu("Библиотека")
        library_menu.addAction(actions.library)

        settings_menu = self.addMenu("Настройки")
        settings_menu.addAction(actions.settings)

        help_menu = self.addMenu("Справка")
        help_menu.addAction(actions.about)