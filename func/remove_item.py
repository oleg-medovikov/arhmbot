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

    # Настало время надеть предмет на персонажа
    if ITEM.slot in equip_slots:
        CHEAK, MESS = await Inventory.equip(
            PERS.p_id,
            ITEM.i_id,
            ITEM.slot,
            ITEM.equip_mess)
        if not CHEAK:
            return MESS

    # теперь нужно применить свойства предмета
    for key, value in json.loads(ITEM.effect).items():
        STAT = await STAT.change(key, value)

    await STAT.update()

    # если предмет одноразовый, то удалить из инвентаря
    if ITEM.single_use:
        await Inventory(PERS.p_id, ITEM.i_id)
        return ITEM.equip_mess

    return MESS
