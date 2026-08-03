from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from papershelf.models import LibraryItem
from papershelf.ui.widgets.library_widget import LibraryWidget


class LibraryPanel(QWidget):
    """
    Панель библиотеки.
    """

    article_selected = Signal(LibraryItem)
    
    open_folder_requested = Signal(LibraryItem)
    
    open_original_requested = Signal(LibraryItem)
    
    delete_requested = Signal(LibraryItem)

    # ------------------------------------------------------------------

    def __init__(self) -> None:
        super().__init__()
        
        self._articles: list[LibraryItem] = []
        self._create_widgets()
        self._create_layout()
        self._connect_signals()

    # ------------------------------------------------------------------

    def _create_widgets(self) -> None:

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "🔍 Поиск..."
        )
        self.search.setClearButtonEnabled(True)
        self.library = LibraryWidget()

    # ------------------------------------------------------------------

    def _create_layout(self) -> None:

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.addWidget(
            self.search,
        )

        layout.addWidget(
            self.library,
            1,
        )

    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:

        self.library.article_selected.connect(
            self.article_selected
        )
        self.search.textChanged.connect(
            self._filter_articles
        )
        self.library.open_folder_requested.connect(
            self.open_folder_requested
        )
        
        self.library.open_original_requested.connect(
            self.open_original_requested
        )
        
        self.library.delete_requested.connect(
            self.delete_requested
        )

    # ------------------------------------------------------------------

    def set_articles(
            self,
            articles: list[LibraryItem],
    ) -> None:
        self._articles = articles
        
        self.library.set_articles(
            articles
        )

    # ------------------------------------------------------------------

    def current_article(self):

        return self.library.current_article()

    # ------------------------------------------------------------------

    def select_article(
        self,
        directory,
    ) -> None:

        self.library.select_article(
            directory
        )
    
    # ------------------------------------------------------------------
    
    def _filter_articles(
            self,
            text: str,
    ) -> None:
        """
        Фильтрация библиотеки.
        """
        
        text = text.lower().strip()
        
        if not text:
            self.library.set_articles(
                self._articles
            )
            return
        
        filtered = []
        
        for article in self._articles:
            
            haystack = (
                f"{article.title} "
                f"{article.author} "
                f"{article.source}"
            ).lower()
            
            if text in haystack:
                filtered.append(article)
        
        self.library.set_articles(
            filtered
        )