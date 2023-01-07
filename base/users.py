from .base import metadata

from sqlalchemy import Table, Column, \
    Integer, BigInteger, String, Boolean, DateTime

t_users = Table(
    "users",
    metadata,
    Column('u_id',        Integer, primary_key=True),  # TG_ID
    Column('tg_id',       BigInteger),  # TG_ID
    Column('username',    String),  # логин пользователя
    Column('name_tg',     String),  # имя пользователя в телеге если есть
    Column('admin',       Boolean),  # является ли админом
    Column('date_create', DateTime),
    )
