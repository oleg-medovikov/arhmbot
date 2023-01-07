from aiogram.types import BotCommand


async def set_default_commands(dp):
    "команды для синенького меню"
    commands = [
        BotCommand(
            command="start",
            description="Приветсвие"
            ),
           ]

    await dp.bot.set_my_commands(commands)
