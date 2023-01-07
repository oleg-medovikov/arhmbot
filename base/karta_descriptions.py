from .base import metadata

from sqlalchemy import Table, Column, SmallInteger, String, DateTime

t_karta_descriptions = Table(
    'karta_descriptions',
    metadata,
    Column('node_id',     SmallInteger),  # id локации
    Column('stage',       SmallInteger),  # номер игрового этапа
    Column('description', String),  # описание локации
    Column('date_update', DateTime),  # время обновления
    )
