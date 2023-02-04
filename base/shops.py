from .base import metadata

from sqlalchemy import Table, Column, ARRAY, SmallInteger, String, DateTime

t_shops = Table(
        'shops',
        metadata,
        Column('s_id',          SmallInteger, primary_key=True),
        Column('l_id',          SmallInteger),  # id локации
        Column('stage',         SmallInteger),  # номер стадии игры
        Column('shop_name',     String),  # имя для магазина
        Column('demand',        String),  # требования для входа
        Column('mess_welcome',  String),  # приветственное сообщение
        Column('mess_not_pass', String),  # когда не проходишь по требованиям
        Column('mess_goodbye',  String),  # прощальное сообщение
        Column('product_list',  ARRAY(SmallInteger)),  # что продают
        Column('shopping_list', ARRAY(SmallInteger)),  # что покупают
        Column('date_update',   DateTime)  # дата обновления
        )
