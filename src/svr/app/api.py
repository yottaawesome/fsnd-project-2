from db import dal_factory
from flask import (Flask, render_template, jsonify, session as login_session)
from .flask_app import (main_app, GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, 
                        GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)

dal_fct = dal_factory()

@main_app.route('/')
def home():
    return render_template('index.html', google_client_id=GOOGLE_CLIENT_ID,
                            github_client_id=GITHUB_CLIENT_ID)


@main_app.route('/user/')
def user():
    user = login_session.get('user')
    if user is None:
        return jsonify({ 'message': 'No currently logged in user' }), 215

    return jsonify(user)


@main_app.route('/user/books')
def get_books_by_user():
    user = login_session.get('user')
    if user is None:
        return jsonify({ 'message': 'No currently logged in user' }), 215
    
    with dal_fct() as dal:
        return dal.get_books_by_user(user.user_id)


@main_app.route('/logout/', methods=['DELETE'])
def logout():
    login_session.clear()
    return '', 204


@main_app.route('/bookshelf/<int:id>')
def get_bookshelf(id):
    user = login_session.get('user')
    if user is None:
        return jsonify({ 'message': 'No currently logged in user' }), 401

    with dal_fct() as dal:
        return dal.get_bookshelf_by_user(user.user_id)


@main_app.route('/bookshelf/<int:id>/', methods=['POST'])
def new_book(id):
    user = login_session.get('user')
    if user is None:
        return jsonify({ 'message': 'No currently logged in user' }), 401

    pass


@main_app.route('/book/<int:id>', methods=['GET'])
def get_book(id):
    pass


@main_app.route('/book/<int:id>', methods=['POST'])
def edit_book():
    pass


@main_app.route('/book/<int:id>', methods=['DELETE'])
def delete_book():
    pass
