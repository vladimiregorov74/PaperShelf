from __future__ import annotations

from pathlib import Path
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QListWidget, QListWidgetItem

from papershelf.models import LibraryItem


class LibraryWidget(QListWidget):
    """
    Виджет библиотеки статей.
    """

    article_selected = Signal(LibraryItem)

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
            
            return
    
    # ------------------------------------------------------------------
    
    def current_article(self) -> LibraryItem | None:
        """
        Вернуть выбранную статью.
        """
        
        row = self.currentRow()
        
        if row < 0:
            return None
        
        return self._items[row]
