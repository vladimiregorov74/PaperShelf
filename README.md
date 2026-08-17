# PaperShelf

Настольное приложение для сохранения и систематизации веб-статей.

## Features

- Сохраняет статьи как отдельный HTML.
- Загрузка изображений
- Офлайн чтение
- Построен с помощью PySide6.

src/
└── papershelf/
    ├── app.py               # Точка входа
    │
    ├── config/              # Константы и настройки
    ├── controllers/         # Координация сценариев
    ├── core/                # Общие базовые компоненты
    ├── models/              # Модели данных
    ├── parsers/             # Парсеры сайтов
    ├── services/            # Сервисы
    ├── ui/                  # Интерфейс
    ├── workers/             # Фоновые задачи
    ├── resources/           # Иконки, стили, шаблоны
    └── saved/               # (опционально, если захотим хранить внутри)
tools/
└── site_inspector                    # Анализ сайта и формирования селекторов
    └── inspect_site.py               # Точка входа для анализа сайта

Теперь у нас работает цепочка:

Пользователь вводит URL.
ParserFactory находит конфигурацию(соответсвующие селекторы в selectors.py) → по селекторам сохраняется статья.
ParserFactory не находит конфигурацию → UnsupportedSiteError.
SaveWorker отправляет сигнал unsupported_site.
MainWindow показывает диалог.
Пользователь соглашается.
Запускается SiteSupportController.
SiteInspector анализирует сайт.
Обновляются:
selectors.py;
site_registry_data.py.
get_site_configs() перечитывает их.
SaveController.retry().
Статья успешно скачивается.


В случае если поменялась структура сайта и статья грузится криво или вообще не грузится, при этом сайт находится
в базе уже записаных селекторов, то можно вручную удалить сайт из src/papershelf/parsers/site_registry_data.py и 
src/papershelf/parsers/selectors.py