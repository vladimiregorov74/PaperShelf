from __future__ import annotations

from papershelf.models import LibraryItem
from papershelf.services.library_metadata_service import (
    LibraryMetadataService,
)
from papershelf.services.library_scanner import LibraryScanner
from papershelf.services.library_service import LibraryService


class LibraryController:
    """
    Контроллер библиотеки.

    Назначение
    ----------
    Координирует работу со списком сохранённых статей.

    Контроллер предоставляет простой интерфейс
    пользовательскому интерфейсу и делегирует
    выполнение операций LibraryService.

    Не отвечает за:

    - отображение библиотеки;
    - работу с Qt;
    - открытие статьи;
    - удаление статьи;
    - открытие папок.

    Эти задачи относятся к другим компонентам приложения.
    """

    # ------------------------------------------------------------------

    def __init__(
        self,
        scanner: LibraryScanner,
    ) -> None:
        """
        Parameters
        ----------
        scanner:
            Сканер библиотеки.
        """

        metadata_service = LibraryMetadataService()

        self._service = LibraryService(
            scanner=scanner,
            metadata_service=metadata_service,
        )

    # ------------------------------------------------------------------

    def reload(
        self,
    ) -> list[LibraryItem]:
        """
        Перезагрузить библиотеку.

        Returns
        -------
        list[LibraryItem]
            Список сохранённых статей.
        """

        return self._service.reload()

    # ------------------------------------------------------------------

    def sort_by_date(
        self,
    ) -> list[LibraryItem]:
        """
        Отсортировать библиотеку по дате.

        Returns
        -------
        list[LibraryItem]
            Отсортированный список статей.
        """

        return self._service.sort_by_date()

    # ------------------------------------------------------------------

    def sort_by_title(
        self,
    ) -> list[LibraryItem]:
        """
        Отсортировать библиотеку по названию.

        Returns
        -------
        list[LibraryItem]
            Отсортированный список статей.
        """

        return self._service.sort_by_title()

    # ------------------------------------------------------------------

    def rename(
        self,
        item: LibraryItem,
        title: str,
    ) -> None:
        """
        Изменить название статьи.

        Parameters
        ----------
        item:
            Элемент библиотеки.

        title:
            Новое название статьи.
        """

        self._service.rename(
            item=item,
            title=title,
        )