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

    def test_get_user(self):
        with self.dal_fct() as dal:
            user = dal.create_user(name='Vasilios Magriplis', 
                                    email='test@example.com', 
                                    picture='path/to/picture')
            dal.flush()
            self.assertIsNotNone(dal.get_user(user.id))
            
    def test_create_user(self):
        with self.dal_fct() as dal:
            user = dal.create_user(name='Vasilios Magriplis', 
                                    email='test@example.com', 
                                    picture='path/to/picture')
            dal.flush()
            self.assertIsNotNone(user.id)

    def test_create_book(self):
        with self.dal_fct() as dal:
            name='Test'
            description='desc'
            weblink='testlink'

            user = dal.create_user(name='Vasilios Magriplis', 
                                    email='test@example.com', 
                                    picture='path/to/picture')
            dal.flush()
            
            bookshelf = dal.create_bookshelf(user.id)
            dal.flush()
            
            book = dal.create_book(name,
                                    bookshelf.id,
                                    description=description,
                                    weblink=weblink)
            dal.flush()
            
            book = dal.get_book(book.id)
            self.assertIsNotNone(book)
            self.assertTrue(book.bookshelf_id == bookshelf.id)
            self.assertTrue(book.description == description)
            self.assertTrue(book.web_link == weblink)

    def test_delete_book(self):
        with self.dal_fct() as dal:
            user = dal.create_user(name='Vasilios Magriplis', 
                                    email='test@example.com', 
                                    picture='path/to/picture')
            dal.flush()
            
            bookshelf = dal.create_bookshelf(user.id)
            dal.flush()
            
            book = dal.create_book('Test',
                                    bookshelf.id,
                                    description='desc',
                                    weblink='testlink')
            dal.flush()
            dal.delete_book(book.id)
            dal.flush()
            self.assertIsNone(dal.get_book(book.id))

    def test_create_bookshelf(self):
        with self.dal_fct() as dal:
            user = dal.create_user(name='Vasilios Magriplis', 
                                    email='test@example.com', 
                                    picture='path/to/picture')
            dal.flush()
            bookshelf = dal.create_bookshelf(user.id)
            dal.flush()
            bookshelf = dal.get_bookshelf_by_user(user.id)
            self.assertIsNotNone(bookshelf)
            self.assertTrue(bookshelf.user_id == user.id)

    def create_book_category(self):
        with self.dal_fct() as dal:
            name='testcategory'
            desc='desc'
            book_category = dal.create_book_category(name, desc)
            dal.flush()

            self.assertIsNotNone(book_category)
            self.assertTrue(book_category.name==name)
            self.assertTrue(book_category.description==desc)

    def test_add_category_to_book(self):
        with self.dal_fct() as dal:
            user = dal.create_user(name='Vasilios Magriplis', 
                                    email='test@example.com', 
                                    picture='path/to/picture')
            dal.flush()
            
            bookshelf = dal.create_bookshelf(user.id)
            dal.flush()
            
            book_category = dal.create_book_category('testcategory', 'desc')
            dal.flush()

            book = dal.create_book('Test',
                                    bookshelf.id,
                                    description='desc',
                                    weblink='testlink')
            dal.flush()

            book_cat_assoc = dal.add_category_to_book(book.id, book_category.id)
            self.assertIsNotNone(book_cat_assoc)
            self.assertTrue(book_cat_assoc.book_id == book.id)
            self.assertTrue(book_cat_assoc.category_id == book_category.id)


if __name__ == '__main__':
    unittest.main()
