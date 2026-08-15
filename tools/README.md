Для вызова инспектора достаточно вызвать терминал в корне проекта и выполнить

bash
poetry run python tools/inspect_site.py https://metanit.com/python/database/2.2.php

где https://metanit.com/python/database/2.2.php - иследуемый сайт

--source и --title-suffix — это флаги CLI-инструмента tools/inspect_site.py, оба необязательные.

--source — отображаемое имя источника, которое попадёт в Article.source (то, что видит пользователь как «откуда 
статья» — например в библиотеке сохранённых статей). Детектор не может это надёжно угадать по домену — есть только 
грубый дефолт (dan-it.com.ua → Dan It), который не всегда совпадает с тем, как вы хотите называть источник по факту 
(например DAN IT Education вместо Dan It).

bash
poetry run python tools/inspect_site.py https://dan-it.com.ua/... --source "DAN IT Education"

--title-suffix — «хвост» в <title> страницы, который нужно отрезать при извлечении заголовка статьи. У многих сайтов 
<title> выглядит как "Название статьи / БрендСайта" или "Название статьи | БрендСайта", и без обрезки в Article.title 
попадает лишний брендинг. Это тоже нельзя определить автоматически — вопрос конкретной вёрстки конкретного сайта.

bash
poetry run python tools/inspect_site.py https://habr.com/... --title-suffix " / Хабр"

Без этого флага у Habr Article.title был бы "Визуализация на Python за 15 минут... / Хабр" вместо просто "Визуализация 
на Python за 15 минут...".

Оба флага пишутся в site_registry_data.py (через SiteRegistryGenerator) и оттуда попадают в 
SiteConfig.source/SiteConfig.title_suffix, которые уже использует GenericParser при разборе конкретной статьи. 
Если не указать — source подберётся дефолтом по домену, title_suffix останется пустым (заголовок просто не будет 
обрезаться).