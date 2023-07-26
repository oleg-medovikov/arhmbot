from .dispetcher import dp, bot
from .on_startup import on_startup
from .start import send_welcome, start_game
from .get_files import get_files_help, send_objects_file
from .update_base import update_base
from .manual import kb_full_manual, answer_man_buttom
from .test import test_func
from .register import hello_callback_register, \
    profession_callback_previos, load_gamename_register, \
    load_sex_register, load_profession_register, \
    load_destination_register
from .continue_game import continue_game
from .look_around import look_around, look_around_get_item
from .relocation import leave, relocation
from .inventory_main import inventory_main
from .inventory_bag_item import inventory_bag_item
from .inventory_using_item import inventory_using_item
from .inventory_drop_item import inventory_drop_item, inventory_drop_item_ask
from .inventory_equip_items import inventory_equip_items
from .inventory_remove_item import inventory_remove_item
from .get_event import get_event
from .end_event import end_event
from .monster_fight import monster_fight
from .go_to_the_shop import go_to_the_shop
from .buy_item import buy_item
from .dialog import dialog
from .prepare_main import prepare_main
from .prepare_main_quest import prepare_main_quest
from .prepare_relocations import prepare_relocations
from .prepare_map import prepare_map

__all__ = [
    'dp',
    'bot',
    'on_startup',
    'send_welcome',
    'hello_callback_register',
    'profession_callback_previos',
    'load_gamename_register',
    'load_sex_register',
    'load_profession_register',
    'load_destination_register',
    'start_game',
    'continue_game',
    'inventory_main',
    'inventory_bag_item',
    'inventory_using_item',
    'inventory_drop_item',
    'inventory_drop_item_ask',
    'inventory_equip_items',
    'inventory_remove_item',
    'look_around',
    'look_around_get_item',
    'leave',
    'relocation',
    'get_files_help',
    'send_objects_file',
    'update_base',
    'kb_full_manual',
    'answer_man_buttom',
    'test_func',
    'get_event',
    'end_event',
    'monster_fight',
    'go_to_the_shop',
    'buy_item',
    'dialog',
    'prepare_main',
    'prepare_main_quest',
    'prepare_relocations',
    'prepare_map',
    ]
