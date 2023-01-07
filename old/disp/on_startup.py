from func import set_default_commands
from .dispetcher import dp
import asyncio 

async def on_startup(dp):
    await set_default_commands(dp)
    await dp.start_polling()
