from __future__ import annotations

from pathlib import Path

#
# Корень проекта PaperShelf
#
PROJECT_ROOT = Path(__file__).resolve().parents[3]

#
# Каталог со всеми сохранёнными статьями
#
SAVED_DIR = PROJECT_ROOT / "saved"