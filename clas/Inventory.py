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
                'hands':        [],
                'rings':        [],
                'bag':          [],
                'achievements': [],
                'date_update':  datetime.now()
                }
            query = t_inventory.insert().values(values)
            await ARHM_DB.execute(query)
            return Inventory(**values)
        else:
            return Inventory(**res)

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

    async def bug_free_space(self) -> bool:
        "Проверяем есть ли свободное место в сумке"
        return len(self.bag) < MAX_BAG_CAPASITY

    async def get_all(self) -> dict:
        "Возвращаем список всех предметов персонажа"
        DICT = dict()
        for key, value in self:
            if key in ('p_id', 'sex', 'date_update'):
                DICT[key] = value
                continue
            if value is None:
                DICT[key] = []
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
            value = getattr(
                self,
                'hands' if ITEM.slot in ('onehand', 'twohands') else ITEM.slot
                    )
        except AttributeError:
            raise ValueError(f"Несуществующий слот у предмета {ITEM.name}")

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

            setattr(
                self,
                'hands' if ITEM.slot in ('onehand', 'twohands') else ITEM.slot,
                value
                    )

        if value is None:
            # Если слот пустой, то просто добавляем в него предмет
            setattr(
                self,
                'hands' if ITEM.slot in ('onehand', 'twohands') else ITEM.slot,
                ITEM.i_id
                    )

        self.date_update = datetime.now()
        # обновляем строчку в базе
        query = t_inventory.update()\
            .where(t_inventory.c.p_id == self.p_id)\
            .values(self.dict())
        await ARHM_DB.execute(query)

        return True, ITEM.equip_mess

    async def remove(self, I_ID: int) -> tuple[bool, str]:
        """снятие предмета и помещение в сумку"""
        COUNT = MAX_BAG_CAPASITY - len(self.bag)
        if COUNT < 1:
            return False, 'Вам нужно освободить место в сумке!'
        # узнаем в каком слоте предмет
        SLOT = ''
        for key, value in self:
            if key == 'p_id':
                continue
            if type(value) is list:
                if I_ID in value:
                    SLOT = key
                    value.remove(I_ID)
                    setattr(self, key, value)
                    break
            if type(value) is int:
                if I_ID == value:
                    SLOT = key
                    setattr(self, key, None)
                    break

        if SLOT == '':
            return False, 'Вы пытаетесь снять то, что не одето!'

        # кладем предмет в сумку
        self.bag.append(I_ID)
        # обновляем базу
        query = t_inventory.update()\
            .where(t_inventory.c.p_id == self.p_id)\
            .values(self.dict())
        await ARHM_DB.execute(query)

        return True, 'Предмет положен в сумку'

    async def drop(self, I_ID: int):
        """Функция удаления из инвенторя"""
        # узнаем в каком слоте предмет
        SLOT = ''
        for key, value in self:
            if key == 'p_id':
                continue
            if type(value) is list:
                if I_ID in value:
                    SLOT = key
                    value.remove(I_ID)
                    setattr(self, key, value)
                    break
            if type(value) is int:
                if I_ID == value:
                    SLOT = key
                    setattr(self, key, None)
                    break
        if SLOT == '':
            return False, 'Нет такого предмета!'
        # обновляем базу
        query = t_inventory.update()\
            .where(t_inventory.c.p_id == self.p_id)\
            .values(self.dict())
        await ARHM_DB.execute(query)
        return True, 'Предмет выброшен!'

    async def add(self, I_ID: int) -> tuple[bool, str]:
        """функция добавления предмета в сумку
        проверка на уникальность"""
        if I_ID in self.bag:
            return False, await String.get('double_item')
        if len(self.bag) >= MAX_BAG_CAPASITY:
            return False, await String.get('not_free_space_in_bug')

        self.bag.append(I_ID)
        # меняем таблицу
        query = t_inventory.update()\
            .where(t_inventory.c.p_id == self.p_id)\
            .values(bag=self.bag)

        await ARHM_DB.execute(query)
        return True, 'Предмет добавлен в сумку'
