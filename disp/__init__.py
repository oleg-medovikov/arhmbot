from .dispetcher import dp, bot
from .on_startup import on_startup
from .start import send_welcome, start_game
from .get_files import get_files_help, send_objects_file
from .update_base import update_base
from .manual import kb_full_manual, answer_man_buttom
from .test import test_func

__all__ = [
    'dp',
    'bot',
    'on_startup',
    'send_welcome',
    'start_game',
    'get_files_help',
    'send_objects_file',
    'update_base',
    'kb_full_manual',
    'answer_man_buttom',
    'test_func',
    ]
