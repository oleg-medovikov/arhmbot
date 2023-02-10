from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sqlalchemy import select, and_

from base import ARHM_DB, t_inventory, t_items
from conf import MAX_BAG_CAPASITY
from .String import String
from .Person import Person
from .Item import Item


class Inventory(BaseModel):
    p_id:         int
    head:         Optional[int]
    earrings:     Optional[int]
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
            query = t_inventory.insert(*values)
            await ARHM_DB.execute(query)
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
        DICT = dict()
        for key, value in self:
            if key == 'p_id':
                DICT[key] = value
                continue
            list_ = []

            if type(value) is list:
                query = select([
                    t_items.c.i_id,
                    t_items.c.name,
                    t_items.c.emoji,
                    ]).where(t_items.c.i_id.in_(value))
            if type(value) is int:
                query = select([
                    t_items.c.i_id,
                    t_items.c.name,
                    t_items.c.emoji,
                    ]).where(t_items.c.i_id == value)

            for row in await ARHM_DB.fetch_all(query):
                list_.append(dict(row))

            DICT[key] = list_

        return DICT

    async def equip(self, ITEM: 'Item') -> tuple[bool, str]:
        """ Функция надевания предмета
        нужно проверить есть ли в данном слоте другой предмет
        двуручное блокируется двуручным и одноручным и наоборот
        решаем блокировать ли обмундирование, занят ли слот
        """
        try:
            value = getattr(self, ITEM.slot)
        except AttributeError:
            raise f"Несуществующий слот у предмета {ITEM.name}"

        if type(value) is int:
            # это если слот занят
            MESS = {
                'earrings': 'Вы уже носите другие серьги!',
                'head':     'Вы уже что-то носите на голове!',
                'body':     'Вы уже одеты во что-то!',
                'legs':     'На ваших ногах что-то надето!',
                'shoes':    'Вы уже обуты в другую обувь!',
            }.get(ITEM.slot)
            return False, MESS
        if type(value) is list:
            # для слотов с несколькими предметами проверяем количество
            COUNT = len(value)
            if ITEM.slot == 'twohands' and COUNT:
                return False, 'Этот двуручный предмет, требует свободных рук'

            if ITEM.slot == 'onehand' and COUNT > 1:
                return False, 'Обе руки заняты!'

            # если всё ок, добавляем предмет
            # двуручное добавляем дважды
            value.append(ITEM.i_id)
            if ITEM.slot == 'twohands':
                value.append(ITEM.i_id)

            setattr(self, ITEM.slot, value)

        if value is None:
            # Если слот пустой, то просто добавляем в него предмет
            setattr(self, ITEM.slot, ITEM.i_id)

        self.date_update = datetime.now()
        # обновляем строчку в базе
        query = t_inventory.update()\
            .where(t_inventory.c.p_id == self.p_id)\
            .values(*self)
        await ARHM_DB.execute(query)

        return True, ITEM.equip_mess

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
