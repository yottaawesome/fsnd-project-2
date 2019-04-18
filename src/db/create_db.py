#!/usr/bin/env python3
'''Creates the DB.'''

import os
from db_setup import DB_NAME, setup_db
from pathlib import Path

db_file = Path(DB_NAME)
if db_file.is_file:
    os.remove(db_file)

setup_db()

import populate_db
