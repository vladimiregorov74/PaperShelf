from __future__ import annotations

from pathlib import Path

from papershelf.config.constants import LOG_DIRECTORY, LOG_FILENAME

#
# Корень проекта PaperShelf
#
PROJECT_ROOT = Path(__file__).resolve().parents[3]

#
# Каталог со всеми сохранёнными статьями
#
SAVED_DIR = PROJECT_ROOT / "saved"

LOGS_DIR = PROJECT_ROOT / LOG_DIRECTORY
LOG_FILE = LOGS_DIR / LOG_FILENAME