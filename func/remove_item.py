import json
from clas import Person, PersonStatus, Item, Inventory

equip_slots = [
    'head', 'onehand', 'twohands',
    'head', 'body', 'legs', 'shoes'
    ]


async def using_item(
    PERS: 'Person',
    STAT: 'PersonStatus',
    I_ID: int,
        ) -> str:
    """
    Мы должны убедиться, что в сумке достаточно места
    и изменить статы, откатив влияние предмета на персонажа
    """

    # получаем предмет
    ITEM = await Item.get(I_ID)

    # Проверяем место в сумке
    if not await Inventory.bug_free_space(PERS.p_id):
        return "Необходимо освободить место в сумке!"

    # снимаем предмет и кладем в сумку
    await Inventory.remove(STAT.p_id, ITEM.i_id)

    # теперь нужно применить свойства предмета
    for key, value in json.loads(ITEM.effect).items():
        STAT = await STAT.change(key, -value)

    return ITEM.remove_mess
