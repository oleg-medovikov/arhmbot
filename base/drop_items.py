from .base import metadata

from sqlalchemy import Integer, SmallInteger, Table, Column, String, DateTime

t_drop_items = Table(
    'drop_items',
    metadata,
    Column('di_id',    Integer, primary_key=True),
    Column('node_id',  SmallInteger),  # локация
    Column('i_id',     SmallInteger),  # предмет
    Column('stage',    SmallInteger),  # игровой этап
    Column('gamename', String),        # имя персонажа
    Column('comment',  String),        # дополнительный комментарий
    Column('time',     DateTime),      # время когда это произошло
    )
