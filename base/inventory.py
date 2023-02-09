from base import metadata

from sqlalchemy import Table, Column, ARRAY, \
    Integer, SmallInteger, DateTime, Boolean

"""
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
    Column('sex',          Boolean),  # пол персонажа
    Column('head',         SmallInteger, nullable=True),  # голова
    Column('earrings',     SmallInteger, nullable=True),  # серьги
    Column('hands',        ARRAY(SmallInteger)),  # руки
    Column('rings',        ARRAY(SmallInteger)),  # кольца
    Column('body',         SmallInteger, nullable=True),  # костюм
    Column('legs',         SmallInteger, nullable=True),  # штаны
    Column('shoes',        SmallInteger, nullable=True),  # обувь
    Column('bag',          ARRAY(SmallInteger)),  # сумка
    Column('achievements', ARRAY(SmallInteger)),  # достижения
    Column('date_update',  DateTime),
    )
