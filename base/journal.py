from .base import metadata

from sqlalchemy import Table, Column, SmallInteger, Text,\
    DateTime, String

t_journal = Table(
    'journal',
    metadata,
    Column('gametime',    SmallInteger),
    Column('p_id',        SmallInteger),
    Column('name',        String),
    Column('metka',       SmallInteger),
    Column('mess',        Text),
    Column('date_create', DateTime),
    )
