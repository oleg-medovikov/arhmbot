from .base import metadata

from sqlalchemy import Table, Column, Integer, SmallInteger, String, Boolean, \
    DateTime
from sqlalchemy.dialects.postgresql import UUID


t_fight_history = Table(
    'fight_history',
    metadata,
    Column('gametime',       SmallInteger),  # игровое время
    Column('p_id',           Integer),  # идентификатор пользователя
    Column('m_id',           SmallInteger),  # идентификатор монстра
    Column('m_uid',          UUID),  # уникальный идентификатор монстра
    Column('battle_round',   SmallInteger),  # раунд боя с монстром
    Column('p_start_hp',     SmallInteger),  # здоровье перс в начале раунда
    Column('p_start_md',     SmallInteger),  # рассудок перс в начале раунда
    Column('m_start_hp',     SmallInteger),  # здоровье монстра в начале раунда
    Column('numbers_hp',     String),  # броски игрока на урон (словарь)
    Column('numbers_md',     String),  # броски игрока на рассудок (словарь)
    Column('p_damage_hp',    SmallInteger),  # число успехов (урон по монстру)
    Column('m_damage_hp',    SmallInteger),  # урон монстра по здоровью игрока
    Column('m_damage_md',    SmallInteger),  # урон монстра по рассудку игрока
    Column('p_end_hp',       SmallInteger),  # здоровье игрока в конце раунда
    Column('p_end_md',       SmallInteger),  # рассудок игрока в конце раунда
    Column('m_end_hp',       SmallInteger),  # здоровье монстра в конце раунда
    Column('p_alive',        Boolean),  # живой ли игрок
    Column('p_right_mind',   Boolean),  # в здравом ли уме игрок
    Column('m_alive',        Boolean),  # живой ли монстр
    Column('description',    String),  # комментарий
    Column('date_create',    DateTime),  # реальное время события
        )
