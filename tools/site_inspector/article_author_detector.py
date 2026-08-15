from __future__ import annotations

import re

from bs4 import BeautifulSoup, Tag

from .css_utils import build_selector

# ------------------------------------------------------------------

AUTHOR_CLASS_KEYWORDS = {
    "author",
    "byline",
    "writer",
    "journalist",
    "columnist",
}

# Автор часто лежит вне найденного контейнера статьи (например, в
# шапке карточки статьи рядом с датой публикации, а не внутри самого
# текста) — поэтому детектор ищет по всей странице, а не только
# внутри ArticleCandidate.element.

MAX_AUTHOR_TEXT_LENGTH = 80

MAX_AUTHOR_LINKS = 3

# ------------------------------------------------------------------


class ArticleAuthorDetector:
    """
    Поиск блока автора статьи на странице.

    Класс отвечает только за поиск кандидатов в CSS-селекторы
    автора. Собственно текст автора нигде не извлекается.
    """

    # ------------------------------------------------------------------

    def detect(
            self,
            soup: BeautifulSoup,
    ) -> list[str]:
        """
        Найти кандидатов в селекторы блока автора.

        Parameters
        ----------
        soup:
            Разобранная страница целиком.

        Returns
        -------
        list[str]
            Список CSS-селекторов кандидатов, без дубликатов,
            в порядке обнаружения. Может быть пустым, если на
            странице автор не указан.
        """

        candidates: list[str] = []

        candidates.extend(
            self._meta_candidates(
                soup,
            )
        )

        candidates.extend(
            self._markup_candidates(
                soup,
            )
        )

        return self._deduplicate(
            candidates,
        )

    # ------------------------------------------------------------------

    @staticmethod
    def _meta_candidates(
            soup: BeautifulSoup,
    ) -> list[str]:
        """
        Найти автора через meta-теги в <head>.

        Parameters
        ----------
        soup:
            Разобранная страница целиком.

        Returns
        -------
        list[str]
        """

        candidates: list[str] = []

        if soup.find(
                "meta",
                attrs={"name": "author"},
        ):
            candidates.append(
                'meta[name="author"]',
            )

        if soup.find(
                "meta",
                attrs={"property": "article:author"},
        ):
            candidates.append(
                'meta[property="article:author"]',
            )

        return candidates

    # ------------------------------------------------------------------

    @classmethod
    def _markup_candidates(
            cls,
            soup: BeautifulSoup,
    ) -> list[str]:
        """
        Найти автора через видимую разметку: rel="author",
        itemprop="author" и класс/id, содержащие слово
        "author"/"byline"/... среди отдельных токенов.

        Parameters
        ----------
        soup:
            Разобранная страница целиком.

        Returns
        -------
        list[str]
        """

        candidates: list[str] = []

        for tag in soup.find_all(True):

            rel = tag.get("rel")

            if rel and "author" in rel:
                candidates.append(
                    cls._selector(tag),
                )
                continue

            if tag.get("itemprop") == "author":
                candidates.append(
                    cls._selector(tag),
                )
                continue

            if (
                    cls._matches_author_keywords(tag)
                    and cls._is_plausible_author_block(tag)
            ):
                candidates.append(
                    cls._selector(tag),
                )

        return candidates

    # ------------------------------------------------------------------

    @staticmethod
    def _matches_author_keywords(
            tag: Tag,
    ) -> bool:
        """
        Проверить, содержит ли class/id элемента слово из
        AUTHOR_CLASS_KEYWORDS как отдельный токен (не подстроку).

        Разбиение на токены — по "-", "_", пробелу и границам
        camelCase, поэтому "tm-user-info.author" совпадёт по токену
        "author", а случайное слово вроде "unauthorized" — нет
        (там нет отдельного токена "author").

        Parameters
        ----------
        tag:
            HTML-элемент.

        Returns
        -------
        bool
        """

        raw = (
                " ".join(tag.get("class", []))
                + " "
                + (tag.get("id") or "")
        )

        raw = re.sub(
            r"(?<=[a-zA-Zа-яА-Я0-9])(?=[A-ZА-Я][a-zа-я])",
            " ",
            raw,
        )

        tokens = {
            part.lower()
            for part in re.split(
                r"[^0-9a-zA-Zа-яА-Я]+",
                raw,
            )
            if part
        }

        return bool(
            tokens & AUTHOR_CLASS_KEYWORDS,
        )

    # ------------------------------------------------------------------

    @staticmethod
    def _is_plausible_author_block(
            tag: Tag,
    ) -> bool:
        """
        Отсечь совпадения, которые явно не блок с именем автора:
        слишком длинный текст (скорее целая статья/секция, у которой
        случайно оказался подходящий класс) или слишком много ссылок
        (похоже на навигацию/список, а не на одно имя).

        Parameters
        ----------
        tag:
            HTML-элемент.

        Returns
        -------
        bool
        """

        text = tag.get_text(
            strip=True,
        )

        if not text or len(text) > MAX_AUTHOR_TEXT_LENGTH:
            return False

        if len(tag.find_all("a")) > MAX_AUTHOR_LINKS:
            return False

        return True

    # ------------------------------------------------------------------

    @staticmethod
    def _selector(
            tag: Tag,
    ) -> str:
        """
        Построить CSS-селектор элемента (tag + id/class).

        Parameters
        ----------
        tag:
            HTML-элемент.

        Returns
        -------
        str
        """

        return build_selector(
            tag,
        )

    # ------------------------------------------------------------------

    @staticmethod
    def _deduplicate(
            candidates: list[str],
    ) -> list[str]:
        """
        Убрать дубликаты, сохранив порядок первого появления.

        Parameters
        ----------
        candidates:
            Список селекторов-кандидатов.

        Returns
        -------
        list[str]
        """

        seen: set[str] = set()

        result: list[str] = []

        for candidate in candidates:

            if candidate in seen:
                continue

            seen.add(candidate)

            result.append(candidate)

        return result
