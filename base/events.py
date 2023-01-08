from .base import metadata

from sqlalchemy import Table, Column, SmallInteger, String, Boolean, DateTime

t_events = Table(
    'events',
    metadata,
    Column('e_id',            SmallInteger, primary_key=True),
    Column('e_name',          String),  # название события
    Column('single',          Boolean),  # одноразовый или нет
    Column('active',          Boolean),  # активен или нет
    Column('stage',           SmallInteger),  # номер этапа игры
    Column('node_id',         SmallInteger),  # номер локации
    Column('profession',      String),  # требования по профессии
    Column('demand',          String),  # требования по характеристикам
    Column('description',     String),  # описание события
    Column('mess_prize',      String),  # сообщение при удаче
    Column('mess_punishment', String),  # сообщение при наказании
    Column('check',           String),  # словарь проверок
    Column('choice',          Boolean),  # есть ли выбор
    Column('prize',           String),  # награда за успех
    Column('punishment',      String),  # наказание за провал
    Column('username',        String),  # кто добавил
    Column('date_update',     DateTime),
        )
