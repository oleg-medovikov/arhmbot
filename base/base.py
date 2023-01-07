from databases import Database
from sqlalchemy import create_engine, MetaData

from conf import ARHM_PSQL

ARHM_DB = Database(ARHM_PSQL)
metadata = MetaData()
engine = create_engine(ARHM_PSQL)
