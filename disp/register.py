import json
from .dispetcher import dp
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from func import using_item
from clas import User, Person, PersonDefaults, Item, Inventory, PersonStatus
from conf import MESS_ask_name, MESS_anketa_repeat, MESS_ask_sex, \
    MESS_ask_profession_male, MESS_ask_profession_female, \
    MESS_ask_destination, MESS_anketa_end


class NewGamer(StatesGroup):
    gamename = State()
    sex = State()
    profession = State()
    destination = State()


@dp.callback_query_handler(Text(equals=['register']))
async def hello_callback_register(query: types.CallbackQuery):
    "Начинаем опрос анкеты для создания нового игрока"
    await query.message.edit_reply_markup(reply_markup=None)
    await NewGamer.gamename.set()
    await query.message.answer(MESS_ask_name)


@dp.callback_query_handler(
        Text(equals=['register_new']),
        state=NewGamer.profession
        )
async def profession_callback_previos(
        query: types.CallbackQuery,
        state: FSMContext
        ):
    "Начинаем заново опрос анкеты для создания нового игрока"
    await state.finish()
    await query.message.edit_reply_markup(reply_markup=None)
    await NewGamer.gamename.set()
    await query.message.answer(MESS_anketa_repeat)


@dp.message_handler(state=NewGamer.gamename)
async def load_gamename_register(message: types.Message, state: FSMContext):
    "Получаем юзернейм от пользователя и спрашиваем пол"
    async with state.proxy() as data:
        data['gamename'] = message.text

    await NewGamer.next()
    kb_sex = InlineKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
        )\
        .add(InlineKeyboardButton(text='мужчина', callback_data='male'))\
        .add(InlineKeyboardButton(text='женщина', callback_data='female'))
    await message.answer(MESS_ask_sex, reply_markup=kb_sex)


@dp.callback_query_handler(Text(equals=['male', 'female']), state=NewGamer.sex)
async def load_sex_register(query: types.CallbackQuery, state: FSMContext):
    "Получаем пол и спрашиваем профессию"
    await query.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        data['sex'] = query.data

    if query.data == 'male':
        MESS = MESS_ask_profession_male
        DICT = {
            'мафиози':    'мафиози',
            'профессор':  'профессор',
            'безумец':    'безумец',
            'инквизитор': 'инквизитор',
            'назад':      'register_new',
            }
    else:
        MESS = MESS_ask_profession_female
        DICT = {
            'студентка':   'студентка',
            'медсестра':   'медсестра',
            'проститутка': 'проститутка',
            'журналистка': 'журналистка',
            'назад':       'register_new',
            }

    kb_prof = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )

    for key, value in DICT.items():
        kb_prof.add(InlineKeyboardButton(text=key, callback_data=value))

    await NewGamer.next()
    await query.message.answer(MESS, reply_markup=kb_prof)


@dp.callback_query_handler(
    Text(equals=[
        'мафиози', 'профессор', 'безумец', 'инквизитор',
        'студентка', 'медсестра', 'проститутка', 'журналистка'
        ]),
    state=NewGamer.profession
    )
async def load_profession_register(
    query: types.CallbackQuery,
    state: FSMContext
        ):
    "Получаем профессию и спрашиваем о цели поездки"
    await query.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        data['profession'] = query.data

    await NewGamer.next()
    await query.message.answer(MESS_ask_destination)


@dp.message_handler(state=NewGamer.destination)
async def load_destination_register(message: types.Message, state: FSMContext):
    "Получаем цель путешествия ради шутки"
    async with state.proxy() as data:
        data['destination'] = message.text

        TG_USER = message['from']

        LIST = (
            TG_USER.username, ' ',
            TG_USER.last_name, ' ',
            TG_USER.first_name,
            )
        NAME_TG = ''.join(str(x) for x in LIST)
        NAME_TG = NAME_TG.strip()

        USER = await User.create(
            TG_ID=TG_USER.id,
            USERNAME=TG_USER.username,
            NAME_TG=NAME_TG,
                )

        PERS = await Person.create(
            U_ID=USER.u_id,
            GAMENAME=data['gamename'],
            SEX=True if data['sex'] == 'male' else False,
            PROFESSION=data['profession'],
            DESTINATION=data['destination'],
                )
        await state.finish()

    # Теперь нужно заполнить инвентарь персонажа

    PERSDEF = await PersonDefaults.get(PERS.profession)
    STAT = await PersonStatus.get(PERS)

    for I_ID in json.loads(PERSDEF.start_list_items):
        await using_item(PERS, STAT, I_ID, True)

    kb_end_reg = InlineKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
        ).add(InlineKeyboardButton(
            text='Подождать 15 минут',
            callback_data='start_new_game'
                ))

    await message.answer(MESS_anketa_end, reply_markup=kb_end_reg)
