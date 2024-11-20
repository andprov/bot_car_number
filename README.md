# bot_car_number

[![License MIT](https://img.shields.io/badge/licence-MIT-green)](https://opensource.org/license/mit/)
[![Code style black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![Python versions](https://img.shields.io/badge/python-3.11-blue)](#)
[![Telegram API](https://img.shields.io/badge/Telegram%20Bot%20API-6.9-blue?logo=telegram)](https://core.telegram.org/bots/api)
[![Aiogram version](https://img.shields.io/badge/Aiogram-3.1.1-blue)](https://aiogram.dev/)
[![Main bot_car_number workflow](https://github.com/andprov/bot_car_number/actions/workflows/main.yml/badge.svg)](https://github.com/andprov/bot_car_number/actions/workflows/main.yml)

# Описание

Телеграм бот для сохранения и поиска контактных данных автовладельцев-участников
группы.

Перед запуском, бот должен быть добавлен в группу и иметь права администратора для проверки
является ли пользователь ее участником.

ID группы необходимо указать в переменной окружения `GROUP_ID` в `.env` файле.
Бот поддерживает только личную переписку с пользователем, обращения в группах
отключены в `PrivateMiddleware`.

![Pic](https://github.com/andprov/bot_car_number/blob/main/img/pic.png?raw=true "Pic")

# Установка

[Создать бота и получить](https://core.telegram.org/bots#how-do-i-create-a-bot) `BOT_TOKEN`

Клонировать репозиторий:

```shell
git clone <https or SSH URL>
```

Перейти в каталог проекта:

```shell
cd bot_car_number
```

В корне проекта создать файл `.env` пример - [.env.example](.env.example)

Создать базу данных PostgreSQL с именем `bot_car_number`.

```shell
createdb -U postgres -h localhost -p 5432 bot_car_number
```

Создать и активировать виртуальное окружение:

```shell
python3.11 -m venv .venv
source .venv/bin/activate
```

Обновить pip:

```shell
pip install --upgrade pip
```

Установить зависимости:

```shell
pip install -e .
```

Выполнить миграции:

```shell
alembic upgrade head
```

Запустить приложение:

```shell
python -m bot_car_number
```
