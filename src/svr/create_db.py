'''Auto-creates the database'''

from cfg import CONNECTION_STRING

from db import setup_db, populate
setup_db(CONNECTION_STRING)
populate(CONNECTION_STRING)
