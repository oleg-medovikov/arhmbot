from .base import metadata

from sqlalchemy import Table, Column, SmallInteger, String, Text, DateTime

t_manual = Table(
        'manual',
        metadata,
        Column('m_id',        SmallInteger, primary_key=True),
        Column('m_name',      String),
        Column('order',       SmallInteger),
        Column('text',        Text),
        Column('date_update', DateTime)
        )
