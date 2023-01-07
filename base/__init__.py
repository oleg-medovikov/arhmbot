from .base import ARHM_DB, metadata, engine

from .users import t_users
from .persons import t_persons
from .persons_defaults import t_persons_defaults
from .karta import t_karta

metadata.create_all(engine)

__all__ = [
    'ARHM_DB',
    't_users',
    't_persons',
    't_persons_defaults',
    't_karta',
    ]
