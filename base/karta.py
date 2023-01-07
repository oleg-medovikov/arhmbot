from .base import metadata

from sqlalchemy import Table, Column, SmallInteger, String, Boolean, DateTime

t_karta = Table(
    'karta',
    metadata,
    Column('node_id',         SmallInteger, primary_key=True),  # id локации
    Column('name_node',       String),  # Имя локации
    Column('declension',      String),  # Склонение вы находитесь ...
    Column('contact_list_id', String),  # связи с другими узлами
    Column('district',        String),  # район  локации
    Column('district_id',     SmallInteger),  # код района локации
    Column('street',          Boolean),  # Является ли улицей
    Column('dist',            Boolean),  # является ли районом
    Column('date_update',     DateTime),
        )
