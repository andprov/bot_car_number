from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from app.misc.cmd import Button as btn
from app.misc.cmd import Command as cmd


async def set_ui_commands(bot: Bot):
    commands = [
        BotCommand(
            command=cmd.MAIN,
            description=btn.MAIN_MENU_TXT,
        ),
        BotCommand(
            command=cmd.CANCEL,
            description=btn.CANCEL_TXT,
        ),
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats(),
    )
