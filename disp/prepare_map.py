from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMedia
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from json import loads

from clas import Journal, Location
from func import update_message


@dp.callback_query_handler(Text(startswith=['prepare_map_']))
async def prepare_map(query: types.CallbackQuery):
    """показать игроку основной квест"""
    P_ID = int(query.data.split('_')[-1])

    NODES = await Journal.get_relocation_map(P_ID)

    NODE_IDS = list(set([num for row in NODES for num in row]))

    NAMES = await Location.get_names(NODE_IDS)
    # формируем картинку
    figure(figsize=(20, 15), dpi=80)

    G = nx.Graph()
    G.add_edges_from(NODES)
    H = nx.relabel_nodes(G, NAMES)
    nx.draw(
        H,
        pos=nx.kamada_kawai_layout(H),
        node_color='white',
        node_size=19000,
        with_labels=True
    )
    MAP = f'/tmp/map_{P_ID}.png'
    plt.savefig(MAP)
    photo = open(MAP, 'rb')
    await query.message.delete()

    kb_prepare = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )
    kb_prepare.add(InlineKeyboardButton(
            text='назад',
            callback_data='prepare_main',
        ))

    MESS = 'Вы нарисовали карандашом схему своих путешествий по городу.'

    # await query.message.delete()
    return await query.message.answer_photo(
        caption=MESS,
        photo=photo,
        reply_markup=kb_prepare
    )
