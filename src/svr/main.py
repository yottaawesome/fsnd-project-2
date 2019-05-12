'''Runs the web application.'''

import os
from app import main_app

if __name__ == '__main__':
    main_app.debug = True
    main_app.secret_key = os.urandom(24)
    main_app.run(host='0.0.0.0', port=5000)
