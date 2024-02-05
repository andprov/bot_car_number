from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from app.utils import cmd


async def set_ui_commands(bot: Bot):
    commands = [
        BotCommand(
            command=cmd.MAIN,
            description="Главное меню",
        ),
        BotCommand(
            command=cmd.CANCEL,
            description="Отмена",
        ),
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats(),
    )
