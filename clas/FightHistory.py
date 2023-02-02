from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
import json
from json.decoder import JSONDecodeError

from base import ARHM_DB, t_fight_history

from .Monster import Monster
from .PersonStatus import PersonStatus


class FightHistory(BaseModel):
    gametime:      int
    p_id:          int
    m_id:          int
    m_uid:         UUID
    battle_round = 0
    p_start_hp:    int
    p_start_md:    int
    m_start_hp:    int
    numbers_hp:    Optional[str] = '{}'
    numbers_md:    Optional[str] = '{}'
    p_damage_hp = 0
    m_damage_hp = 0
    m_damage_md = 0
    p_end_hp = 0
    p_end_md = 0
    m_end_hp = 0
    p_alive = True
    p_right_mind = True
    m_alive = True
    description:   Optional[str]
    date_create:   Optional[datetime] = datetime.now()

    @staticmethod
    async def get_history(M_UID: int) -> list:
        "Достаем все раунды сражения с монстром"
        query = t_fight_history.select(
                t_fight_history.c.m_uid == M_UID
                ).order_by(t_fight_history.c.battle_round)
        list_ = []
        for row in await ARHM_DB.fetch_all(query):
            list_.append(FightHistory(**row))
        return list_

    def get_num_hp(self) -> dict:
        return json.loads(self.numbers_hp)

    def get_num_md(self) -> dict:
        try:
            return json.loads(self.numbers_md)
        except JSONDecodeError:
            return {
                'success': True,
                'luck': 0,
                'numbers': [],
                'check_passed': 0
                    }

    async def new_battle_round(
        self,
        STAT: 'PersonStatus',
        MONSTER: 'Monster'
            ) -> 'FightHistory':
        "Отыгрываем и сохраняем раунд боя персонажа с монстром"
        # ===========подготовка
        self.battle_round += 1
        # обновляем игровое время
        self.gametime = STAT.gametime

        if self.battle_round == 1:
            # первый раунд начинается с проверки на сокрушение и кошмар
            if MONSTER.crush:
                # проверим умрёт ли персонаж
                if self.p_start_hp - MONSTER.crush < 1:
                    self.p_alive = False
                    self.p_end_hp = self.p_start_hp - MONSTER.crush
                    self.description = 'Сокрушён мощью монстра'
                else:
                    self.m_damage_hp = MONSTER.crush

            if MONSTER.nigthmare and self.p_alive is True:
                if self.p_start_md - MONSTER.nigthmare < 1:
                    self.p_alive = False
                    self.p_end_md = self.p_start_md - MONSTER.nigthmare
                    self.description = 'Рехнулся с кошмарности монстра'
                else:
                    self.m_damage_md = MONSTER.nigthmare
        else:
            # если раунд не первый, то обнуляем урон
            self.p_damage_hp = 0
            self.m_damage_md = 0
            self.m_damage_hp = 0
            # стартовые значения приравниваем к конечным
            self.p_start_hp = self.p_end_hp
            self.p_start_md = self.p_end_md
            self.m_start_hp = self.m_end_hp
        # ==========================

        # непосредственно сам раунд боя
        # делаем проверку на рассудок
        if MONSTER.check_mind and self.p_alive is True:
            DICT = STAT.dice_roll(STAT.knowledge + STAT.godliness)
            self.numbers_md = json.dumps(DICT)
            if DICT['check_passed'] < MONSTER.check_mind:
                self.m_damage_md += MONSTER.mind_damage
                self.p_end_md = self.p_start_md - self.m_damage_md
                if self.p_end_md < 1:
                    self.p_alive = False
                    self.description = 'Сошёл с ума в бою'
            else:
                # тут нужно не забыть про урон от кошмара монстра
                # в первом раунде!
                self.p_end_md = self.p_start_md - self.m_damage_md
        else:
            # если монстр не может нанести урон по рассудку
            self.numbers_md = 'проверка рассудка не требовалась'
            self.p_end_md = self.p_start_md - self.m_damage_md

        # проверка боя
        if MONSTER.check_fight and self.p_alive is True:
            DICT = STAT.dice_roll(STAT.strength)
            self.numbers_hp = json.dumps(DICT)
            try:
                self.p_damage_hp = DICT['check_passed'] // MONSTER.check_fight
            except ZeroDivisionError:
                self.p_damage_hp = DICT['check_passed']

            self.m_end_hp = self.m_start_hp - self.p_damage_hp

            if self.m_end_hp < 1:
                self.m_alive = False
                self.description = "монстр был побеждён в честном бою"
                # не забываем прописать здоровье персонажа
                self.p_end_hp = self.p_start_hp - self.m_damage_hp
            else:
                self.m_damage_hp += MONSTER.body_damage

        # если монстр и персонаж выжили вычитаем накопившийся урон
        if self.p_alive is True and self.m_alive is True:
            self.p_end_hp = self.p_start_hp - self.m_damage_hp
            if self.p_end_hp < 1:
                self.p_alive = False
                self.description = 'Персонаж умер в бою'

        self.date_create = datetime.now()
        query = t_fight_history.insert().values(self.dict())
        await ARHM_DB.execute(query)

        return self
