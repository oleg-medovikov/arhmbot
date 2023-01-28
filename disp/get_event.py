from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json

from clas import PersonStatus, Event, EventHistory

from func import update_message, filter_event


@dp.callback_query_handler(Text(equals=['get_event']))
async def get_event(query: types.CallbackQuery):
    "Выбираем игроку событие и предлагаем выбор как поступить"
    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])

    kb_event = InlineKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
        )

    # проверка, что персонаж не в состоянии выполнения события
    EH = await EventHistory.get(PERS.p_id)
    if EH is not None:
        EVENT = await Event.get(EH.e_id)
    else:
        try:
            EVENT = await filter_event(PERS, STAT)
        except ValueError:
            # возможно, после фильтров не осталось ивентов
            kb_event.add(InlineKeyboardButton(
                text='понимаю',
                callback_data='continue_game'
                    ))

            return await update_message(
                    query.message,
                    'Похоже, вам нечего тут делать',
                    kb_event
                        )
        else:
            # добавляем элемент в историю ивентов
            EVENTHIS = EventHistory(**{
                'gametime': STAT.gametime,
                'p_id':     PERS.p_id,
                'e_id':     EVENT.e_id, })
            await EVENTHIS.new()

    if EVENT.choice:
        LIST_ = json.loads(EVENT.check)['choice']
        for i, key in enumerate(LIST_):
            CALL = f"end_event_{'punishment' if i else 'prize'}_{EVENT.e_id}"

            kb_event.add(InlineKeyboardButton(
                text=key,
                callback_data=CALL
             ))

    else:
        kb_event.add(InlineKeyboardButton(
            text='Понимаю',
            callback_data='end_event_{EVENT.i_id}'
             ))

    return await update_message(
            query.message,
            EVENT.desription,
            kb_event
                )
