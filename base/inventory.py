from base import metadata

from sqlalchemy import Table, Column, ARRAY, \
    Integer, SmallInteger, String, DateTime

t_inventory = Table(
        'inventory',
        metadata,
        Column('p_id', Integer),
        Column('slot', String),
        Column('i_id', SmallInteger),
        Column('date_update', DateTime),
        )
"""
t_inventory = Table(
        'inventory',
        metadata,
        Column('p_id',         Integer),  # идентификатор персонажа
        Column('head',         SmallInteger),  # голова
        Columns('earrings',    SmallInteger),  # серьги
        Column('hand_one',     SmallInteger),  # правая рука
        Column('hand_two',     SmallInteger),  # левая рука
        Column('rings',        ARRAY(SmallInteger)),  # кольца
        Column('body',         SmallInteger),  # костюм
        Column('legs',         SmallInteger),  # штаны
        Column('shoes',        SmallInteger),  # обувь
        Column('bag',          ARRAY(SmallInteger)),  # сумка
        Column('achievements', ARRAY(SmallInteger)),  # достижения
        Column('date_update',  DateTime),
        )
"""
