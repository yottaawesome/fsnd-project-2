from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .schema import (
    User, Book, Bookshelf, BookCategory, 
    BookCategories, Base, DB_NAME)

PKG_DB_NAME = DB_NAME

def populate():
    engine = create_engine('sqlite:///{}'.format(PKG_DB_NAME))
    Base.metadata.bind = engine
    
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    session.add(BookCategory(name='Art', description='Books that describe, '
                            'analyse, categorise art.'))
    session.add(BookCategory(name='Autobiography', description='An account of '
                            'one\'s life.'))
    session.add(BookCategory(name='Biography', description='An account of one\'s ' 
                            'life written by another person.'))
    session.add(BookCategory(name='Book review', description='Books that review '
                            'other books.'))
    session.add(BookCategory(name='Cookbook', description='Books that are '
                            'collections of recipes.'))

    session.commit()
    session.close()

if __name__ == '__main__':
    populate()
