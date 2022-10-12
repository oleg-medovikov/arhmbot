from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from func import get_game_status, get_look_around,\
        get_locations_nearby, make_relocation

@dp.callback_query_handler(Text(equals=['continue_game']))
async def continue_game(query: types.CallbackQuery):
    "Непосредственно игра!"
    # удаляем предыдущую клавиатуру
    await query.message.edit_reply_markup( reply_markup=None )

    """ 1. показать игроку частичный статус
        2. предложить меню с действиями, куда двигаться  """

    U_ID = query.message['chat']['id']
    MESS = get_game_status( U_ID )

    kb_game = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
            .add(InlineKeyboardButton(
                text='осмотреться', callback_data='look_around'
                ))\
            .add(InlineKeyboardButton(
                text='уйти куда-то ещё', callback_data='leave'
                ))

    await query.message.answer(MESS, reply_markup=kb_game)


@dp.callback_query_handler(Text(equals=['look_around'] ))
async def look_around(query: types.CallbackQuery):
    "персонаж осматривается на местности и тратит время"
    # удаляем предыдущую клавиатуру
    await query.message.edit_reply_markup( reply_markup=None )
    U_ID = query.message['chat']['id']

    MESS = get_look_around( U_ID )

    kb_look_around = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
            .add(InlineKeyboardButton(
                text='продолжить', callback_data='continue_game'
                ))

    await query.message.answer(MESS, reply_markup=kb_look_around )

@dp.callback_query_handler(Text(equals='leave'))
async def leave(query : types.CallbackQuery):
    "проверить список локаций по близости и предложить игроку"
    
    # удаляем предыдущую клавиатуру
    await query.message.edit_reply_markup( reply_markup=None )

    LOCATIONS = get_locations_nearby( query.message['chat']['id'] ) 

    kb_loc_nearby =  InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for loc in LOCATIONS:
        kb_loc_nearby.add(InlineKeyboardButton(
            text=loc['name_node'], callback_data='leave_' + str( loc['node_id'])
            ))
    kb_loc_nearby.add(InlineKeyboardButton(
        text='остаться на месте', callback_data='continue_game'
        ))
    
    MESS = 'Вы можете пойти:'

    await query.message.reply( MESS, reply_markup=kb_loc_nearby )

@dp.callback_query_handler(Text(startswith='leave_'))
async def relocation(query : types.CallbackQuery):
    NODE_ID = query.data.split('_')[-1]
    U_ID = query.message['chat']['id']

    make_relocation( U_ID, NODE_ID )

    kb_relocation = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
            .add(InlineKeyboardButton(
                text='идти дальше', callback_data='leave'
                ))\
            .add(InlineKeyboardButton(
                text='остановиться', callback_data='continue_game'
                ))
    await query.message.reply('Вы перешли в другое место', reply_markup=kb_relocation ) 
