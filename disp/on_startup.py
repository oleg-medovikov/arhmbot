from func import set_default_commands
from base import ARHM_DB


async def on_startup(dp):
    # запустим подключение к базе
    await ARHM_DB.connect()
    # это команды меню в телеграм боте
    await set_default_commands(dp)
