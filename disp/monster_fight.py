from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import PersonStatus, Inventory, Event, EventHistory, Monster
from func import update_message


@dp.callback_query_handler(Text(startswith=['monster_fight_']))
async def end_event(query: types.CallbackQuery):
    "Заканчиваем событие, сражением с монстром"

    E_ID = int(query.data.split('_')[-1])
    M_ID = int(query.data.split('_')[-2])


    EVENT = await Event.get(E_ID)
    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])
    EVENTHIS = await EventHistory.get(PERS.p_id)
    MESS = query.message.text

    MONSTER = await Monster.get(M_ID)
