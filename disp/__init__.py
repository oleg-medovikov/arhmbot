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
    'get_files_help',
    'send_objects_file',
    'update_base',
    'kb_full_manual',
    'answer_man_buttom',
    'test_func',
    ]
