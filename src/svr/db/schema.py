from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import os
from pathlib import Path

Base = declarative_base()
DB_NAME = 'bookshelf.db'

class User(Base):
    __tablename__ = 'user'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name'      : self.name,
            'id'        : self.id,
            'email'     : self.email,
            'picture'   : self.picture,
       }


class Bookshelf(Base):
    __tablename__ = 'bookshelf'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable = False)
    user = relationship(User)
    
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id'        : self.id,
            'user_id'     : self.user_id,
       }


class BookCategory(Base):
    __tablename__ = 'book_category'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id'            : self.id,
            'name'          : self.name,
            'description'   : self.description,
       }

class BookCategories(Base):
    __tablename__ = 'book_categories'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('book_category.id'), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id'        : self.id,
            'book_id'     : self.bookshelf_id,
            'category_id'     : self.description,
       }


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    bookshelf_id = Column(Integer, ForeignKey('bookshelf.id'), nullable = False)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    web_link = Column(String(250))
    bookshelf = relationship(Bookshelf)
    categories = relationship(BookCategory, secondary="book_categories")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id'            : self.id,
            'bookshelf_id'  : self.bookshelf_id,
            'description'   : self.description,
            'name'          : self.name,
            'web_link'      : self.web_link,
            'categories'    : [category.serialize for category in self.categories]
       }


def setup_db(db_name=DB_NAME):
    # remove the old db file, if it exists
    db_file = Path(db_name)
    if db_file.is_file():
        os.remove(db_file)
    engine = create_engine('sqlite:///{}'.format(db_name))
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    setup_db()
