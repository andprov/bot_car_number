# auto bot
[![License MIT](https://img.shields.io/badge/licence-MIT-green)](https://opensource.org/license/mit/)
[![Code style black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![Python versions](https://img.shields.io/badge/python-3.11-blue)](#)
[![Telegram API](https://img.shields.io/badge/Telegram%20Bot%20API-6.9-blue?logo=telegram)](https://core.telegram.org/bots/api)
[![Aiogram version](https://img.shields.io/badge/Aiogram-3.1.1-blue)](https://aiogram.dev/)
[![Main auto_bot workflow](https://github.com/andprov/auto_bot/actions/workflows/main.yml/badge.svg)](https://github.com/andprov/auto_bot/actions/workflows/main.yml)


# Описание
Телеграм бот для сохранения и поиска контактных данных автовладельцев-участников 
группы.

Перед запуском, бот должен быть добавлен в группу и иметь права администратора для проверки 
является ли пользователь ее участником. 

ID группы необходимо указать в переменной окружения `GROUP_ID` в `.env` файле. 
Бот поддерживает только личную переписку с пользователем, обращения в группах 
отключены в `PrivateMiddleware`.


![Pic](https://github.com/andprov/auto_bot/blob/main/img/pic.png?raw=true "Pic")


# Установка
[Создать бота и получить](https://core.telegram.org/bots#how-do-i-create-a-bot) `BOT_TOKEN`

Возможно два сценария установки локально и в [Docker](https://docs.docker.com/engine/install/).

## Локальная установка
Для локальной установки необходимо наличие [PostgreSQL](https://www.postgresql.org/download/) 
в системе.

Клонировать репозиторий:
```shell
git clone <https or SSH URL>
```

Перейти в каталог проекта:
```shell
cd auto_bot
```

Создать файл `.env` с переменными окружения, со следующим содержанием:
```shell
# MODE
DEBUG=True

# BOT
BOT_TOKEN=<bot_token>
GROUP_ID=<group_id>

# DB
DB_TYPE=postgresql
DB_CONNECTOR=psycopg
DB_HOST=db
DB_PORT=5432
POSTGRES_DB=bot
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# REDIS
REDIS_HOST=redis
REDIS_PORT=6379
```

Создать базу данных PostgreSQL с именем `bot`.

```shell
createdb -U postgres -h localhost -p 5432 bot
```

Создать и активировать виртуальное окружение:
```shell
python3 -m venv .venv
source .venv/bin/activate
```

Обновить pip:
```shell
pip install --upgrade pip
```

Установить зависимости:
```shell
pip install -r requirements.txt
```

Выполнить миграции:
```shell
alembic upgrade head
```

Запустить приложение:
```shell
python -m app
```

## Установка в Docker на удаленный сервер
Дальнейшая инструкция предполагает, что удаленный сервер настроен на работу 
по SSH. На сервере установлен Docker.

Отредактировать файл `.env` с переменными окружения:
```shell
# MODE
DEBUG=False

# BOT
BOT_TOKEN=<bot_token>
GROUP_ID=<group_id>

# DB
DB_TYPE=postgresql
DB_CONNECTOR=psycopg
DB_HOST=db
DB_PORT=5432
POSTGRES_DB=bot
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# REDIS
REDIS_HOST=redis
REDIS_PORT=6379

# Docker images
DB_IMAGE=postgres:14
REDIS_IMAGE=redis:7
BOT_IMAGE=ghcr.io/andprov/auto_bot:latest
```

Скопировать на удаленный сервер файлы `.env` `docker-compose.production.yml`
Выполнить на сервере сборку и запуск:
```shell
sudo docker compose -f docker-compose.prod.yml up -d
```
