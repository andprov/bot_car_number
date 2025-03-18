# bot_car_number

[![License MIT](https://img.shields.io/badge/licence-MIT-green)](https://opensource.org/license/mit/)
[![Code style black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![Python versions](https://img.shields.io/badge/python-3.11-blue)](#)
[![Telegram API](https://img.shields.io/badge/Telegram%20Bot%20API-6.9-blue?logo=telegram)](https://core.telegram.org/bots/api)
[![Aiogram version](https://img.shields.io/badge/Aiogram-3.1.1-blue)](https://aiogram.dev/)
[![Main bot_car_number workflow](https://github.com/andprov/bot_car_number/actions/workflows/main.yml/badge.svg)](https://github.com/andprov/bot_car_number/actions/workflows/main.yml)

# Description

A Telegram bot for saving and searching contact information of car owners

![Pic](https://github.com/andprov/bot_car_number/blob/main/img/pic.png?raw=true "Pic")

# Quickstart

1. [Create a bot and get a token](https://core.telegram.org/bots#how-do-i-create-a-bot) `BOT_TOKEN`

2. Clone the repository:

```shell
git clone <https or SSH URL>
```

3. In the project root, create a `.env` file. Example: [.env.example](.env.example)

4. Create a PostgreSQL database with the name `bot_car_number`.

```shell
createdb -U postgres -h localhost -p 5432 bot_car_number
```

5. Create and activate a virtual environment:

```shell
python3.11 -m venv .venv
source .venv/bin/activate
```

6. Install dependencies:

```shell
pip install -e .
```

7. Export environment variables:

```shell
export $(grep -v '^#' .env | xargs)
```

8. Run migrations:

```shell
alembic upgrade head
```

9. Run the app:

```shell
python -m bot_car_number
```
