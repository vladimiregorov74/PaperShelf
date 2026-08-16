from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton, QVBoxLayout,
)
from PySide6.QtWidgets import QStyle
from papershelf.ui.dialogs.base_dialog import BaseDialog


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
        
        self.title_label = QLabel(title)
        
        # self.title_label.setStyleSheet(
        #     "font-size:16px;font-weight:bold;"
        # )
        self.title_label.setStyleSheet("""
        font-size:18px;
        font-weight:bold;
        color:#202020;
        """)
        
        self.text_label = QLabel(text)
        # self.text_label.setStyleSheet("""
        # font-size:14px;
        # color:#404040;
        # """)
        
        self.text_label.setWordWrap(True)
        
        self.icon_label = QLabel()
        
        # Иконка предупреждения
        icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_MessageBoxWarning
        )
        
        self.icon_label.setPixmap(
            icon.pixmap(48, 48)
        )
        
        self.icon_label.setFixedSize(48, 48)
        
        self.icon_label.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )
        
        self.yes_button = QPushButton("✔ Да")
        
        self.no_button = QPushButton("Нет")
        
        self.yes_button.setFixedWidth(110)
        
        self.no_button.setFixedWidth(110)
        
        self.yes_button.setStyleSheet("""
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: 1px solid #3d8b40;
            border-radius: 6px;
            padding: 6px 18px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #5DBB63;
        }

        QPushButton:pressed {
            background-color: #3F9142;
        }
        """)
        self.yes_button.setStyleSheet("""
        QPushButton {
            background-color: #43A047;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 6px 18px;
            font-size: 13px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #4CAF50;
        }

        QPushButton:pressed {
            background-color: #2E7D32;
        }
        """)
        self.no_button.setStyleSheet("""
        QPushButton {
            background-color: #DCDCDC;
            color: #DC143C;
            padding: 6px 18px;
            font-size: 13px;
            font-weight: bold;
            border-radius: 6px;
            border: 1px solid black;
            
        }
        
         QPushButton:hover {
            background-color: #D3D3D3;
        }
        """)
    
    # ------------------------------------------------------------------
    
    def _create_layout(self) -> None:
        """
        Создать компоновку окна.
        """
        
        content_layout = QHBoxLayout()
        
        content_layout.setSpacing(16)
        
        content_layout.addWidget(
            self.icon_label,
            alignment=Qt.AlignmentFlag.AlignTop,
        )
        
        text_layout = QVBoxLayout()
        
        text_layout.setSpacing(8)
        
        text_layout.addWidget(
            self.title_label,
        )
        
        text_layout.addWidget(
            self.text_label,
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
            self.yes_button,
        )
        
        buttons_layout.addWidget(
            self.no_button,
        )
        
        self.main_layout.addLayout(
            buttons_layout,
        )
    
    # ------------------------------------------------------------------
    
    def _connect_signals(self) -> None:
        """
        Подключить сигналы.
        """
        
        self.yes_button.clicked.connect(
            self._accept
        )
        
        self.no_button.clicked.connect(
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