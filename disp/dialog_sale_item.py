from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text

from clas import PersonStatus, Inventory, String
from func import update_message, create_keyboard
from conf import emoji


@dp.callback_query_handler(Text(startswith=['dialog_sale_']))
async def dialog_sale_item(query: types.CallbackQuery):
    "продаем предмет в магазине"

    S_ID, D_ID, Q_ID, I_ID, COST = [int(x) for x in query.data[12:].split('_')]


