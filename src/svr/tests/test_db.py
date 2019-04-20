import unittest
import context
import svr.db
import os
from pathlib import Path

DB_NAME = "test.db"
svr.db.schema.DB_NAME = DB_NAME
svr.db.data.PKG_DB_NAME = DB_NAME
from svr.db import Dal, populate, dal_factory

class TestDal(unittest.TestCase):
    def setUp(self):
        svr.db.schema.setup_db()
        populate()
        self.dal_fct = dal_factory(DB_NAME)

    def tearDown(self):
        db_file = Path(svr.db.schema.DB_NAME)
        if db_file.is_file():
            os.remove(db_file)

    def test_create_user(self):
        with self.dal_fct() as dal:
            user = dal.create_user(name='Vasilios Magriplis', 
                                    email='test@example.com', 
                                    picture='path/to/picture')
            dal.flush()
            self.assertTrue(user.id is not None)


if __name__ == '__main__':
    unittest.main()
