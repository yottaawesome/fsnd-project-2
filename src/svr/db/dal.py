from .schema import (User, Book, BookCategories,
                    BookCategory, Bookshelf, DB_NAME, Base)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///{}'.format(DB_NAME))
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)

class Dal():
    def __init__(self):
        pass

    def __enter__(self):
        self.session = DBSession()
        return self

    def __exit__(self, type, value, traceback):
        if type is not None:
            self.session.rollback()
        else:
            self.session.commit()

        self.session.close()

    def create_book(self, book: Book):
        pass

    def get_book(self, id: int):
        pass

    def delete_book(self, id: int):
        pass

    def get_books_by_bookshelf(self, bookshelf_id: int):
        pass

    def create_bookshelf(self, bookshelf: Bookshelf):
        pass

    def create_user(self, user: User):
        pass

    def get_user(self, user_id: int):
        pass

    def get_bookshelf_by_user(self, user_id: int):
        pass
