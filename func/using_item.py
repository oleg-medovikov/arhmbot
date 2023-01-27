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
    CREATE_PERSON: bool = False
        ) -> str:
    """
    Мы должны убедиться, есть ли предмет в сумке, так как
    экипировка может происходить на этапе создания персонажа,
    в случае, если в сумке уже есть предмет, его не продублирует
    но мы не можем надеть, если сумка пуста
    """
    # получаем предмет
    ITEM = await Item.get(I_ID)
    # кладём предмет в сумку, если это создание персонажа
    if CREATE_PERSON:
        cheak, string = await Inventory.add(PERS.p_id, I_ID)
        # если предмет не нужно одевать,  вы выходим
        if ITEM.slot not in equip_slots:
            return "Предмет добавлен в сумку"

    # теперь нужно проверить статы персонажа, перед надеванием
    for key, value in json.loads(ITEM.demand).items():
        if key in ('sex', 'profession'):
            # Это проверка персоны
            if PERS.dict()[key] != value:
                return ITEM.fail_mess

            continue
        if abs(STAT.dict()[key]) < abs(value):
            return ITEM.fail_mess

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

    # если предмет одноразовый, то удалить из инвентаря
    if ITEM.single_use:
        await Inventory.drop(PERS.p_id, ITEM.i_id)
        return ITEM.equip_mess

    return MESS
