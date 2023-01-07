from .dispetcher import dp
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from func import create_user_and_person

class NewGamer(StatesGroup):
    gamename    = State()
    sex         = State()
    profession  = State()
    destination = State()


@dp.callback_query_handler(Text(equals=['register']))
async def kb_hello_callback_register(query: types.CallbackQuery):
    "Начинаем опрос анкеты для создания нового игрока"
    await query.message.edit_reply_markup(reply_markup=None)
    await NewGamer.gamename.set()
    await query.message.answer('Напишите ваше имя, желательно покороче - бумага в дефиците.')

@dp.callback_query_handler(Text(equals=['register_new']),state=NewGamer.profession)
async def kb_profession_callback_previos(query: types.CallbackQuery, state: FSMContext ):
    "Начинаем заново опрос анкеты для создания нового игрока"
    await state.finish()
    await query.message.edit_reply_markup(reply_markup=None)
    await NewGamer.gamename.set()
    await query.message.answer('Что значит, вы ошиблись? Я же просил не тратить дефицитную бумагу. Хорошо, держите ещё один бланк. Вот сюда печатными буквами Ваше имя...')

@dp.message_handler(state=NewGamer.gamename)
async def load_gamename(message: types.Message, state: FSMContext):
    "Получаем юзернейм от пользователя и спрашиваем пол"
    async with state.proxy() as data:
        data['gamename'] = message.text

    await NewGamer.next()
    MESS = "Современные законы обязывают меня спросить ваш пол. Кем вы себя идентифицируете? Помните, что мужчины сильнее, выносливее и умнее, а женщины привлекательны, ловки и менее подвержены стрессу."
    kb_sex = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
            .add(InlineKeyboardButton(text='мужчина',callback_data='male'))\
            .add(InlineKeyboardButton(text='женщина',callback_data='female'))
    await message.answer(MESS, reply_markup=kb_sex)

@dp.callback_query_handler(Text(equals=['male','female']), state=NewGamer.sex)
async def load_sex(query: types.CallbackQuery, state: FSMContext):
    "Получаем пол и спрашиваем профессию"
    await query.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        data['sex'] = query.data
    
    if query.data == 'male':
        MESS = "Должен до Вас донести, сэр, что жители нашего славного города Архэма официально победили безработицу и открыто гордятся этим! Каждый приезжий на срок более недели обязан выбрать одну из предложенных ниже вакансий и тем самым послужить на благо общества."
        kb_profession = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
            .add(InlineKeyboardButton(text='мафиози',  callback_data='мафиози'))\
            .add(InlineKeyboardButton(text='профессор',callback_data='профессор'))\
            .add(InlineKeyboardButton(text='безумец',callback_data='безумец'))\
            .add(InlineKeyboardButton(text='инквизитор',callback_data='инквизитор'))\
            .add(InlineKeyboardButton(text='назад',callback_data='register_new'))
    else:
        MESS = "Послушайте меня, мисс, жители нашего славного города Архэма официально победили безработицу и открыто гордятся этим! Каждый приезжий на срок более недели обязан выбрать одну из предложенных ниже вакансий и тем самым послужить обществу."
        kb_profession = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
            .add(InlineKeyboardButton(text='студентка',  callback_data='студентка'))\
            .add(InlineKeyboardButton(text='медсестра',callback_data='медсестра'))\
            .add(InlineKeyboardButton(text='проститутка',callback_data='проститутка'))\
            .add(InlineKeyboardButton(text='журналистка',callback_data='журналистка'))\
            .add(InlineKeyboardButton(text='назад',callback_data='register_new'))
    
    await NewGamer.next()
    await query.message.answer(MESS, reply_markup = kb_profession )

@dp.callback_query_handler(Text(equals=['мафиози', 'профессор', 'безумец', 'инквизитор', 'студентка', 'медсестра', 'проститутка','журналистка']), state=NewGamer.profession)
async def load_profession(query: types.CallbackQuery, state: FSMContext):
    "Получаем профессию и спрашиваем о цели поездки"
    await query.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        data['profession'] = query.data

    await NewGamer.next()
    MESS = 'Теперь опишите в двух словах цель приезда в Аркхем.'
    await query.message.answer(MESS)

@dp.message_handler(state=NewGamer.destination)
async def load_destination(message: types.Message, state: FSMContext):
    "Получаем цель путешествия ради шутки"
    async with state.proxy() as data:
        data['destination'] = message.text
        
        NAME_TG = ( message['from']['username'] if message['from']['username'] else ' ') \
                +' '+\
                ( message['from']['last_name']  if message['from']['last_name'] else ' ') \
                + ' ' +\
                ( message['from']['first_name'] if message['from']['first_name'] else ' ')

        create_user_and_person(
                message['from']['id'],
                NAME_TG,
                data['gamename'],
                data['sex'],
                data['profession'],
                data['destination']
                )

    await state.finish()
    MESS = 'Отлично... Дайте мне четверть часа на оформление и можете отправляться в город.'
    kb_end_reg = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
            .add(InlineKeyboardButton(text='Подождать 15 минут',  callback_data='start_new_game'))
    
    await message.answer(MESS, reply_markup= kb_end_reg ) 

