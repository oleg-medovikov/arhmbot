from .base import metadata

from sqlalchemy import Table, Column, SmallInteger, Boolean

t_dialogs_history = Table(
    'dialogs_history',
    metadata,
    Column('p_id',        SmallInteger),  # персонаж
    Column('s_id',        SmallInteger),  # магазин
    Column('d_id',        SmallInteger),  # диалог
    Column('q_id',        SmallInteger),  # вопрос
    Column('result',      Boolean, nullable=True),
    )
