from __future__ import annotations

from bs4 import Tag

from .models import CleaningReport

# ------------------------------------------------------------------


class ArticleCleaner:
    """
    Очищает HTML-контейнер статьи от служебных элементов.

    Класс отвечает только за физическое удаление элементов.
    Решения о том, что удалить, принимает
    ArticleCleanerAnalyzer.
    """

    # ------------------------------------------------------------------

    def clean(
        self,
        element: Tag,
        report: CleaningReport,
    ) -> Tag:
        """
        Очистить HTML-контейнер согласно отчёту.

        Parameters
        ----------
        element:
            Корневой HTML-контейнер.

        report:
            Отчёт анализатора очистки.

        Returns
        -------
        Tag
            Очищенный HTML-контейнер.
        """

        selectors = {
            decision.selector
            for decision in report.remove
        }

        for selector in selectors:
            self._remove(
                element,
                selector,
            )

        return element

    # ------------------------------------------------------------------

    @staticmethod
    def _remove(
        element: Tag,
        selector: str,
    ) -> None:
        """
        Удалить непосредственные дочерние элементы
        по CSS-селектору.

        Parameters
        ----------
        element:
            Корневой HTML-контейнер.

        selector:
            CSS-селектор удаляемых элементов.
        """

        for child in element.find_all(
            recursive=False,
        ):
            if not isinstance(
                child,
                Tag,
            ):
                continue

            if child.select_one(selector) is child:
                print(
                    "REMOVE:",
                    child.name,
                    child.get("id", ""),
                    child.get("class", []),
                    "images=",
                    len(child.find_all("img")),
                )
                child.decompose()