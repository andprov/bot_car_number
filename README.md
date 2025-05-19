# bot_car_number

[![Python versions](https://img.shields.io/badge/python-3.12-blue)](#)
[![License MIT](https://img.shields.io/badge/licence-MIT-green)](https://opensource.org/license/mit/)
[![Code style black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![Main bot_car_number workflow](https://github.com/andprov/bot_car_number/actions/workflows/main.yml/badge.svg)](https://github.com/andprov/bot_car_number/actions/workflows/main.yml)

# Description

A Telegram bot for saving and searching contact information of car owners

![Pic](https://github.com/andprov/bot_car_number/blob/main/img/pic.png?raw=true "Pic")

# Quickstart

## Create bot and get token

<https://core.telegram.org/bots#how-do-i-create-a-bot>

## Clone the repository

```shell
git clone <https or SSH URL>
cd <repository_name>
```

## Configure environment

Create and edit `.env` file from the [.env.example](.env.example)

```shell
cp .env.example .env
```

## Create PostgreSQL database

```shell
createdb -U postgres -h localhost -p 5432 bot_car_number
```

## Installation and run (Choose one method)

### pip

```shell
# Create and activate virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .

# Export environment variables
export $(grep -v '^#' .env | xargs)

# Run migrations
alembic upgrade head

# Run app
python -m bot_car_number
```

### uv

```shell
# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv sync

# Export environment variables
export $(grep -v '^#' .env | xargs)

# Run migrations
alembic upgrade head

# Run app
uv run python -m bot_car_number
```
