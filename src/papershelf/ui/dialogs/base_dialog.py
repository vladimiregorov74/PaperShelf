from __future__ import annotations

from PySide6.QtWidgets import (
	QDialog,
	QHBoxLayout,
	QLabel,
	QPushButton,
	QVBoxLayout,
	QWidget, QLineEdit,
)

from papershelf.ui.styles.button_styles import SUCCESS_BUTTON_STYLE, SECONDARY_BUTTON_STYLE


class BaseDialog(QDialog):
    """
    Базовый диалог приложения PaperShelf.

    Является основой для всех диалоговых окон приложения.
    Обеспечивает единый внешний вид и общие элементы интерфейса.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.main_layout = QVBoxLayout(self)

        self._configure()

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def _configure(self) -> None:
        """
        Настроить внешний вид окна.
        """

        self.setWindowTitle("PaperShelf")

        self.setMinimumWidth(430)

        self.main_layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        self.main_layout.setSpacing(16)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def create_section_title(
        self,
        text: str,
    ) -> QLabel:
        """
        Создать заголовок раздела.

        Parameters
        ----------
        text:
            Текст заголовка.

        Returns
        -------
        QLabel
            Настроенный виджет заголовка.
        """

        label = QLabel(text)

        font = label.font()
        font.setBold(True)
        font.setPointSize(
            font.pointSize() + 1,
        )

        label.setFont(font)

        return label

    # ------------------------------------------------------------------

    def add_buttons(
        self,
        *buttons: QPushButton,
    ) -> None:
        """
        Добавить панель кнопок.

        Parameters
        ----------
        *buttons:
            Кнопки, отображаемые справа налево.
        """

        layout = QHBoxLayout()

        layout.addStretch()

        for button in buttons:
            layout.addWidget(button)

        self.main_layout.addLayout(layout)
    
    # ------------------------------------------------------------------
    
    def create_description(
            self,
            text: str,
    ) -> QLabel:
        """
        Создать поясняющий текст.

        Parameters
        ----------
        text:
            Текст описания.

        Returns
        -------
        QLabel
            Настроенная подпись.
        """
        
        label = QLabel(text)
        
        label.setWordWrap(True)
        
        label.setStyleSheet(
            """
            color: #606060;
            """
        )
        
        return label
    
    # ------------------------------------------------------------------
    
    def add_field(
            self,
            title: str,
            widget: QWidget,
    ) -> None:
        """
        Добавить поле с заголовком.

        Parameters
        ----------
        title:
            Название поля.

        widget:
            Виджет ввода.
        """
        
        self.main_layout.addWidget(
            self.create_section_title(title)
        )
        
        self.main_layout.addWidget(
            widget
        )

    def _create_widgets(
            self,
            source: str,
            title_suffix: str,
    ) -> None:
        """
        Создать элементы интерфейса.
        """

        self._source_edit = QLineEdit()
        self._source_edit.setText(source)

        self._title_suffix_edit = QLineEdit()
        self._title_suffix_edit.setText(title_suffix)

        self._description = self.create_description(
            "Если заголовок страницы содержит название сайта, "
            "укажите суффикс, который нужно удалить.\n\n"
            "Например:\n"
            "    | Metanit\n"
            "    / Хабр"
        )

        self._ok_button = QPushButton(
            f"Сохранить разметку\n  и скачать"
        )

        self._cancel_button = QPushButton(
            "Отмена"
        )

        self._ok_button.setStyleSheet(
            SUCCESS_BUTTON_STYLE
        )

        self._cancel_button.setStyleSheet(
            SECONDARY_BUTTON_STYLE
        )

    