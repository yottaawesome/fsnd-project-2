from flask import (Flask, render_template, url_for, 
                    request, redirect, flash, jsonify,
                    session as login_session, make_response)

from .flask_app import main_app
from db import Dal, dal_factory

dal_fct = dal_factory()

@main_app.route('/')
def home():
    with dal_fct() as dal:
        dal.get_user(1)
    return render_template('index.html')

@main_app.route('/bookshelf/<int:id>')
def get_bookshelf(id):
    pass

@main_app.route('/book/<int:id>')
def get_book(id):
    pass

@main_app.route('/book/<int:id>/new', methods=['POST'])
def new_book(id):
    pass

@main_app.route('/book/<int:id>/edit', methods=['POST'])
def edit_book():
    pass

@main_app.route('/book/<int:id>/delete', methods=['POST'])
def delete_book():
    pass
