'''Runs the web application.'''

import os
from app import main_app

app = main_app

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
