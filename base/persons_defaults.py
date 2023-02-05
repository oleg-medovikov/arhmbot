from .base import metadata

from sqlalchemy import Table, Column, ARRAY, SmallInteger, String, DateTime

t_persons_defaults = Table(
    "persons_defaults",
    metadata,
    Column('date_update',       DateTime),
    Column('profession',        String),
    Column('start_location_id', SmallInteger),
    Column('money_min',         SmallInteger),
    Column('money_max',         SmallInteger),
    Column('start_list_items',  ARRAY(SmallInteger)),
    Column('max_health_min',    SmallInteger),
    Column('max_health_max',    SmallInteger),
    Column('max_mind_min',      SmallInteger),
    Column('max_mind_max',      SmallInteger),
    Column('speed_min',         SmallInteger),
    Column('speed_max',         SmallInteger),
    Column('stealth_min',       SmallInteger),
    Column('stealth_max',       SmallInteger),
    Column('strength_min',      SmallInteger),
    Column('strength_max',      SmallInteger),
    Column('knowledge_min',     SmallInteger),
    Column('knowledge_max',     SmallInteger),
    Column('godliness_min',     SmallInteger),
    Column('godliness_max',     SmallInteger),
    Column('luck_min',          SmallInteger),
    Column('luck_max',          SmallInteger)
    )
