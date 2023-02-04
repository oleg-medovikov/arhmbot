from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import PersonStatus, Inventory, Event, EventHistory
from func import update_message, timedelta_to_str
from conf import emoji

DICT_CHECK = {
    'speed':     'на скорость',
    'stealth':   'на незаметность',
    'strength':  'на силу',
    'knowledge': 'на осведомлённость в данном вопросе',
    'godliness': 'на Вашу веру в высшие силы',
    'luck':      'на удачу',
        }


@dp.callback_query_handler(Text(startswith=['end_event_']))
async def end_event(query: types.CallbackQuery):
    "Заканчиваем событие, кидаем кости"

    E_ID = int(query.data.split('_')[-1])

    EVENT = await Event.get(E_ID)
    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])
    EVENTHIS = await EventHistory.get(PERS.p_id)
    MESS = query.message.text
    WASTE = 0

    # если событие подразумевает выбор, то нужно определиться, что выбрано

    if EVENT.choice:
        CHEAK = 0 if 'prize' in query.data else 1
        MESS += '\n\nВы выбрали ' + EVENT.get_choice()[CHEAK]
        EVENTHIS.result = True if 'prize' in query.data else False
    else:
        EVENTHIS.result = True

    # Если выбора нет, нужно пройти проверки и выяснить результат

    for key, value in EVENT.get_check().items():
        if key not in ('speed', 'stealth', 'strength',
                       'knowledge', 'godliness', 'luck'):
            # если затесалась ошибка в параметре - игнорируем
            print(f'в {EVENT.e_id} ivent ошибка в check!\n {key}')
            continue

        # нужно вычислить количество бросков кубиком
        COUNT = STAT.dict().get(key) - value
        RES = STAT.dice_roll(COUNT)
        MESS += f'\n\nВы проходите проверку {DICT_CHECK.get(key)}\n'
        MESS += f'всего у Вас попыток: {COUNT}' \
            + (f' из которых {RES["luck"]} благодаря удаче\n'
               if RES["luck"] else '\n')

        for num in RES['numbers']:
            MESS += f"  {num}\ufe0f\u20e3  "

        if not RES['success']:
            # если хоть одна проверка не пройдена - то результат плохой
            EVENTHIS.result = False
            MESS += f"\nВам не удалось пройти проверку {DICT_CHECK.get(key)}"
        else:
            MESS += f"\nВам удалось пройти проверку {DICT_CHECK.get(key)}!"

    MESS += '\n\n' + EVENT.mess_prize if EVENTHIS.result \
        else '\n\n' + EVENT.mess_punishment

    # словарь изменение статов персонажа
    DICT = EVENT.get_prize() if EVENTHIS.result \
        else EVENT.get_punishment()

    # Применяем эффекты
    for key, value in DICT.items():
        if key in ('speed', 'stealth', 'strength', 'knowledge',
                   'godliness', 'luck', 'experience', 'bless', 'proof',
                   'hunger', 'weary', 'money', 'health', 'mind',
                   'location', 'death'):
            STAT = await STAT.change(key, value)
        elif key == 'time':
            WASTE = await STAT.waste_time(int(value))
        elif key == 'item':
            INV = Inventory(**{
                'p_id': PERS.p_id,
                'slot': 'bag',
                'i_id': int(value)
                })
            CHECK_EQUIP, MESS_EQUIP = await INV.add()
            if not CHECK_EQUIP:
                MESS += '\n\n' + MESS_EQUIP

    MESS = emoji('stopwatch') + ' ' + timedelta_to_str(WASTE) \
        + '\n\n' + MESS

    # заканчиваем прохождение ивента
    await EVENTHIS.write_result()

    kb_event = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )

    # в любом случае предлагаем продолжить
    kb_event.add(InlineKeyboardButton(
        text='закончить событие',
        callback_data='continue_game'
                ))

    return await update_message(
            query.message,
            MESS,
            kb_event
            )
