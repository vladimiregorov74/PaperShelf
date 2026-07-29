from __future__ import annotations

from pathlib import Path
from PySide6.QtCore import (
    Qt,
    Signal,
    QPoint,
)
from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QMenu,
)

from papershelf.models import LibraryItem


class LibraryWidget(QListWidget):
    """
    Виджет библиотеки статей.
    """

    article_selected = Signal(LibraryItem)
    
    open_folder_requested = Signal(LibraryItem)
    
    open_original_requested = Signal(LibraryItem)
    
    delete_requested = Signal(LibraryItem)

    # ------------------------------------------------------------------

    def __init__(self) -> None:
        super().__init__()

        self._items: list[LibraryItem] = []

        self.setAlternatingRowColors(True)

        self.setSelectionMode(
            self.SelectionMode.SingleSelection
        )
        
        self.itemDoubleClicked.connect(
            self._item_double_clicked
        )
        
        self.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        
        self.customContextMenuRequested.connect(
            self._show_context_menu
        )

    # ------------------------------------------------------------------

    def set_articles(
        self,
        articles: list[LibraryItem],
    ) -> None:
        """
        Загрузить список статей.
        """
 
        self.clear()

        self._items = articles

        for article in articles:
            item = QListWidgetItem()

            item.setText(
                article.title
            )

            item.setToolTip(
                (
                    f"{article.title}\n\n"
                    f"Автор: {article.author}\n"
                    f"Источник: {article.source}"
                )
            )

            self.addItem(item)


    # ------------------------------------------------------------------

    def _item_double_clicked(
        self,
        item: QListWidgetItem,
    ) -> None:
        """
        Пользователь дважды щёлкнул по статье.
        """

        index = self.row(item)

        if index < 0:
            return

        self.article_selected.emit(
            self._items[index]
        )
    
    # ------------------------------------------------------------------
    
    def select_article(
            self,
            directory: Path,
    ) -> None:
        """
        Выделить статью по каталогу.
        """
        
        for index, article in enumerate(self._items):
            
            if article.directory != directory:
                continue
            
            item = self.item(index)
            
            if item is None:
                return
            
            self.setCurrentItem(item)
            
            self.scrollToItem(item)
            
            self.article_selected.emit(
                article
            )
            
            return
    

    # ------------------------------------------------------------------
    
    def current_article(self) -> LibraryItem | None:
        """
        Возвращает выбранную статью.
        """
        
        row = self.currentRow()
        
        if row < 0:
            return None
        
        if row >= len(self._items):
            return None
        
        return self._items[row]
    
    # ------------------------------------------------------------------
    
    def _show_context_menu(
            self,
            position: QPoint,
    ) -> None:
        """
        Контекстное меню статьи.
        """
        
        item = self.itemAt(position)
        
        if item is None:
            return
        
        index = self.row(item)
        
        if index < 0:
            return
        
        article = self._items[index]
        
        menu = QMenu(self)
        
        open_action = menu.addAction("📖 Открыть")
        
        menu.addSeparator()
        
        open_folder_action = menu.addAction(
            "📂 Открыть папку"
        )
        
        open_original_action = menu.addAction(
            "🌍 Открыть оригинал"
        )
        
        menu.addSeparator()
        
        delete_action = menu.addAction(
            "🗑 Удалить статью"
        )
        
        action = menu.exec(
            self.mapToGlobal(position)
        )
        
        if action == open_action:
            self.article_selected.emit(article)
        
        elif action == open_folder_action:
            self.open_folder_requested.emit(article)
        
        elif action == open_original_action:
            self.open_original_requested.emit(article)
        
        elif action == delete_action:
            self.delete_requested.emit(article)
