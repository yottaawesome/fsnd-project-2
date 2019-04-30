import unittest
import context
import svr.db
import svr.app
import os
from pathlib import Path
import threading

DB_NAME = "test.db"
svr.db.schema.DB_NAME = DB_NAME
svr.db.data.PKG_DB_NAME = DB_NAME
from svr.db import Dal, populate, dal_factory

from svr.app import main_app

# TODO: need to give this more thought

def run(obj):
    main_app.debug = True
    main_app.secret_key = os.urandom(24)
    obj.running = True
    main_app.run(host = '127.0.0.1', port = 5000)

class TestApi(unittest.TestCase):
    def __init__(self):
        self.running = False

    def setUp(self):
        svr.db.schema.setup_db()
        populate()
        self.dal_fct = dal_factory(DB_NAME)
        self.daemon = threading.Thread(target=run, args=self, daemon=True)
        self.daemon.start()
        while self.running == False:
            i=1

    def tearDown(self):
        db_file = Path(svr.db.schema.DB_NAME)
        if db_file.is_file():
            os.remove(db_file)

    def generic_test(self):
        i = 1

if __name__ == '__main__':
    unittest.main()