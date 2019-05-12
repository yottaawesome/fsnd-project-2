'''Auto-creates the database'''

from db import setup_db, populate
setup_db('bookshelf.db')
populate('bookshelf.db')
