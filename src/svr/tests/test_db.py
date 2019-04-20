import unittest
import context
from svr.db import Dal

class TestDal(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_user(self):
        with Dal() as dal:
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
