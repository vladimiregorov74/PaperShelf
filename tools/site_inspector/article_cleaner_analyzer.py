from __future__ import annotations

from .constants import SELECTOR_BONUSES, SELECTOR_PENALTIES, TEXT_LENGTH_FACTOR, PARAGRAPH_SCORE, HEADING_SCORE, \
    LINK_PENALTY, LINK_DENSITY_THRESHOLD, LINK_DENSITY_PENALTY, CODE_BLOCK_SCORE, NOISE_NAV_SCORE, NOISE_SOCIAL_SCORE, \
    NOISE_DATE_SCORE, NOISE_REMOVE_THRESHOLD, TABLE_SCORE, IMAGE_SCORE
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
    ) -> CleaningReport:
        """
        Выполнить анализ контейнера статьи.

        Parameters
        ----------
        analysis:
            Анализ контейнера.

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

        return CleaningReport(
            keep=keep,
            remove=remove,
        )

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
        
        classes = {
            css_class.lower()
            for css_class in child.css_classes
        }
        
        if "nav" in classes:
            score += NOISE_NAV_SCORE
            reasons.append("navigation")
        
        if (
                "social" in classes
                or "socblock" in classes
        ):
            score += NOISE_SOCIAL_SCORE
            reasons.append("social")
        
        if "date" in classes:
            score += NOISE_DATE_SCORE
            reasons.append("date")
        
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