from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableView,
)

from papershelf.services.site_registry_editor import SiteRegistryEditor
from papershelf.services.site_registry_service import (
    SiteRegistryService,
)
from papershelf.ui.dialogs.base_dialog import BaseDialog
import importlib

from papershelf.parsers import (
    selectors,
    site_registry,
    site_registry_data,
)

class SupportedSitesDialog(BaseDialog):
    """
    Диалог управления поддерживаемыми сайтами.
    """

    # ------------------------------------------------------------------

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self._service = SiteRegistryService()
        
        self._editor = SiteRegistryEditor()

        self._create_widgets()

        self._create_layout()

        self._connect_signals()

        self._load_sites()
    
    # ------------------------------------------------------------------

    def _create_widgets(self, ) -> None:
        """
        Создать элементы интерфейса.
        """

        self.setWindowTitle(
            "Поддерживаемые сайты",
        )

        self.resize(
            700,
            450,
        )

        self._table = QTableView()

        self._model = QStandardItemModel()
        
        # self._refresh_button = QPushButton(
        #     "Обновить",
        # )

        self._delete_button = QPushButton(
            "Удалить",
        )

        self._close_button = QPushButton(
            "Закрыть",
        )
        
        self._model.setHorizontalHeaderLabels(
            (
                "ID",
                "Источник",
                "Домен",
                "Суффикс",
            )
        )

        self._table.setModel(
            self._model,
        )

        self._table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows,
        )

        self._table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection,
        )

        self._table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers,
        )

        self._table.verticalHeader().hide()

        self._table.horizontalHeader().setStretchLastSection(
            True,
        )

        self._table.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.ResizeToContents,
        )

        self._table.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.Stretch,
        )

        self._table.horizontalHeader().setSectionResizeMode(
            2,
            QHeaderView.ResizeMode.ResizeToContents,
        )

        self._delete_button.setEnabled(False)
        
        self._help_label = QLabel(
            (
                "<b>💡 Статья скачивается неправильно?</b><br><br>"
                
                "Возможно, структура сайта изменилась. "
                "Удалите поддержку сайта из списка и повторите скачивание.. "
                "PaperShelf автоматически заново определит "
                "структуру страницы и создаст новые селекторы."
            )
        )
        
        self._help_label.setWordWrap(True)
    
    # ------------------------------------------------------------------

    def _create_layout(
            self,
    ) -> None:
        """
        Создать разметку окна.
        """

        self.main_layout.addWidget(

            self.create_section_title(
                "Поддерживаемые сайты",
            )

        )
        self.main_layout.addWidget(
            self.create_description(
                "Список сайтов, поддерживаемых PaperShelf."
            )
        )
        
        self.main_layout.addWidget(
            self._help_label,
        )
        
        self.main_layout.addWidget(
            self._table,
        )

        self.add_buttons(

            # self._refresh_button,
            self._delete_button,
            self._close_button,

        )
    
    # ------------------------------------------------------------------

    def _connect_signals(
            self,
    ) -> None:
        """
        Подключить сигналы.
        """
        
        # self._refresh_button.clicked.connect(
        #     self._load_sites,
        # )
        self._close_button.clicked.connect(
            self.close,
        )
        self._table.selectionModel().selectionChanged.connect(
	        lambda: self._delete_button.setEnabled(
		        self._selected_site() is not None,
	        )
        )
        
        self._delete_button.clicked.connect(
            self._delete_site,
        )
    
    # ------------------------------------------------------------------

    def _load_sites(
            self,
    ) -> None:
        """
        Загрузить список поддерживаемых сайтов.
        """

        self._model.removeRows(
            0,
            self._model.rowCount(),
        )

        for site in self._service.get_sites():
            identifier_item = QStandardItem(
                site.identifier,
            )
            
            source_item = QStandardItem(
                site.source,
            )
            
            domain_item = QStandardItem(
                site.domain,
            )
            
            suffix_item = QStandardItem(
                site.title_suffix,
            )

            self._model.appendRow(
                (
                    identifier_item,
                    source_item,
                    domain_item,
                    suffix_item,
                )
            )
    
    # ------------------------------------------------------------------
    
    def _selected_site(
            self,
    ) -> str | None:
        """
        Вернуть идентификатор выбранного сайта.
        """
        
        indexes = self._table.selectionModel().selectedRows()
        
        if not indexes:
            return None
        
        return self._model.item(
            indexes[0].row(),
            0,
        ).text()
    
    # ------------------------------------------------------------------
    
    def _delete_site(
            self,
    ) -> None:
        """
        Удалить выбранный сайт.
        """
        
        identifier = self._selected_site()
        
        if identifier is None:
            return
        
        answer = QMessageBox.question(
            self,
            "Удаление сайта",
            (
                f"Удалить поддержку сайта\n\n"
                f"{identifier}?"
            ),
        )
        
        if answer != QMessageBox.StandardButton.Yes:
            return
        
        self._editor.remove(
            identifier,
        )
        
        importlib.reload(site_registry_data)
        importlib.reload(selectors)
        importlib.reload(site_registry)
        
        self._load_sites()