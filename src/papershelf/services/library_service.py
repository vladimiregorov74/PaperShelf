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

    MainWindow не должна знать,
    каким образом происходит сканирование
    библиотеки и сортировка.

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

        self._scanner = scanner
        
        self._sort_mode = "date"

    # ------------------------------------------------------------------

    def load(
        self,
        sort_by: str = "date",
    ) -> list[LibraryItem]:
        """
        Загрузить библиотеку.

        Parameters
        ----------
        sort_by:
            Способ сортировки.

        Returns
        -------
        list[LibraryItem]
        """

        return self._scanner.scan(
            sort_by=sort_by,
        )
    # ------------------------------------------------------------------

    def set_sort_mode(
        self,
        mode: str,
    ) -> None:
        """
        Изменить способ сортировки библиотеки.

        Parameters
        ----------
        mode:
            Новый способ сортировки.
        """

        self._sort_mode = mode
        
    # ------------------------------------------------------------------

    def reload(
        self,
    ) -> list[LibraryItem]:
        """
        Перезагрузить библиотеку.

        Returns
        -------
        list[LibraryItem]
        """

        return self.load(
            self._sort_mode
        )