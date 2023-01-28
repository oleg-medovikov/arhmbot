from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import random

from clas import PersonStatus, Event, EventHistory, Inventory

from func import update_message
from conf import emoji


@dp.callAback_query_handler(Text(equals=['get_event']))
async def get_event(query: types.CallbackQuery):
    "показываем игроку инвентарь персонажа"
    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])

    kb_event = InlineKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
        )

    # проверка, что персонаж не в состоянии выполнения события
    EH = await EventHistory.get(PERS.p_id)
    if EH is not None:
        kb_event.add(InlineKeyboardButton(
             text='понимаю',
             callback_data=f'end_event_{EH.e_id}'
             ))

        return await update_message(
            query.message,
            'У вас незаконченное событие!',
            kb_event
                )

    # выбираем доступные события для этой локации
    EVENTS = await Event.location(
                    STAT.location,
                    STAT.stage,
                    PERS.profession,
                    PERS.p_id
                    )

    EVENT_FILTER = []
    # получаем список событий, которые персонаж уже проходил
    EVENT_DONE = await EventHistory.get_list(PERS.p_id)

    for EVENT in EVENTS:
        # если событие одноразовые и уже было, то исключаем
        if EVENT['single'] is True:
            if EVENT['e_id'] in list(EVENT_DONE):
                EVENT_FILTER.append(EVENT)
                continue
        # проверяем событие подходит ли оно по статам
        for key, value in json.loads(EVENT['demand']).items():
            if key in ('sex', 'profession'):
                # Это проверка персоны
                if PERS.dict()[key] != value:
                    EVENT_FILTER.append(EVENT)
                    break

            if key in ('money', 'health', 'mind', 'speed',
                       'stealth', 'strength', 'knowledge',
                       'godliness', 'luck', 'hunger', 'weary'):
                # так сложно потому что есть отрицательная скрытность!
                if abs(STAT.dict()[key]) < abs(value) \
                        and STAT.dict()[key]*value > 0:
                    EVENT_FILTER.append(EVENT)
                    break

            if key == 'item':
                if not await Inventory.check_item(PERS.p_id, value):
                    EVENT_FILTER.append(EVENT)
                    break

    # удаляем из списка ивентов те, что попали в фильтр
    for EVENT in EVENT_FILTER:
        EVENTS.remove(EVENT)

    # возможно, после фильтров не осталось ивентов
    if len(EVENTS) == 0:
        # если список пустой, то возвращаем сообщение
        kb_event.add(InlineKeyboardButton(
             text='понимаю',
             callback_data=f'end_event_{EH.e_id}'
             ))

        return await update_message(
            query.message,
            'Похоже, вам нечего тут делать',
            kb_event
                )

    # наконец-то выбираем ивент из оставшегося, случайным образом
    EVENT = random.choice(EVENTS)

    # добавляем элемент в историю ивентов
    EVENTHIS = EventHistory(**{
        'gametime': STAT.gametime,
        'p_id':     PERS.p_id,
        'e_id':     EVENT['e_id'], })
    await EVENTHIS.new()

    if EVENT.choice:
        LIST_ = json.loads(EVENT.check)['choice']
        for index, key in enumerate(LIST_):
            CALL = f"end_event_{'punishment' if index else 'prize'}_{EH.e_id}"

            kb_event.add(InlineKeyboardButton(
                text=key,
                callback_data=CALL
             ))

        return await update_message(
            query.message,
            EVENT.desription,
            kb_event
                )
