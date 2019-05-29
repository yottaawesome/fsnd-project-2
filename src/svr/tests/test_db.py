'''Contains the functional test cases for the DAL.'''
import context
from svr.db import Dal, populate, dal_factory
import unittest
import svr.db
import os
from pathlib import Path

DB_NAME = 'test.db'
CONNECTION_STRING = 'sqlite:///{}'.format(DB_NAME)


class TestDal(unittest.TestCase):
    def setUp(self):
        svr.db.schema.setup_db(CONNECTION_STRING)
        populate(CONNECTION_STRING)
        self.dal_fct = dal_factory(CONNECTION_STRING)

    def tearDown(self):
        db_file = Path(DB_NAME)
        if db_file.is_file():
            os.remove(db_file)

    def test_get_user(self):
        with self.dal_fct() as dal:
            user = dal.create_user(
                name='Vasilios Magriplis',
                email='test@example.com',
                picture='path/to/picture')
            dal.flush()
            self.assertIsNotNone(dal.get_user(user.id))

    def test_create_user(self):
        with self.dal_fct() as dal:
            user = dal.create_user(
                name='Vasilios Magriplis',
                email='test@example.com',
                picture='path/to/picture')
            dal.flush()
            self.assertIsNotNone(user.id)

    def test_create_book(self):
        with self.dal_fct() as dal:
            name = 'Test'
            description = 'desc'
            weblink = 'testlink'

            user = dal.create_user(
                name='Vasilios Magriplis',
                email='test@example.com',
                picture='path/to/picture')
            dal.flush()

            book_category = dal.create_book_category('testcategory', 'desc')
            dal.flush()

            bookshelf = dal.create_bookshelf(user.id)
            dal.flush()

            book = dal.create_book(
                name,
                bookshelf.id,
                description=description,
                weblink=weblink,
                categories=[book_category.id])
            dal.flush()

            book = dal.get_book(book.id)
            self.assertIsNotNone(book)
            self.assertTrue(book.bookshelf_id == bookshelf.id)
            self.assertTrue(book.description == description)
            self.assertTrue(book.web_link == weblink)
            self.assertTrue(book.categories[0].id == book_category.id)

    def test_get_book_by_id_and_user(self):
        with self.dal_fct() as dal:
            user = dal.create_user(
                name='Vasilios Magriplis',
                email='test@example.com',
                picture='path/to/picture')
            dal.flush()

            bookshelf = dal.create_bookshelf(user.id)
            dal.flush()

            book = dal.create_book(
                'Test',
                bookshelf.id,
                description='desc',
                weblink='testlink')
            dal.flush()
            book = dal.get_book_by_id_and_user(book.id, user.id)

            self.assertIsNotNone(book)
            self.assertTrue(book.bookshelf_id == bookshelf.id)
            self.assertTrue(bookshelf.user_id == user.id)

    def test_update_book(self):
        with self.dal_fct() as dal:
            user = dal.create_user(
                name='Vasilios Magriplis',
                email='test@example.com',
                picture='path/to/picture')
            dal.flush()

            bookshelf = dal.create_bookshelf(user.id)
            book_category = dal.create_book_category('testcategory', 'desc')
            dal.flush()

            book = dal.create_book(
                'Test',
                bookshelf.id,
                description='desc',
                weblink='testlink',
                categories=[book_category.id])
            dal.flush()

            book_category2 = dal.create_book_category('testcategory2', 'desc2')
            dal.flush()

            name = 'Test2'
            desc = 'desc2'
            weblink = 'testlink2'
            dal.update_book(book.id, name, desc, weblink, [book_category2.id])
            dal.flush()

            book = dal.get_book(book.id)

            self.assertTrue(book.name == name)
            self.assertTrue(book.description == desc)
            self.assertTrue(book.web_link == weblink)
            self.assertTrue(book.categories[0].id == book_category2.id)

    def test_delete_book(self):
        with self.dal_fct() as dal:
            user = dal.create_user(
                name='Vasilios Magriplis',
                email='test@example.com',
                picture='path/to/picture')
            dal.flush()

            bookshelf = dal.create_bookshelf(user.id)
            dal.flush()

            book = dal.create_book(
                'Test',
                bookshelf.id,
                description='desc',
                weblink='testlink')

            dal.flush()
            dal.delete_book(book.id)
            dal.flush()
            self.assertIsNone(dal.get_book(book.id))

    def test_create_bookshelf(self):
        with self.dal_fct() as dal:
            user = dal.create_user(
                name='Vasilios Magriplis',
                email='test@example.com',
                picture='path/to/picture')
            dal.flush()

            bookshelf = dal.create_bookshelf(user.id)
            dal.flush()
            bookshelf = dal.get_bookshelf_by_user(user.id)
            self.assertIsNotNone(bookshelf)
            self.assertTrue(bookshelf.user_id == user.id)

    def test_create_book_category(self):
        with self.dal_fct() as dal:
            name = 'testcategory'
            desc = 'desc'
            book_category = dal.create_book_category(name, desc)
            dal.flush()

            self.assertIsNotNone(book_category)
            self.assertTrue(book_category.name == name)
            self.assertTrue(book_category.description == desc)

    def test_get_books_by_user(self):
        with self.dal_fct() as dal:
            user = dal.create_user(
                name='Vasilios Magriplis',
                email='test@example.com',
                picture='path/to/picture')
            dal.flush()

            bookshelf = dal.create_bookshelf(user.id)
            dal.flush()

            book = dal.create_book(
                'Test',
                bookshelf.id,
                description='desc',
                weblink='testlink')
            dal.flush()

            books = dal.get_books_by_user(user.id)
            self.assertIsNotNone(books)
            self.assertTrue(len(books) > 0)
            self.assertTrue(books[0].id == book.id)

    def test_add_category_to_book(self):
        with self.dal_fct() as dal:
            user = dal.create_user(
                name='Vasilios Magriplis',
                email='test@example.com',
                picture='path/to/picture')
            dal.flush()

            bookshelf = dal.create_bookshelf(user.id)
            dal.flush()

            book_category = dal.create_book_category('testcategory', 'desc')
            book_category2 = dal.create_book_category('testcategory2', 'desc2')
            dal.flush()

            book = dal.create_book(
                'Test',
                bookshelf.id,
                description='desc',
                weblink='testlink')
            dal.flush()

            dal.add_category_to_book(book.id, book_category.id)
            dal.add_category_to_book(book.id, book_category2.id)
            book = dal.get_book(book.id)

            self.assertTrue(book.categories[0].id == book_category.id)
            self.assertTrue(book.categories[1].id == book_category2.id)

    def test_get_categories(self):
        with self.dal_fct() as dal:
            dal.create_book_category('testcategory', 'desc')
            dal.flush()

            categories = dal.get_categories()
            self.assertTrue(len(categories) > 0)


if __name__ == '__main__':
    unittest.main()
