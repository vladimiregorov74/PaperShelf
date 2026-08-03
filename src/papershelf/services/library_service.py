from __future__ import annotations

from papershelf.models import LibraryItem
from papershelf.services.library_scanner import LibraryScanner


class LibraryService:
    """
    Сервис работы с библиотекой.

    Назначение
    ----------
    Выполняет все операции,
    связанные со списком сохранённых статей.

    Сервис полностью скрывает детали
    сканирования библиотеки и способа
    сортировки.

    В дальнейшем сервис будет отвечать за:

    • обновление библиотеки;

    • поиск;

    • сортировку;

    • фильтрацию;

    • избранное.
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

        self._scanner = scanner
        self._sort_mode: str = "date"

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

        return self._load()

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

        self._set_sort_mode("date")

        return self.reload()

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

        self._set_sort_mode("title")

        return self.reload()

    # ------------------------------------------------------------------

    def _load(
        self,
    ) -> list[LibraryItem]:
        """
        Загрузить библиотеку.

        Returns
        -------
        list[LibraryItem]
            Список найденных статей.
        """

        return self._scanner.scan(
            sort_by=self._sort_mode,
        )

    # ------------------------------------------------------------------

    def _set_sort_mode(
        self,
        mode: str,
    ) -> None:
        """
        Изменить текущий способ сортировки.

        Parameters
        ----------
        mode:
            Новый способ сортировки.
        """

        self._sort_mode = mode