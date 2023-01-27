from .base import metadata

from sqlalchemy import Table, Column, SmallInteger, String, Text, DateTime

t_strings = Table(
        'strings',
        metadata,
        Column('s_id',        SmallInteger, primary_key=True),
        Column('s_name',      String),
        Column('text',        Text),
        Column('date_update', DateTime)
        )
