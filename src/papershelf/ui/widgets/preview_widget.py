from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView



class PreviewWidget(QWebEngineView):
    """
    Виджет предварительного просмотра статьи.

    Использует встроенный Chromium (Qt WebEngine),
    поэтому отображает HTML практически так же,
    как современные браузеры.

    Предназначен только для просмотра сохранённых
    статей и приветственной страницы.
    """

    # ------------------------------------------------------------------

    def __init__(self) -> None:
        super().__init__()
        
        self._show_welcome()

    # ------------------------------------------------------------------

    def _show_welcome(self) -> None:
        """
        Показать приветственную страницу.
        """

        self.setHtml(
            """
<!DOCTYPE html>

<html lang="ru">

<head>

<meta charset="utf-8">

<style>

body {

    max-width: 900px;

    margin: 50px auto;

    padding: 20px;

    font-family: Arial, sans-serif;

    line-height: 1.7;

    color: #222;

}

h2 {

    color: #2c3e50;

}

p {

    margin-top: 18px;

}

b {

    color: #0b74d1;

}

</style>

</head>

<body>

<h2>📚 PaperShelf</h2>

<p>

Вставьте ссылку на статью и нажмите
<b>«Сохранить статью»</b>.

</p>

<p>

После сохранения статья автоматически
отобразится здесь.

</p>

</body>

</html>
"""
        )

    
    
    # ------------------------------------------------------------------
    
    def load_article(
            self,
            directory: Path,
    ) -> None:
        """
        Загрузить сохранённую статью.

        Parameters
        ----------
        directory:
            Каталог статьи.
        """
        
        html_file = directory / "article.html"
        
        if not html_file.exists():
            self.setHtml(
                f"""
    <!DOCTYPE html>

    <html>

    <body>

    <h3>Ошибка</h3>

    <p>

    Не найден файл

    <b>{html_file.name}</b>

    </p>

    </body>

    </html>
    """
            )
            
            return
        
        html = html_file.read_text(
            encoding="utf-8",
        )
        
        base_url = QUrl.fromLocalFile(
            str(html_file.resolve())
        )
        
        self.setHtml(
            html,
            base_url,
        )

    # ------------------------------------------------------------------

    def clear_preview(self) -> None:
        """
        Очистить область просмотра.

        Вместо статьи отображается приветственная
        страница приложения.
        """

        self._show_welcome()