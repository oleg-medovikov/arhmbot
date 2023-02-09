from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sqlalchemy import select, and_

from base import ARHM_DB, t_inventory, t_items
from conf import MAX_BAG_CAPASITY
from .String import String
from .Person import Person


class Inventory(BaseModel):
    p_id:         int
    head:         Optional[int]
    earrings:     list
    hands:        list
    rings:        list
    body:         Optional[int]
    legs:         Optional[int]
    shoes:        Optional[int]
    bag:          list
    achievements: list
    date_update:  Optional[datetime] = datetime.now()

    @staticmethod
    async def get(PERS: 'Person') -> 'Inventory':
        "Вытаскиваем инвентарь персонажа"
        query = t_inventory.select(
            t_inventory.c.p_id == PERS.p_id
            )
        res = await ARHM_DB.fetch_one(query)
        if res is None:
            # Необходимо создать пустой инвентарь
            values = {
                'p_id':         PERS.p_id,
                'sex':          PERS.sex,
                'earrings':     [],
                'hands':        [],
                'rings':        [],
                'bag':          [],
                'achievements': [],
                'date_update':  datetime.now()
                }
            return Inventory(*values)
        else:
            return Inventory(*res)

    async def check_item(self, I_ID: int) -> bool:
        "проверяем наличие предмета у персонажа"
        for key, value in self:
            if key == 'p_id':
                continue
            if type(value) is list:
                if I_ID in value:
                    return True
            if type(value) is int:
                if I_ID == value:
                    return True
        return False

    async def check_not_item(self, I_ID: int) -> bool:
        "проверяем отсутствие предмета у персонажа"
        for key, value in self:
            if key == 'p_id':
                continue
            if type(value) is list:
                if I_ID in value:
                    return False
            if type(value) is int:
                if I_ID == value:
                    return False
        return True

    async def bug_free_space(self, P_ID: int) -> bool:
        "Проверяем есть ли свободное место в сумке"
        return len(self.bag) < MAX_BAG_CAPASITY

    async def get_all(self) -> dict:
        "Возвращаем список всех предметов персонажа"
        list_ = []
        DICT = dict()
        for key, value in self:
            if key == 'p_id':
                DICT[key] = value
                continue

            if type(value) is list:
                query = select([
                    t_items.c.i_id,
                    t_items.c.name,
                    t_items.c.emoji,
                    ]).where(t_items.c.p_id.in_(value))
            if type(value) is list:
                query = select([
                    t_items.c.i_id,
                    t_items.c.name,
                    t_items.c.emoji,
                    ]).where(t_items.c.p_id.in_(value))

            for row in await ARHM_DB.fetch_all(query):
                list_.append(dict(row))

            DICT[key] = list_

        return DICT

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
            return False, await String.get('double_item')
        # проверка на вместимость сумки
        query = t_inventory.select().where(and_(
            t_inventory.c.p_id == P_ID,
            t_inventory.c.slot == 'bag'
            ))
        res = await ARHM_DB.fetch_all(query)
        if len(res) >= MAX_BAG_CAPASITY:
            return False, await String.get('not_free_space_in_bug')

        values = {
            'p_id': P_ID,
            'slot': 'bag',
            'i_id': I_ID,
            'date_update': datetime.now()
                }
        query = t_inventory.insert().values(**values)
        await ARHM_DB.execute(query)
        return True, 'Предмет добавлен в сумку'
