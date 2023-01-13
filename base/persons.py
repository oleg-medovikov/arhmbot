from .base import metadata

from sqlalchemy import Table, Column, \
    Integer, SmallInteger, String, Boolean, DateTime

t_persons = Table(
    "persons",
    metadata,
    Column('p_id',              Integer, primary_key=True),  # номер
    Column('u_id',              Integer),  # user id
    Column('gamename',          String),  # имя персонажа
    Column('create_date',       DateTime),  # время создания
    Column('sex',               Boolean),  # 1 - male, 0 - female
    Column('profession',        String),  # профессия персонажа
    Column('destination',       String),  # цель прибытия в Архэм (так шутка)
    Column('start_location_id', SmallInteger),
    Column('start_money',       SmallInteger),
    Column('max_health',        SmallInteger),  # максимальное здоровье
    Column('max_mind',          SmallInteger),  # максимальный рассудок
    Column('speed',             SmallInteger),  # скорость
    Column('stealth',           SmallInteger),  # скрытность
    Column('strength',          SmallInteger),  # сила
    Column('knowledge',         SmallInteger),  # знания
    Column('godliness',         SmallInteger),  # набожность
    Column('luck',              SmallInteger),  # удача
    Column('death',             Boolean),  # 0 - живой, 1 - мертвый
    Column('d_reason',          String),  # причина смерти
    Column('date_death',        DateTime),  # время смерти
    )
