# PaperShelf

Desktop application for saving and organizing web articles.

## Features

- Save articles as standalone HTML
- Download images
- Offline reading
- Built with PySide6

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
