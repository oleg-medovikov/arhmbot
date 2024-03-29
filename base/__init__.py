from .base import ARHM_DB, metadata, engine

from .users import t_users
from .persons import t_persons
from .persons_defaults import t_persons_defaults
from .karta import t_karta
from .karta_descriptions import t_karta_descriptions
from .manual import t_manual
from .items import t_items
from .inventory import t_inventory
from .events import t_events
from .monsters import t_monsters
from .drop_items import t_drop_items
from .events_history import t_events_history
from .persons_status import t_persons_status
from .strings import t_strings
from .fight_history import t_fight_history
from .shops import t_shops
from .dialogs import t_dialogs
from .journal import t_journal
from .dialogs_history import t_dialogs_history

metadata.create_all(engine)

__all__ = [
    'ARHM_DB',
    't_users',
    't_persons',
    't_persons_defaults',
    't_persons_status',
    't_karta',
    't_karta_descriptions',
    't_manual',
    't_items',
    't_inventory',
    't_events',
    't_monsters',
    't_drop_items',
    't_events_history',
    't_strings',
    't_fight_history',
    't_shops',
    't_dialogs',
    't_dialogs_history',
    't_journal',
    ]
