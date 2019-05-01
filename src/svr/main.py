'''Runs the web application.'''
from app import main_app
import os

if __name__ == '__main__':
    main_app.debug = True
    main_app.secret_key = os.urandom(24)
    main_app.run(host = '127.0.0.1', port = 5000)
