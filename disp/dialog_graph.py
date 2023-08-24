from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from pandas import DataFrame

from clas import User, Dialog
from func import create_keyboard


@dp.message_handler(Text(startswith=['dialog_graph_']))
async def dialog_graph(message: types.Message):
    """показать админу граф конкретного диалога"""
    try:
        D_ID = int(message['text'].split('_')[-1])
    except ValueError:
        return await message.answer('неправильный номер диалога')

    USER = await User.get(message['from']['id'])
    if USER is None or not USER.admin:
        return await message.answer('Эта функция только для админов')

    df = DataFrame(data=await Dialog.get_dialog(D_ID))
    if len(df) == 0:
        return await message.answer(
            f'не существует диалога с номером {D_ID}'
            )

    df = df[['q_id', 'name', 'description', 'answers', 'transfer']]
    df['transfer_'] = df['transfer'].apply(lambda x: max(x))
    df = df.sort_values(by='transfer_')

    list_ = []
    for node in df.to_dict('records'):
        for key in node['transfer']:
            list_.append([node['q_id'], key])

    options = {
        "font_size": 36,
        "node_size": 3000,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 5,
        "width": 5,
    }

    G = nx.DiGraph(list_)

    # выставляю позицию первого узла
    pos = {1: (0, 1 + 0.5)}
    nodes = set([1, -1])
    level = 2

    # расставляю следующие узлы
    for row in df.to_dict('records'):
        bounds = row['transfer']
        new_level = []
        for i in bounds:
            if i not in nodes:
                nodes.add(i)
                new_level.append(i)

        if len(new_level) > 0:
            pos.update({n: (level, i + 0.5) for i, n in enumerate(new_level)})
            level += 1 

    # добавляю узел выхода -1
    pos.update({n: (level + 2, 2) for i, n in enumerate([-1])})

    figure(figsize=(4 * level, 40), dpi=40)
    nx.draw_networkx(
        G,
        pos,
        **options
    )

    # Set margins for the axes so that nodes aren't clipped
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")

    GRAPH = f'/tmp/map_{D_ID}.png'
    plt.savefig(GRAPH)
    photo = open(GRAPH, 'rb')
    await message.delete()

    DICT = {
        'назад': 'continue_game'
    }
    MESS = 'Вы нарисовали карандашом схему своих переговоров'

    return await message.answer_photo(
        caption=MESS,
        photo=photo,
        reply_markup=create_keyboard(DICT)
    )
