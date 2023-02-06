from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from random import choice

from clas import Person, PersonStatus, Event, EventHistory

from func import update_message, demand


async def filter_event(PERS: 'Person', STAT: 'PersonStatus') -> 'Event':
    "отбираем события доступные персонажу"
    EVENTS = await Event.location(
        STAT.location,
        STAT.stage,
        PERS.profession
            )
    EVENT_FILTER = []
    # получаем список событий, которые персонаж уже проходил
    EVENT_DONE = await EventHistory.get_list(PERS.p_id)

    for EVENT in EVENTS:
        # если событие одноразовые и уже было, то исключаем
        if EVENT.single and EVENT.e_id in list(EVENT_DONE):
            EVENT_FILTER.append(EVENT)
            continue
        # проверяем событие подходит ли оно по требованиям
        if not await demand(PERS, STAT, EVENT.get_demand()):
            EVENT_FILTER.append(EVENT)

    # удаляем из списка ивентов те, что попали в фильтр
    for EVENT in EVENT_FILTER:
        EVENTS.remove(EVENT)

    if len(EVENTS) == 0:
        raise ValueError('Нет событий!')
    else:
        return choice(EVENTS)


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
                choice = 'attack' if i else 'hide'
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
