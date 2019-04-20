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
        self.sess_fct = sess_fct
        self.session = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close(type is not None)

    def open(self):
        if self.session is None:
            self.session = self.sess_fct()

    def close(self, rollback=False):
        if self.session:
            try:
                if rollback:
                    self.session.rollback()
                else:
                    self.session.commit()
            finally:
                self.session.close()

    def flush(self):
        self.session.flush()

    def create_book(self, name, bookshelf_id, description=None, weblink=None):
        book = Book(name=name,
                    bookshelf_id=bookshelf_id,
                    description=None,web_link=weblink)
        self.session.add(book)
        return book

    def get_book(self, id: int):
        return (self
            .session
            .query(Book)
            .filter_by(id=id)
            .first())

    def delete_book(self, id: int):
        (self
            .session
            .query(Book)
            .filter_by(id=id)
            .delete())

    def get_books_by_bookshelf(self, bookshelf_id: int):
        return (self
            .session
            .query(Book)
            .filter_by(bookshelf_id=bookshelf_id)
            .all())

    def create_bookshelf(self, user_id):
        bookshelf = Bookshelf(user_id=user_id)
        self.session.add(bookshelf)
        return bookshelf

    def create_user(self, name, email, picture):
        user = User(name=name, email=email, picture=picture)
        self.session.add(user)
        return user

    def get_user(self, user_id: int):
        return (self
            .session
            .query(User)
            .filter_by(id=user_id)
            .first())

    def get_bookshelf_by_user(self, user_id: int):
        return (self
            .session
            .query(Bookshelf)
            .filter_by(user_id=user_id)
            .first())
