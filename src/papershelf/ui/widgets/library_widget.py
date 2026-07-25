from __future__ import annotations

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

        self.itemClicked.connect(
            self._item_clicked
        )

    # ------------------------------------------------------------------

    def set_articles(
        self,
        articles: list[LibraryItem],
    ) -> None:
        """
        Загрузить список статей.
        """
        print(f"Получено статей: {len(articles)}")  ##
        self.clear()

        self._items = articles

        for article in articles:
            print(article.title)
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
        
        print("Элементов в QListWidget:", self.count())  ###

    # ------------------------------------------------------------------

    def _item_clicked(
        self,
        item: QListWidgetItem,
    ) -> None:
        """
        Пользователь выбрал статью.
        """

        index = self.row(item)

        if index < 0:
            return

        self.article_selected.emit(
            self._items[index]
        )