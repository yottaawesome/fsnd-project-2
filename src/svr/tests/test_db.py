import unittest
import context
import svr.db
import os
from pathlib import Path

DB_NAME = "test.db"
svr.db.schema.DB_NAME = DB_NAME
svr.db.dal.PKG_DB_NAME = DB_NAME
svr.db.data.PKG_DB_NAME = DB_NAME
from svr.db import Dal, populate

class TestDal(unittest.TestCase):
    def setUp(self):
        svr.db.schema.setup_db()
        populate()

    def tearDown(self):
        db_file = Path(svr.db.schema.DB_NAME)
        if db_file.is_file():
            os.remove(db_file)

    def test_create_user(self):
        Dal.print_db_name()
        with Dal() as dal:
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
