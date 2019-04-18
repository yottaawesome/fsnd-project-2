from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import (
    User, Book, Bookshelf, BookCategory, 
    BookCategories, Base, DB_NAME)
 
engine = create_engine('sqlite:///{}'.format(DB_NAME))
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()

session.commit()
session.close()
