from __future__ import annotations

from PySide6.QtCore import QSettings

from papershelf.config.constants import (
    APP_NAME,
    FILE_LOGGING_KEY,
    ORGANIZATION_NAME, LOG_PANEL_VISIBLE_KEY,
)


class AppSettings:
    """
    Работа с настройками приложения.

    Является единственной точкой доступа к QSettings.
    """
    
    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------
    
    def __init__(self) -> None:
        self._settings = self._create_settings()
    
    # ------------------------------------------------------------------
    
    @staticmethod
    def _create_settings() -> QSettings:
        """
        Создать объект QSettings.
        """
        
        return QSettings(
            ORGANIZATION_NAME,
            APP_NAME,
        )
    
    # ------------------------------------------------------------------
    # File logging
    # ------------------------------------------------------------------

    def file_logging_enabled(self) -> bool:
        """
        Возвращает состояние записи журнала в файл.
        """

        return self._settings.value(
            FILE_LOGGING_KEY,
            False,
            type=bool,
        )

    # ------------------------------------------------------------------

    def set_file_logging(
        self,
        enabled: bool,
    ) -> None:
        """
        Включить или отключить запись журнала в файл.

        Parameters
        ----------
        enabled:
            Новое состояние.
        """

        self._settings.setValue(
            FILE_LOGGING_KEY,
            enabled,
        )
    
    # ------------------------------------------------------------------
    # Log panel
    # ------------------------------------------------------------------
    
    def log_panel_visible(self) -> bool:
        """
        Возвращает состояние отображения панели логирования.
        """
        
        return self._settings.value(
            LOG_PANEL_VISIBLE_KEY,
            False,
            type=bool,
        )
    
    # ------------------------------------------------------------------
    
    def set_log_panel_visible(
            self,
            visible: bool,
    ) -> None:
        """
        Изменить состояние отображения панели логирования.

        Parameters
        ----------
        visible:
            Новое состояние.
        """
        
        self._settings.setValue(
            LOG_PANEL_VISIBLE_KEY,
            visible,
        )