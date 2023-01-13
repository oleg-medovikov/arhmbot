from base import metadata

from sqlalchemy import Table, Column, Integer, SmallInteger, String, DateTime


t_inventory = Table(
        'inventory',
        metadata,
        Column('p_id', Integer),
        Column('slot', String),
        Column('i_id', SmallInteger),
        Column('date_update', DateTime),
        )
