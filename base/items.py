from .base import metadata

from sqlalchemy import Table, Column, SmallInteger, String, Boolean, DateTime

t_items = Table(
    'items',
    metadata,
    Column('i_id',        SmallInteger),  # номер предмета
    Column('name',        String),  # название предмета
    Column('description', String),  # описание предмета
    Column('equip_mess',  String),  # сообщение при использовании
    Column('fail_mess',   String),  # сообщение если не удалось использовать
    Column('remove_mess', String),  # сообщение когда снимаешь предмет
    Column('drop_mess',   String),  # сообщение когда выбрасываешь предмет
    Column('i_type',      String),  # Тип предмета
    Column('slot',        String),  # куда надевается предмет
    Column('effect',      String),  # json описывающий эффекты предмета
    Column('demand',      String),  # json описывающий требования предмета
    Column('emoji',       String),  # emoji иконка для данного предмета
    Column('cost',        SmallInteger),  # Стоимость предмета
    Column('single_use',  Boolean),  # одноразовость
    Column('achievement', Boolean),  # Является ли медалью персонажа
    Column('date_update', DateTime),  # Время обновления предмета админом
    )
