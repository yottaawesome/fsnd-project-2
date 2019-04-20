from flask import (Flask, render_template, url_for, 
                    request, redirect, flash, jsonify)
from db import Dal

# Flask
app = Flask(__name__)

@app.route('/')
def home():
    with Dal() as x:
        x.get_user(1)
    return render_template('index.html')

@app.route('/bookshelf/<int:id>')
def view_bookshelf(id):
    pass

@app.route('/book/<int:id>')
def view_book(id):
    pass

@app.route('/book/<int:id>/new', methods=['POST'])
def new_book(id):
    pass

@app.route('/book/<int:id>/edit', methods=['POST'])
def edit_book():
    pass

@app.route('/book/<int:id>/delete', methods=['POST'])
def delete_book():
    pass

if __name__ == '__main__':
    app.debug = True
    app.run(host = '127.0.0.1', port = 5000)
