from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text

from clas import PersonStatus, Event, EventHistory
from func import update_message, timedelta_to_str, applying_effects, \
    create_keyboard
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
    TIME_START = STAT.gametime

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

    # Применяем эффекты, награждаем или наказываем
    MESS += await applying_effects(
        PERS,
        STAT,
        EVENT.get_prize() if EVENTHIS.result else EVENT.get_punishment()
            )
    # считаем сколько потратили времени
    STAT = await PersonStatus.get(PERS)
    WASTE = STAT.gametime - TIME_START
    MESS = emoji('stopwatch') + ' ' + timedelta_to_str(WASTE) \
        + '\n\n' + MESS

    # заканчиваем прохождение ивента
    await EVENTHIS.write_result()
    DICT = {'закончить событие': 'continue_game'}

    return await update_message(
            query.message,
            MESS,
            create_keyboard(DICT)
            )
