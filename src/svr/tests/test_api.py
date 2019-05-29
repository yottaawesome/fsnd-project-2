from svr.db import Dal, populate, dal_factory
from svr.app import main_app
import unittest
import context
import svr.db
import svr.app
import os
from pathlib import Path
import threading

CONNECTION_STRING = "test.db"


'''
# TODO: need to give this more thought
def run(obj):
    main_app.debug = True
    main_app.secret_key = os.urandom(24)
    obj.running = True
    main_app.run(host='127.0.0.1', port=5000)


class TestApi(unittest.TestCase):
    def __init__(self):
        self.running = False

    def setUp(self):
        svr.db.schema.setup_db(DB_NAME)
        populate(DB_NAME)
        self.dal_fct = dal_factory(DB_NAME)
        self.daemon = threading.Thread(target=run, args=self, daemon=True)
        self.daemon.start()
        while self.running is False:
            pass

    def tearDown(self):
        db_file = Path(svr.db.schema.DB_NAME)
        if db_file.is_file():
            os.remove(db_file)

    def generic_test(self):
        pass

if __name__ == '__main__':
    unittest.main()
'''