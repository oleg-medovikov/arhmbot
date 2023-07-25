from .base import metadata

from sqlalchemy import Table, Column, SmallInteger, Text,\
    DateTime, String, Integer

t_journal = Table(
    'journal',
    metadata,
    Column('gametime',    SmallInteger),
    Column('p_id',        SmallInteger),
    Column('name',        String),  # название записи
    Column('metka',       Integer),  # метка уникального события
    Column('mess',        Text),  # генерируемый текст события
    Column('date_create', DateTime),
    )
