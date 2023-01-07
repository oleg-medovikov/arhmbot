from .dispetcher import dp
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text

from func import delete_message
from conf import MESS_disclaimer, MESS_hello_nologin, \
    MESS_anketa_first
from clas import User


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

    # если юзер не зарегистрирован
    # просим пройти анкету, переходим на регистрацию
    if USER is None:
        await query.message.answer(MESS_hello_nologin)
        kb_hello = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )\
            .add(InlineKeyboardButton(
                text='Пройти анкету',
                callback_data='register'
                ))\
            .add(InlineKeyboardButton(
                text='Прочесть правила',
                callback_data='manual'))
        return await query.message.answer(
            MESS_anketa_first,
            reply_markup=kb_hello
                )
    # если юзер зарегистрирован
    return await query.message.answer(
        'Я тебя знаю! :)'
            )

