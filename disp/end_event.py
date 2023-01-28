from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import PersonStatus, Inventory, Event
from func import update_message


@dp.callback_query_handler(Text(startswith=['end_event_']))
async def end_event(query: types.CallbackQuery):
    "Заканчиваем событие, кидаем кости"

    E_ID = int(query.data.split('_')[-1])

    EVENT = await Event.get(E_ID)
    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])

    # нужно узнать прошел ли персонаж проверку или что он выбрал
    # JSON - список изменений статуса персонажа

    MESS = ""
    DICT_CHECK = {
        'speed':     'на скорость',
        'stealth':   'на незаметность',
        'strength':  'на силу',
        'knowledge': 'на осведомлённость в данном вопросе',
        'godliness': 'на Вашу веру в высшие силы',
        'luck':      'на удачу',
            }

    if EVENT.choice:
        if choice:
            JSON = json.loads(EVENT.prize)
            MESS += "Вы выбрали " + json.loads(EVENT.check)['choice'][0]
            EVENTHIS.result = True
        else:
            JSON = json.loads(EVENT.punishment)
            MESS += "Вы выбрали " + json.loads(EVENT.check)['choice'][1]
            EVENTHIS.result = False
    else:
        for key, value in json.loads(EVENT.check).items():
            if key in ('speed', 'stealth', 'strength',
                       'knowledge', 'godliness', 'luck'):

                # количество бросков кубиком
                COUNT = PERSTAT.dict().get(key) - value
                if COUNT < 1:
                    MESS += f"Вам не удалось пройти проверку {DICT_CHECK.get(key)}"
                    EVENTHIS.result = False
                    JSON = json.loads( EVENT.punishment )
                else:
                    MESS += f"Вы пробуете пройти проверку {DICT_CHECK.get(key)}\n"
                    MESS += f"Количество бросков кубика: {COUNT}\n"
                    NUMBERS = ""
                    for _ in range(COUNT):
                        NUMBERS += f" {random.randint(1,6)} "

                    # проверяем что выпало с учётом благословения или проклятья
                    checklist = { '5', '6' }
                    if PERSTAT.bless > 0:
                        "Благословение"
                        checklist = { '4', '5', '6' }
                    elif PERSTAT.bless < 0:
                        "Проклят"
                        checklist = { '6' }

                    TEST = set(NUMBERS.split()) & checklist
                    MESS += NUMBERS + '\n'

                    if len(TEST):
                        MESS += "Вы прошли проверку!\n"
                        EVENTHIS.result = True
                        JSON = json.loads( EVENT.prize )
                    else:
                        MESS += "Проверка провалилась!\n"
                        EVENTHIS.result = False
                        JSON = json.loads( EVENT.punishment )

    if EVENTHIS.result:
        MESS += '\n\n' + EVENT.mess_prize
    else:
        MESS += '\n\n' + EVENT.mess_punishment

    # Применяем эффекты
    for key, value in JSON.items():
        if key in ('speed', 'stealth', 'strength', 'knowledge',
                   'godliness', 'luck', 'experience', 'bless', 'proof',
                   'hunger', 'weary', 'money', 'health', 'mind',
                   'location', 'death'):
            PERSTAT = await PERSTAT.change(key, value)
        elif key == 'time':
            await PERSTAT.waste_time(int(value))
        elif key == 'item':
            INV = Inventory(**{
                'p_id': PERSON.p_id,
                'slot': 'bag',
                'i_id': int(value)
                })
            CHECK_EQUIP, MESS_EQUIP = await INV.add()
            if not CHECK_EQUIP:
                MESS += '\n\n' + MESS_EQUIP

    MESS = f'```\n {MESS} \n```'

    # заканчиваем прохождение ивента
    await EVENTHIS.write_result()

    return {'error': False, 'MESS': MESS}
