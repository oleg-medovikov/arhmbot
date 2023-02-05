from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sqlalchemy import select, and_

from base import ARHM_DB, t_inventory, t_items
from conf import MAX_BAG_CAPASITY
from .String import String

class Inventory(BaseModel):
    p_id:         int
    slot:         str
    i_id:         int
    date_update:  Optional[datetime] = datetime.now()

    @staticmethod
    async def check_item(P_ID, I_ID) -> bool:
        "проверяем наличие предмета у персонажа"
        query = t_inventory.select(and_(
            t_inventory.c.p_id == P_ID,
            t_inventory.c.i_id == I_ID
            ))
        res = await ARHM_DB.fetch_one(query)
        return res is not None

    @staticmethod
    async def bug_free_space(P_ID: int) -> bool:
        "Проверяем есть ли свободное место в сумке"
        query = t_inventory.select(and_(
            t_inventory.c.p_id == P_ID,
            t_inventory.c.slot == 'bag'
            ))
        res = await ARHM_DB.fetch_all(query)

        return len(res) < MAX_BAG_CAPASITY

    @staticmethod
    async def get(P_ID: int) -> list:
        "Возвращаем список всех предметов персонажа"
        j = t_inventory.join(
                t_items,
                t_inventory.c.i_id == t_items.c.i_id
                      )

        query = select([
            t_inventory.c.p_id,
            t_inventory.c.slot,
            t_inventory.c.i_id,
            t_items.c.name,
            t_items.c.emoji,
            t_inventory.c.date_update
            ]).where(t_inventory.c.p_id == P_ID)\
            .order_by(t_inventory.c.date_update)\
            .select_from(j)

        list_ = []

        for row in await ARHM_DB.fetch_all(query):
            list_.append(dict(row))

        return list_

    @staticmethod
    async def equip(
        P_ID: int,
        I_ID: int,
        SLOT: str,
        equip_mess: str
            ) -> tuple[bool, str]:
        """ Функция надевания предмета
        нужно проверить есть ли в данном слоте другой предмет
        """
        query = select([t_inventory.c.slot])\
            .where(t_inventory.c.p_id == P_ID)

        LIST = [x[0] for x in await ARHM_DB.fetch_all(query)]

        # двуручное блокируется двуручным и одноручным и наоборот
        # решаем блокировать ли обмундирование, занят ли слот
        LOCK = {
            'onehand':  'twohands' in LIST or LIST.count('onehand') > 1,
            'twohands': 'onehand' or 'twohands' in LIST,
            'head':     'head' in LIST,
            'body':     'body' in LIST,
            'legs':     'legs' in LIST,
            'shoes':    'shoes' in LIST,
                }.get(SLOT)

        if LOCK:
            MESS = {
                'onehand':  'Обе руки заняты!',
                'twohands': 'У Вас не хватает рук!',
                'head':     'Вы уже что-то носите на голове!',
                'body':     'Вы уже одеты во что-то!',
                'legs':     'На ваших ногах что-то надето!',
                'shoes':    'Вы уже обуты в другую обувь!',
                }.get(SLOT)
            return False, MESS

        # если проверка пройдена экипируем предмет
        query = t_inventory.update()\
            .where(and_(
                t_inventory.c.p_id == P_ID,
                t_inventory.c.i_id == I_ID
                ))\
            .values(slot=SLOT, date_update=datetime.now())
        await ARHM_DB.execute(query)
        return True, equip_mess

    @staticmethod
    async def remove(P_ID: int, I_ID: int):
        """снятие предмета и помещение в сумку"""
        query = t_inventory.update().where(and_(
            t_inventory.c.p_id == P_ID,
            t_inventory.c.i_id == I_ID
                )).values(slot='bag')
        await ARHM_DB.execute(query)

    @staticmethod
    async def drop(P_ID: int, I_ID: int):
        """Функция удаления из инвенторя"""
        query = t_inventory.delete().where(and_(
            t_inventory.c.p_id == P_ID,
            t_inventory.c.i_id == I_ID
            ))

        await ARHM_DB.execute(query)

    @staticmethod
    async def add(P_ID: int, I_ID: int) -> tuple[bool, str]:
        """функция добавления предмета в сумку
        проверка на уникальность"""
        query = t_inventory.select().where(and_(
            t_inventory.c.p_id == P_ID,
            t_inventory.c.i_id == I_ID
            ))
        res = await ARHM_DB.fetch_one(query)
        if res is not None:
            return False, String.get('double_item')
        # проверка на вместимость сумки
        query = t_inventory.select().where(and_(
            t_inventory.c.p_id == P_ID,
            t_inventory.c.slot == 'bag'
            ))
        res = await ARHM_DB.fetch_all(query)
        if len(res) >= MAX_BAG_CAPASITY:
            return False, String.get('not_free_space_in_bug')

        values = {
            'p_id': P_ID,
            'slot': 'bag',
            'i_id': I_ID,
            'date_update': datetime.now()
                }
        query = t_inventory.insert().values(**values)
        await ARHM_DB.execute(query)
        return True, 'Предмет добавлен в сумку'
