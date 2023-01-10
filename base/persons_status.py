from .base import metadata

from sqlalchemy import Boolean, Table, Column, Integer, SmallInteger, DateTime

t_persons_status = Table(
    "persons_status",
    metadata,
    Column('date_update', DateTime),  # дата обновления строки
    Column('p_id',        Integer),  # идентификатор персонажа
    Column('death',       Boolean),
    Column('gametime',    Integer),  # время проведенное в археме
    Column('stage',       SmallInteger),  # номер игрового этапа
    Column('money',       SmallInteger),  # количество денег
    Column('location',    SmallInteger),  # локация, где он находится
    Column('health',      SmallInteger),  # здоровье
    Column('mind',        SmallInteger),  # состояние рассудка
    Column('speed',       SmallInteger),
    Column('stealth',     SmallInteger),
    Column('strength',    SmallInteger),
    Column('knowledge',   SmallInteger),
    Column('godliness',   SmallInteger),
    Column('luck',        SmallInteger),
    Column('experience',  SmallInteger),
    Column('bless',       SmallInteger),
    Column('proof',       SmallInteger),
    Column('hunger',      SmallInteger),  # Уровень голода
    Column('weary',       SmallInteger),  # уровень утомленности
    )
