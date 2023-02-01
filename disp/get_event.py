from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
    try:
        EH = await EventHistory.get(PERS.p_id)
    except ValueError:
        # пробуем найти событие для персонажа на этой локации
        try:
            EVENT = await filter_event(PERS, STAT)
        except ValueError:
            # возможно, после фильтров не осталось событий
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
        EVENT = await Event.get(EH.e_id)

    # добавляем элемент в историю ивентов
    EVENTHIS = EventHistory(**{
        'gametime': STAT.gametime,
        'p_id':     PERS.p_id,
        'e_id':     EVENT.e_id, })
    await EVENTHIS.new()

    if EVENT.choice:
        for i, key in enumerate(EVENT.get_choice()):
            if 'monster' in EVENT.get_check().keys():
                choice = 'hide' if i else 'attack'
                CALL = f"monster_fight_{choice}_{EVENT.e_id}"
            else:
                choice = 'punishment' if i else 'prize'
                CALL = f"end_event_{choice}_{EVENT.e_id}"

            kb_event.add(InlineKeyboardButton(
                text=key,
                callback_data=CALL
             ))

    else:
        kb_event.add(InlineKeyboardButton(
            text='Понимаю',
            callback_data=f'end_event_{EVENT.e_id}'
             ))

    return await update_message(
            query.message,
            EVENT.description,
            kb_event
                )
