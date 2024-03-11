from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from app.misc import cmd


async def set_ui_commands(bot: Bot):
    commands = [
        BotCommand(
            command=cmd.MAIN,
            description=cmd.MAIN_MENU,
        ),
        BotCommand(
            command=cmd.CANCEL,
            description=cmd.CANCEL_TXT,
        ),
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats(),
    )
