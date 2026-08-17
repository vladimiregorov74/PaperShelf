from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton, QVBoxLayout,
)
from PySide6.QtWidgets import QStyle
from papershelf.ui.dialogs.base_dialog import BaseDialog
from papershelf.ui.styles.button_styles import SUCCESS_BUTTON_STYLE, SECONDARY_BUTTON_STYLE


class ConfirmDialog(BaseDialog):
    """
    Диалог подтверждения действия.

    Назначение
    ----------
    Используется во всех случаях, когда требуется
    подтверждение пользователя перед выполнением
    необратимой операции.

    Примеры использования
    ---------------------
    • удаление статьи;

    • удаление библиотеки;

    • перезапись существующего файла;

    • очистка данных.

    Особенности
    -----------
    • единый стиль приложения;

    • возвращает True при подтверждении действия.
    """
    
    # ------------------------------------------------------------------
    
    def __init__(
            self,
            parent,
            title: str,
            text: str,
    ) -> None:
        super().__init__(parent)
        
        self._accepted = False
        
        self._create_widgets(
            title,
            text,
        )
        
        self._create_layout()
        
        self._connect_signals()
    
    # ------------------------------------------------------------------
    
    def _create_widgets(
            self,
            title: str,
            text: str,
    ) -> None:
        """
        Создать элементы интерфейса.
        """
        
        self._title_label = QLabel(title)
        
        # self._title_label.setStyleSheet(
        #     "font-size:16px;font-weight:bold;"
        # )
        self._title_label.setStyleSheet("""
        font-size:18px;
        font-weight:bold;
        color:#202020;
        """)
        
        self._text_label = QLabel(text)
        # self._text_label.setStyleSheet("""
        # font-size:14px;
        # color:#404040;
        # """)
        
        self._text_label.setWordWrap(True)
        
        self._icon_label = QLabel()
        
        # Иконка предупреждения
        icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_MessageBoxWarning
        )
        
        self._icon_label.setPixmap(
            icon.pixmap(48, 48)
        )
        
        self._icon_label.setFixedSize(48, 48)
        
        self._icon_label.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )
        
        self._yes_button = QPushButton("✔ Да")
        
        self._no_button = QPushButton("Нет")
        
        self._yes_button.setFixedWidth(110)
        
        self._no_button.setFixedWidth(110)
        
        self._yes_button.setStyleSheet(SUCCESS_BUTTON_STYLE)
        self._no_button.setStyleSheet(SECONDARY_BUTTON_STYLE)
    
    # ------------------------------------------------------------------
    
    def _create_layout(self) -> None:
        """
        Создать компоновку окна.
        """
        
        content_layout = QHBoxLayout()
        
        content_layout.setSpacing(16)
        
        content_layout.addWidget(
            self._icon_label,
            alignment=Qt.AlignmentFlag.AlignTop,
        )
        
        text_layout = QVBoxLayout()
        
        text_layout.setSpacing(8)
        
        text_layout.addWidget(
            self._title_label,
        )
        
        text_layout.addWidget(
            self._text_label,
        )
        
        text_layout.addStretch()
        
        content_layout.addLayout(
            text_layout,
            1,
        )
        
        self.main_layout.addLayout(
            content_layout,
        )
        
        buttons_layout = QHBoxLayout()
        
        buttons_layout.addStretch()
        
        buttons_layout.addWidget(
            self._yes_button,
        )
        
        buttons_layout.addWidget(
            self._no_button,
        )
        
        self.main_layout.addLayout(
            buttons_layout,
        )
    
    # ------------------------------------------------------------------
    
    def _connect_signals(self) -> None:
        """
        Подключить сигналы.
        """
        
        self._yes_button.clicked.connect(
            self._accept
        )
        
        self._no_button.clicked.connect(
            self.reject
        )
    
    # ------------------------------------------------------------------
    
    def _accept(self) -> None:
        """
        Подтвердить действие.
        """
        
        self._accepted = True
        
        self.accept()
    
    # ------------------------------------------------------------------
    
    @staticmethod
    def ask(
            parent,
            title: str,
            text: str,
    ) -> bool:
        """
        Показать диалог подтверждения.
        """
        
        dialog = ConfirmDialog(
            parent,
            title,
            text,
        )
        
        dialog.exec()
        
        return dialog._accepted