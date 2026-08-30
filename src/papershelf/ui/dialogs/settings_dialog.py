from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QPushButton,
)

from papershelf.ui.dialogs.base_dialog import BaseDialog
from papershelf.ui.styles.button_styles import (
    SECONDARY_BUTTON_STYLE,
    SUCCESS_BUTTON_STYLE,
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
            log_panel_visible: bool,
            parent=None,
    ) -> None:
        super().__init__(parent)
        
        self.setWindowTitle("Настройки")
        
        self._create_widgets(
            file_logging,
            log_panel_visible,
        )
        
        self._create_layout()
        
        self._connect_signals()

    # ------------------------------------------------------------------
    # Widgets
    # ------------------------------------------------------------------
    
    def _create_widgets(
            self,
            file_logging: bool,
            log_panel_visible: bool,
    ) -> None:
        """
        Создать элементы интерфейса.
        """
        
        self._title_label = self.create_section_title(
            "Настройки журнала"
        )
        
        self._file_logging = QCheckBox(
            "Логирование в файл"
        )
        
        self._file_logging.setChecked(
            file_logging,
        )
        
        self._log_panel_visible = QCheckBox(
            "Показать панель логирования"
        )
        
        self._log_panel_visible.setChecked(
            log_panel_visible,
        )
        
        self._ok_button = QPushButton("OK")
        self._cancel_button = QPushButton("Отмена")
        
        self._ok_button.setFixedWidth(110)
        self._cancel_button.setFixedWidth(110)
        
        self._ok_button.setStyleSheet(
            SUCCESS_BUTTON_STYLE,
        )
        
        self._cancel_button.setStyleSheet(
            SECONDARY_BUTTON_STYLE,
        )

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _create_layout(self) -> None:
        """
        Создать компоновку окна.
        """

        self.main_layout.addWidget(
            self._title_label,
        )

        self.main_layout.addWidget(
            self._file_logging,
        )
        
        self.main_layout.addWidget(
            self._log_panel_visible,
        )

        self.main_layout.addStretch()

        self.add_buttons(
            self._cancel_button,
            self._ok_button,
        )

    # ------------------------------------------------------------------
    # Signals
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        """
        Подключить сигналы.
        """

        self._ok_button.clicked.connect(
            self.accept,
        )

        self._cancel_button.clicked.connect(
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
    
    def log_panel_visible(self) -> bool:
        """
        Возвращает состояние панели логирования.
        """
        
        return self._log_panel_visible.isChecked()