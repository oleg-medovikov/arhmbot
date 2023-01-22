from .dispetcher import dp
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text

from func import delete_message, person_status_card
from conf import MESS_disclaimer, MESS_hello_nologin, \
    MESS_anketa_first, MESS_hello_login
from clas import User, Person, PersonStatus


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    "только показываем дисклеймер и просим согласиться с жестокостью"
    await delete_message(message)

    kb_agreement = InlineKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
            ).add(InlineKeyboardButton(
                text='Согласиться',
                callback_data='start_new_game'
                    ))
    await message.answer(MESS_disclaimer, reply_markup=kb_agreement)


@dp.callback_query_handler(Text(equals=['start_new_game']))
async def start_game(query: types.CallbackQuery):
    "стартуем игру"
    # удаляем клавиатуру
    await query.message.edit_reply_markup(reply_markup=None)

    # проверяем зарегистрирован ли пользователь
    USER = await User.get(query.message['chat']['id'])
    # проверяем наличие живого персонажа
    if USER is not None:
        PERSON = await Person.get(USER.u_id)

    # если юзер не зарегистрирован
    # просим пройти анкету, переходим на регистрацию
    if USER is None or PERSON is None:
        if USER is None:
            MESS = MESS_hello_nologin
        else:
            MESS = MESS_hello_login

        kb_hello = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )

        DICT = {
            'Пройти анкету':    'register',
            'Прочесть правила': 'manual',
                }
        for key, value in DICT.items():
            kb_hello.add(InlineKeyboardButton(
                text=key,
                callback_data=value
                ))
        return await query.message.answer(
            MESS,
            reply_markup=kb_hello
            )

    """
    если юзер зарегистрирован и есть живой персонаж
    предлагаем продолжить игру дальше,
    выводим карточку персонажа
    """

    kb_game = InlineKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
        )

    DICT = {
        'Продолжить игру':  'continue_game',
        'Прочесть правила': 'manual',
        }

    for key, value in DICT.items():
        kb_game.add(InlineKeyboardButton(
            text=key,
            callback_data=value
            ))
    STAT = await PersonStatus.get(PERSON)
    return await query.message.answer(
        person_status_card(PERSON, STAT),
        parse_mode='Markdown',
        reply_markup=kb_game
        )
