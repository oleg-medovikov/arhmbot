from .base import metadata

from sqlalchemy import Table, Column, SmallInteger, Boolean, DateTime

t_events_history = Table(
    'events_history',
    metadata,
    Column('gametime',    SmallInteger),
    Column('p_id',        SmallInteger),
    Column('e_id',        SmallInteger),
    Column('result',      Boolean, nullable=True),
    Column('date_update', DateTime),
    )
