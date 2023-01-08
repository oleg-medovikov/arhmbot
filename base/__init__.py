from .base import ARHM_DB, metadata, engine

from .users import t_users
from .persons import t_persons
from .persons_defaults import t_persons_defaults
from .karta import t_karta
from .karta_descriptions import t_karta_descriptions
from .manual import t_manual
from .items import t_items
from .events import t_events
from .monsters import t_monsters

metadata.create_all(engine)

__all__ = [
    'ARHM_DB',
    't_users',
    't_persons',
    't_persons_defaults',
    't_karta',
    't_karta_descriptions',
    't_manual',
    't_items',
    't_events',
    't_monsters',
    ]
