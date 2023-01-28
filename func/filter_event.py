import json
import random
from clas import Event, Person, PersonStatus, EventHistory, Inventory


async def filter_event(PERS: 'Person', STAT: 'PersonStatus') -> 'Event':
    "отбираем события доступные персонажу"
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

    if len(EVENTS) == 0:
        raise ValueError('Нет событий!')
    else:
        return random.choice(EVENTS)
