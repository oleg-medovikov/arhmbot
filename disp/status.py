from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton

from func import person_status, get_inventory, get_item,\
        make_equip_item, make_remove_item
from conf import emoji


@dp.callback_query_handler(Text(equals=['status']))
async def person_status_main(query: types.CallbackQuery):
    # удаляем предыдущую клавиатуру
    await query.message.edit_reply_markup( reply_markup=None )

    U_ID = query.message['chat']['id']
    MESS = person_status(U_ID)

    kb_status = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
            .add(InlineKeyboardButton(
                text='инвентарь', callback_data='inventory'
                ))\
            .add(InlineKeyboardButton(
                text='назад', callback_data='continue_game'
                ))
    return await query.message.answer(MESS, reply_markup=kb_status, parse_mode='Markdown')
 
@dp.callback_query_handler(Text(equals=['inventory']))
async def see_inventory(query: types.CallbackQuery):
    # 
    await query.message.edit_reply_markup( reply_markup=None )

    U_ID = query.message['chat']['id']
    MESS, INV = get_inventory( U_ID )

    for key, value in emoji.items():
        if key in MESS:
            MESS = MESS.replace(key, value)

    kb_bag = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for item in INV:
        if item['slot'] == 'bag':
            kb_bag.add(InlineKeyboardButton(
                text = str( emoji.get( item['emoji'] ) ) + ' ' + item['name'], callback_data='bag_item_' + str(item['i_id'] )
                ))
        else:
            kb_bag.add(InlineKeyboardButton(
                text = str( emoji.get( item['emoji'] ) ) + ' ' + item['name'], callback_data='item_' + str(item['i_id'] )
                ))


    kb_bag.add(InlineKeyboardButton(
        text = 'назад', callback_data='status'
        ))

    return await query.message.answer(MESS, reply_markup=kb_bag, parse_mode='Markdown' )


@dp.callback_query_handler(Text(startswith=['bag_item_']))
async def see_bag_item(query: types.CallbackQuery ):
    await query.message.edit_reply_markup( reply_markup=None )

    I_ID = query.data.split('_')[-1]
    U_ID = query.message['chat']['id']

    ITEM = get_item( U_ID, I_ID )

    kb_item = InlineKeyboardMarkup( resize_keybord = True, one_time_keyboard = True)
    kb_item.add(InlineKeyboardButton(
        text = str ('Использовать'), callback_data = 'equip_' + str(ITEM['i_id'])
        ))\
        .add(InlineKeyboardButton(
        text = str ('Выбросить'), callback_data = 'drop_' + str(ITEM['i_id'])
        ))\
        .add(InlineKeyboardButton(
        text = str ('Назад'), callback_data = 'inventory'
        ))
    return await query.message.answer(ITEM['description'], reply_markup = kb_item, parse_mode = 'Markdown')

@dp.callback_query_handler(Text(startswith=['item_']))
async def see_item(query: types.CallbackQuery ):
    await query.message.edit_reply_markup( reply_markup=None )

    I_ID = query.data.split('_')[-1]
    U_ID = query.message['chat']['id']

    ITEM = get_item( U_ID, I_ID )

    kb_item = InlineKeyboardMarkup( resize_keybord = True, one_time_keyboard = True)
    kb_item.add(InlineKeyboardButton(
        text = str ('Снять'), callback_data = 'remove_' + str(ITEM['i_id'])
        ))\
        .add(InlineKeyboardButton(
        text = str ('Выбросить'), callback_data = 'drop_' + str(ITEM['i_id'])
        ))\
        .add(InlineKeyboardButton(
        text = str ('Назад'), callback_data = 'inventory'
        ))
    return await query.message.answer(ITEM['description'], reply_markup = kb_item, parse_mode = 'Markdown')



@dp.callback_query_handler(Text(startswith=['equip_']))
async def equip_item(query: types.CallbackQuery):
    await query.message.edit_reply_markup( reply_markup=None )

    I_ID = query.data.split('_')[-1]
    U_ID = query.message['chat']['id']

    check, MESS = make_equip_item( U_ID, I_ID )

    kb_equip = InlineKeyboardMarkup( resize_keybord = True, one_time_keyboard = True)\
            .add(InlineKeyboardButton(
                text = 'Понятно', callback_data = 'inventory'
                ))
    
    return await query.message.answer(MESS, reply_markup=kb_equip, parse_mode='Markdown'  )


@dp.callback_query_handler(Text(startswith=['remove_']))
async def remove_item(query: types.CallbackQuery):
    await query.message.edit_reply_markup( reply_markup=None )

    I_ID = query.data.split('_')[-1]
    U_ID = query.message['chat']['id']

    check, MESS = make_remove_item( U_ID, I_ID )

    kb_equip = InlineKeyboardMarkup( resize_keybord = True, one_time_keyboard = True)\
            .add(InlineKeyboardButton(
                text = 'Понятно', callback_data = 'inventory'
                ))
    
    return await query.message.answer(MESS, reply_markup=kb_equip, parse_mode='Markdown'  )


