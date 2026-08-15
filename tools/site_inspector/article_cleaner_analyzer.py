from __future__ import annotations

import re

from bs4 import Tag

from .constants import SELECTOR_BONUSES, SELECTOR_PENALTIES, TEXT_LENGTH_FACTOR, PARAGRAPH_SCORE, HEADING_SCORE, \
    LINK_PENALTY, LINK_DENSITY_THRESHOLD, LINK_DENSITY_PENALTY, CODE_BLOCK_SCORE, NOISE_NAV_SCORE, NOISE_SOCIAL_SCORE, \
    NOISE_DATE_SCORE, NOISE_REMOVE_THRESHOLD, TABLE_SCORE, IMAGE_SCORE, NOISE_CLASS_KEYWORDS, \
    AD_NETWORK_ID_PREFIXES, AD_NETWORK_CLASS_MARKERS
from .models import (
    ChildInfo,
    CleaningDecision,
    CleaningReport,
    ContainerAnalysis, NoiseInfo,
)

# ------------------------------------------------------------------

class ArticleCleanerAnalyzer:
    """
    Анализирует содержимое контейнера статьи и определяет,
    какие элементы следует оставить, а какие удалить.
    """

    # ------------------------------------------------------------------

    def analyze(
        self,
        analysis: ContainerAnalysis,
        root_element: Tag | None = None,
    ) -> CleaningReport:
        """
        Выполнить анализ контейнера статьи.

        Parameters
        ----------
        analysis:
            Анализ контейнера.

        root_element:
            Корневой HTML-элемент контейнера статьи (опционально).
            Нужен ТОЛЬКО для поиска рекламных слотов известных сетей
            (см. _find_ad_network_elements) — обычный скоринг работает
            по analysis.children (прямые дети) и root_element не
            требует, а рекламные слоты нужно искать РЕКУРСИВНО по
            всему поддереву, поэтому им нужен сам Tag, а не только
            ContainerAnalysis.

        Returns
        -------
        CleaningReport
        """

        keep: list[CleaningDecision] = []

        remove: list[CleaningDecision] = []

        for child in analysis.children:

            decision = self._analyze_child(
                child,
            )

            if decision.action == "keep":

                keep.append(
                    decision,
                )

            else:

                remove.append(
                    decision,
                )

        keep.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        remove.sort(
            key=lambda item: item.score,
        )

        if root_element is not None:

            remove.extend(
                self._find_ad_network_elements(
                    root_element,
                )
            )

        return CleaningReport(
            keep=keep,
            remove=remove,
        )

    # ------------------------------------------------------------------

    @staticmethod
    def _find_ad_network_elements(
            root: Tag,
    ) -> list[CleaningDecision]:
        """
        Найти рекламные слоты известных сетей рекурсивно по ВСЕМУ
        поддереву (не только среди прямых детей — обычный скоринг
        такие слоты часто пропускает, т.к. они лежат в безымянной
        div-обёртке на 2+ уровня глубже прямых детей).

        Селектор строится по НАЙДЕННОМУ ПРЕФИКСУ id/маркеру class,
        а не по полному id элемента — так один селектор покрывает
        все слоты сети сразу, независимо от случайного числового
        суффикса в их id (yandex_rtb_R-A-201190-1, ...-3, ...).

        Parameters
        ----------
        root:
            Корневой HTML-элемент контейнера статьи.

        Returns
        -------
        list[CleaningDecision]
        """

        found_selectors: set[str] = set()

        decisions: list[CleaningDecision] = []

        for tag in root.find_all(True):

            tag_id = (
                tag.get("id", "")
                or ""
            ).lower()

            for prefix in AD_NETWORK_ID_PREFIXES:

                if tag_id.startswith(prefix.lower()):

                    selector = f'{tag.name}[id^="{prefix}"]'

                    if selector not in found_selectors:

                        found_selectors.add(
                            selector,
                        )

                        decisions.append(
                            CleaningDecision(
                                selector=selector,
                                action="remove",
                                score=-100.0,
                                reason="ad-network",
                            )
                        )

                    break

            classes = [
                css_class.lower()
                for css_class in tag.get("class", [])
            ]

            for marker in AD_NETWORK_CLASS_MARKERS:

                if any(
                        marker in css_class
                        for css_class in classes
                ):

                    selector = f'{tag.name}[class*="{marker}"]'

                    if selector not in found_selectors:

                        found_selectors.add(
                            selector,
                        )

                        decisions.append(
                            CleaningDecision(
                                selector=selector,
                                action="remove",
                                score=-100.0,
                                reason="ad-network",
                            )
                        )

                    break

        return decisions

    # ------------------------------------------------------------------
    
    def _analyze_child(
            self,
            child: ChildInfo,
    ) -> CleaningDecision:
        """
        Принять решение по дочернему элементу.

        Parameters
        ----------
        child:
            Информация о дочернем элементе.

        Returns
        -------
        CleaningDecision
        """
        
        score = self._score(
            child,
        )
        
        noise = self._analyze_noise(
            child,
        )
        
        if noise is not None:
            return CleaningDecision(
                selector=child.selector,
                action="remove",
                score=score,
                reason=noise.reason,
            )
        
        if score > 0:
            return CleaningDecision(
                selector=child.selector,
                action="keep",
                score=score,
                reason="positive score",
            )
        
        return CleaningDecision(
            selector=child.selector,
            action="remove",
            score=score,
            reason="zero score",
        )

    # ------------------------------------------------------------------

    def _score(
        self,
        child: ChildInfo,
    ) -> float:
        """
        Вычислить полезность элемента.
        """

        score = 0.0

        score += self._score_text(
            child,
        )

        score += self._score_code(
            child,
        )

        score += self._score_tables(
            child,
        )

        score += self._score_images(
            child,
        )

        score += self._score_links(
            child,
        )

        score += self._score_selector(
            child,
        )

        return score

    # ------------------------------------------------------------------
    
    @staticmethod
    def _score_text(
            child: ChildInfo,
    ) -> float:
        """
        Оценить текстовое содержимое элемента.

        Parameters
        ----------
        child:
            Информация о дочернем элементе.

        Returns
        -------
        float
        """
        
        score = 0.0
        
        score += (
                child.text_length
                * TEXT_LENGTH_FACTOR
        )
        
        score += (
                child.paragraphs
                * PARAGRAPH_SCORE
        )
        
        score += (
                child.headings
                * HEADING_SCORE
        )
        
        return score

    # ------------------------------------------------------------------
    
    @staticmethod
    def _score_code(
            child: ChildInfo,
    ) -> float:
        """
        Оценить наличие блоков исходного кода.

        Parameters
        ----------
        child:
            Информация о дочернем элементе.

        Returns
        -------
        float
        """
        
        if child.code_blocks == 0:
            return 0.0
        
        score = (
                child.code_blocks
                * CODE_BLOCK_SCORE
        )
        
        return score

    # ------------------------------------------------------------------
    
    @staticmethod
    def _score_tables(
            child: ChildInfo,
    ) -> float:
        """
        Оценить наличие таблиц.

        Parameters
        ----------
        child:
            Информация о дочернем элементе.

        Returns
        -------
        float
            Дополнительная оценка за наличие таблиц.
        """
        
        if child.tables == 0:
            return 0.0
        
        return (
                child.tables
                * TABLE_SCORE
        )

    # ------------------------------------------------------------------
    
    @staticmethod
    def _score_images(
            child: ChildInfo,
    ) -> float:
        """
        Оценить наличие изображений.

        Parameters
        ----------
        child:
            Информация о дочернем элементе.

        Returns
        -------
        float
            Дополнительная оценка за наличие изображений.
        """
        
        if child.images == 0:
            return 0.0
        
        return (
                child.images
                * IMAGE_SCORE
        )

    # ------------------------------------------------------------------
    
    @staticmethod
    def _score_links(
            child: ChildInfo,
    ) -> float:
        """
        Оценить ссылочную насыщенность элемента.
        """
        
        if child.links == 0:
            return 0.0
        
        score = -(
                child.links
                * LINK_PENALTY
        )
        
        text = max(
            child.plain_text_length,
            1,
        )
        
        density = (
                child.link_text_length
                / text
        )
        
        if density > LINK_DENSITY_THRESHOLD:
            score -= LINK_DENSITY_PENALTY
        
        return score

    # ------------------------------------------------------------------
    
    @staticmethod
    def _score_selector(
            child: ChildInfo,
    ) -> float:
        """
        Оценить CSS-селектор элемента.
        """
        
        selector = child.selector.lower()
        
        score = 0.0
        
        for keyword, bonus in SELECTOR_BONUSES.items():
            
            if keyword in selector:
                score += bonus
        
        for keyword, penalty in SELECTOR_PENALTIES.items():
            
            if keyword in selector:
                score -= penalty
        
        return score
    
    # ------------------------------------------------------------------
    
    def _analyze_noise(
            self,
            child: ChildInfo,
    ) -> NoiseInfo | None:
        """
        Определить, является ли дочерний элемент потенциальным шумом.

        Parameters
        ----------
        child:
            Информация о дочернем элементе.

        Returns
        -------
        NoiseInfo | None
        """
        
        score = 0.0
        reasons: list[str] = []
        
        tokens = self._class_tokens(
            child,
        )
        
        matched = tokens & set(NOISE_CLASS_KEYWORDS)
        
        if matched:
            score += NOISE_SOCIAL_SCORE
            reasons.extend(sorted(matched))
        
        if child.links > 0 and child.plain_text_length == 0:
            score += NOISE_NAV_SCORE
            reasons.append("link-only")
        
        if score < NOISE_REMOVE_THRESHOLD:
            return None
        
        return NoiseInfo(
            selector=child.selector,
            score=score,
            reason=", ".join(reasons),
            remove=True,
        )
    
    # ------------------------------------------------------------------
    
    @staticmethod
    def _class_tokens(
            child: ChildInfo,
    ) -> set[str]:
        """
        Разбить class/id элемента на отдельные слова: по разделителям
        ("-", "_", пробел) и по границам camelCase ("socBlock" ->
        "soc", "Block"). Так ключевые слова сравниваются по целым
        словам, а не по случайной подстроке внутри более длинного
        слова (например "meta" не поймает "estimated", а "tag" не
        поймает "voltage" — токенизация режет по границам слов).
        """
        
        raw = " ".join(child.css_classes) + " " + child.css_id
        
        raw = re.sub(
            r"(?<=[a-zA-Zа-яА-Я0-9])(?=[A-ZА-Я][a-zа-я])",
            " ",
            raw,
        )
        
        parts = re.split(
            r"[^0-9a-zA-Zа-яА-Я]+",
            raw,
        )
        
        return {
            part.lower()
            for part in parts
            if part
        }