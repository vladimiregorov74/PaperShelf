from __future__ import annotations

from papershelf.models import LibraryItem
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

        self._service = LibraryService(scanner)

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