from __future__ import annotations

from papershelf.ui.dialogs.base_dialog import BaseDialog

from PySide6.QtWidgets import (
    QCheckBox,
    QDialogButtonBox,
)


class SettingsDialog(BaseDialog):
    """
    Диалог настроек приложения.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        file_logging: bool,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle("Настройки")

        self._create_widgets(
            file_logging,
        )

        self._create_layout()

        self._connect_signals()

    # ------------------------------------------------------------------
    # Widgets
    # ------------------------------------------------------------------

    def _create_widgets(
        self,
        file_logging: bool,
    ) -> None:
        """
        Создать элементы интерфейса.
        """

        self._file_logging = QCheckBox(
            "Логирование в файл",
        )

        self._file_logging.setChecked(
            file_logging,
        )

        self._buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _create_layout(self) -> None:
        """
        Создать компоновку окна.
        """

        self.main_layout.addWidget(
            self._file_logging,
        )

        self.main_layout.addStretch()

        self.main_layout.addWidget(
            self._buttons,
        )

    # ------------------------------------------------------------------
    # Signals
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        """
        Подключить сигналы.
        """

        self._buttons.accepted.connect(
            self.accept,
        )

        self._buttons.rejected.connect(
            self.reject,
        )

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def file_logging_enabled(self) -> bool:
        """
        Возвращает состояние логирования в файл.
        """

        return self._file_logging.isChecked()