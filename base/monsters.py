from .base import metadata

from sqlalchemy import Table, Column, ARRAY, String, SmallInteger, DateTime

t_monsters = Table(
    'monsters',
    metadata,
    Column('m_id',            SmallInteger, primary_key=True),  #
    Column('name',            String),  # название монстра
    Column('description',     String),  # описание монстра
    Column('mess_win',        String),  # сообщение при выигрыше
    Column('mess_lose_hp',    String),  # сообщение при смерти персонажа
    Column('mess_lose_md',    String),  # сообщение когда перс сходит с ума
    Column('check_of_stels',  SmallInteger),  # проверка на скрытность
    Column('nigthmare',       SmallInteger),  # кошмароность монстра
    Column('crush',           SmallInteger),  # сокрушение монстра
    Column('phisical_resist', SmallInteger),  # физическое сопротивление
    Column('magic_resist',    SmallInteger),  # магическое сопротивление
    Column('check_mind',      SmallInteger),  # проверка разума
    Column('check_fight',     SmallInteger),  # проверка боем
    Column('mind_damage',     SmallInteger),  # урон по разуму
    Column('body_damage',     SmallInteger),  # урон по здоровью
    Column('health',          SmallInteger),  # здоровье монстра
    Column('price',           SmallInteger),  # награда за победу
    Column('item',            ARRAY(SmallInteger)),  # выпадающие предметы
    Column('experience',      SmallInteger),  # количество опыта
    Column('date_update',     DateTime),
        )
