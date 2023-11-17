![CI](https://github.com/brivazz/leadHit_tz/actions/workflows/tests.yml/badge.svg)
![CI](https://github.com/brivazz/leadHit_tz/actions/workflows/code-checker.yml/badge.svg)

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/brivazz/leadHit_tz/code-checker.yml)![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/brivazz/leadHit_tz)![GitHub language count](https://img.shields.io/github/languages/count/brivazz/leadHit_tz)![GitHub top language](https://img.shields.io/github/languages/top/brivazz/leadHit_tz)![Github Repository Size](https://img.shields.io/github/repo-size/brivazz/leadHit_tz)

# Web-приложение для определения заполненных форм

### Задание

В базе данных хранится список шаблонов форм.

- Шаблон формы, это структура, которая задается уникальным набором полей, суказанием их типов.
Пример шаблона формы:
        `{"name": "Form template name", "field_name_1": "email", "field_name_2: "phone"}`

Всего должно поддерживаться четыре типа данных полей:

- email
- телефон
- дата
- текст

Все типы кроме текста должны поддерживать валидацию:

- Телефон передается в стандартном формате `+7 xxx xxx xx xx`
- Дата передается в формате `DD.MM.YYYY или YYYY-MM-DD`

Имя шаблона формы задается в свободной форме, например `MyForm` или `Order Form`.

Имена полей также задаются в свободной форме (желательно осмысленно), например `user_name`, `order_date` или `lead_email`.

На вход по урлу **`/get_form`** POST запросом передаются данные такого вида:
`f_name1=value1&f_name2=value2`

В ответ нужно вернуть имя шаблона формы, если она была найдена.

Чтобы найти подходящий шаблон нужно выбрать тот, поля которого совпали с полями
в присланной форме. Совпадающими считаются поля, у которых совпали имя и тип
значения. Полей в пришедшей форме может быть больше чем в шаблоне, в этом случае шаблон все равно будет считаться подходящим

 Самое главное, чтобы все поля шаблона присутствовали в форме.

Если подходящей формы не нашлось, вернуть ответ в следующем формате:
`{f_name1: FIELD_TYPE, f_name2: FIELD_TYPE}`

- где FIELD_TYPE это тип поля, выбранный на основе правил валидации, проверка
правил должна производиться в следующем порядке `дата`, `телефон`, `email`, `текст`.

В качестве базы данных рекомендуем использовать `MongoDB`, вместе с исходниками
задания должен поставляться файл с тестовой базой, содержащей шаблоны форм
если сможете поднять и использовать контейнер Docker с MongoDB - это будет
отличное решение, однако оно может отнять у вас много времени и не является
обязательным.

Также в комплекте должен быть скрипт, который совершает тестовые запросы. Если
окружение приложения подразумевает что-то выходящее за рамки virtualenv, то все
должно быть упаковано в Docker контейнеры или таким способом, чтобы не
приходилось ставить дополнительные пакеты и утилиты на машине. Все необходимые
действия для настройки и запуска приложения должны находится в файле README.
Версия Python остается на ваш выбор. Мы рекомендуем использовать версию 3.6 и
выше.

Входные данные для веб-приложения:

- Список полей со значениями в теле POST запроса.

Выходные данные:

- Имя наиболее подходящей данному списку полей формы, при отсутствии совпадений
с известными формами произвести типизацию полей на лету и вернуть список полей с
их типами.

***

### Используемые технологии сервиса

Технологический стек проекта:

> 1. Nginx — веб-сервер;
> 2. MongoDB - документоориентированная БД
> 3. FastAPI — веб-фреймворк для создания веб-приложений
> 4. GitHub Actions для реализации CI

Сервис запускается с помощью Docker контейнеров, тем самым реализуя в проекте микросервисную архитектуру. Сервисы связаны между собой с помощью docker compose.

У API есть версионирование.

### Подготовка к запуску "Web-приложение для определения заполненных форм"

1. Для работы сервиса у Вас должен быть установлен [Python](https://www.python.org/) на локальной машине и [Docker](https://www.docker.com/)

2. В корневой директории проекта создайте файл `.env` и скопируйте в него содержимое файла `.env.example` или переименуйте последний в .env

3. Находясь в корневой директории проекта в терминале введите команду `python3 -m venv venv`, тем самым будет создано виртуальное окружение для установки и изоляции необходимых для проекта зависимостей

4. Активируйте созданное на предыдущем этапе вируальное окружение командой `source venv/bin/activate`

5. [Опционально] команда `make env` установит необходимые зависимости для профилирования кода, указанные в файле `requirements.txt`

# Запуск

В проекте предусмотрен Makefile для удобства запуска проекта.

Для запуска проекта достаточно:

1. Команда `make start` запустит docker-compose и сервис будет доступен для запросов по адресу: <http://127.0.0.1:80/api/v1/get_form>
   - Веб-сервер Nignx будет проксировать запросы на 8000 порт приложения. Приложение также доступно на этом порту.
   - желательно использовать для запросов программу [Postman](https://www.postman.com/) который умеет отправлять POST запросы, необходимые для правильной работы сервиса, но не обязательно(смотри пункт ниже)
   - Документация (OpenAPI) проекта доступна по адресу <http://127.0.0.1:8000/api/v1/openapi> с помощью которой есть возможность вручную ввести данные на вход приложению.
   - Данные на вход приложению в формате JSON:
        `{"date": "", "phone": "", "email": "", "text": ""}`

   - Также для удобства просмотра коллекций с данными, хранящимися в базе данных MongoDB, в проекте присутствует интерактивный и легковесный веб-инструмент для эффективного управления базами данных MongoDB, который доступен по адресу <http://127.0.0.1:8081>

# Остановка

Команда `make stop` остановит и удалит все контейнеры, вместе со всеми созданными файлами(volumes).

***

### Тестирование

1. Команда `make test` запустит сборку тестовых контейнеров в рамках docker-compose и в случае успешного завершения тестов, контейнер с тестами завершит работу и самостоятельно остановится, о чем и будет выведена информация в окне терминала

2. Для остановки всех тестовых контейнеров команда `make test-stop`

***
