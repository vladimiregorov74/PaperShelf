from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from papershelf.core.paths import APP_ICON_FILE
from papershelf.ui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)

    app.setWindowIcon(
        QIcon(str(APP_ICON_FILE))
    )

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())