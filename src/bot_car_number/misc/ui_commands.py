from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from bot_car_number.misc.cmd import Button as btn
from bot_car_number.misc.cmd import Command as cmd


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
