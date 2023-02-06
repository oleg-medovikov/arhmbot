from base import metadata

from sqlalchemy import Table, Column, ARRAY, \
    SmallInteger, String, DateTime

t_dialogs = Table(
        metadata,
        'dialogs',
        Column('d_id',        SmallInteger),  # идентификатор диалога
        Column('q_id',        SmallInteger),  # идентификатор вопроса
        Column('name',        String),  # название диалога
        Column('description', String),  # описание ситуации
        Column('answers',     ARRAY(String)),  # список ответов
        Column('transfer',    ARRAY(SmallInteger)),  # куда переходим
        Column('buy_items',   ARRAY(SmallInteger)),  # список товаров
        Column('buy_costs',   ARRAY(SmallInteger)),  # список цен
        Column('sale_items',  ARRAY(SmallInteger)),  # список на продажу
        Column('sale_costs',  ARRAY(SmallInteger)),  # цены продажи
        Column('date_update', DateTime),
        )
