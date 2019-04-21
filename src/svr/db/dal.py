from .schema import (User, Book, BookCategories,
                    BookCategory, Bookshelf, DB_NAME, Base)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def dal_factory(db_name=DB_NAME):
    engine = create_engine('sqlite:///{}'.format(db_name))
    Base.metadata.bind=engine
    DBSession = sessionmaker(bind = engine)
    return lambda: Dal(DBSession)

class Dal():

    def __init__(self, sess_fct):
        self._sess_fct = sess_fct
        self._session = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close(type is not None)

    def open(self):
        if self._session is None:
            self._session = self._sess_fct()

    def close(self, rollback=False):
        if self._session:
            try:
                if rollback:
                    self._session.rollback()
                else:
                    self._session.commit()

            finally:
                self._session.close()
                self._session = None

    def flush(self):
        self._session.flush()

    def get_book(self, id: int):
        return (self
            ._session
            .query(Book)
            .filter_by(id=id)
            .first())

    def create_book(self, name, bookshelf_id, description=None, weblink=None):
        book = Book(name=name,
                    bookshelf_id=bookshelf_id,
                    description=description,
                    web_link=weblink)
        self._session.add(book)
        return book

    def delete_book(self, id: int):
        (self
            ._session
            .query(BookCategories)
            .filter_by(book_id=id)
            .delete())
        (self
            ._session
            .query(Book)
            .filter_by(id=id)
            .delete())

    def create_bookshelf(self, user_id):
        bookshelf = Bookshelf(user_id=user_id)
        self._session.add(bookshelf)
        return bookshelf

    def get_books_by_bookshelf(self, bookshelf_id: int):
        return (self
            ._session
            .query(Book)
            .filter_by(bookshelf_id=bookshelf_id)
            .all())

    def get_bookshelf_by_user(self, user_id: int):
        return (self
            ._session
            .query(Bookshelf)
            .filter_by(user_id=user_id)
            .first())

    def create_user(self, name, email, picture=None):
        user = User(name=name, email=email, picture=picture)
        self._session.add(user)
        return user

    def get_user(self, user_id: int):
        return (self
            ._session
            .query(User)
            .filter_by(id=user_id)
            .first())

    def create_book_category(self, name, description):
        book_category = BookCategory(name=name, description=description)
        self._session.add(book_category)
        return book_category

    def add_category_to_book(self, book_id, category_id):
        book_category = BookCategories(book_id=book_id, 
                                        category_id=category_id)
        self._session.add(book_category)
        return book_category

    def delete_category_from_book(self, book_id, category_id):
        (self
            ._session
            .query(BookCategories)
            .filter_by(book_id=book_id,category_id=category_id)
            .delete())

    def delete_book_category(self, id):
        (self
            ._session
            .query(BookCategories)
            .filter_by(id=id)
            .delete())
