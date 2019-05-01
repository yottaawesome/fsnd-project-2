from db import dal_factory
from flask import (Flask, render_template, jsonify, session as login_session, request)
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
        books = dal.get_books_by_user(user.user_id)
        return jsonify(books), 200


@main_app.route('/logout/', methods=['DELETE'])
def logout():
    login_session.clear()
    return '', 204

@main_app.route('/bookshelf/', methods=['GET'])
def get_bookshelf():
    user = login_session.get('user')
    if user is None:
        return jsonify({ 'message': 'No currently logged in user' }), 401

    with dal_fct() as dal:
        bookshelf = dal.get_books_by_user(user['id'])
        if bookshelf is None:
            return jsonify([]), 200
        return jsonify([book.serialize for book in bookshelf]), 200


@main_app.route('/bookshelf/', methods=['POST'])
def new_book():
    try:

        user = login_session.get('user')
        if user is None:
            return jsonify({ 'message': 'No currently logged in user' }), 401

        json = request.get_json()
        if json is None:
            return jsonify({'message': 'Bad request'}), 400

        with dal_fct() as dal:
            bookshelf_id = dal.get_bookshelf_by_user(user['id']).id
            print(bookshelf_id)
            book = dal.create_book(
                json['name'], 
                bookshelf_id, 
                description=json['description'],
                weblink=json['weblink'])
            dal.flush()

            return jsonify(book.serialize), 200
    
    except Exception as ex:
        print('DAL operation failed: ', ex)
        return jsonify({'message': 'Operation failed'}), 500


@main_app.route('/book/<int:id>', methods=['GET'])
def get_book(id):
    try:

        user = login_session.get('user')
        if user is None:
            return jsonify({ 'message': 'No currently logged in user' }), 401

        with dal_fct() as dal:
            book = dal.get_book_by_id_and_user(id, user['id'])
            if book is None:
                return jsonify({'message': 'Book not found'}), 404

            return jsonify(book.serialize)

    except Exception as ex:
        print('DAL operation failed: ', ex)
        return jsonify({'message': 'Operation failed'}), 500


@main_app.route('/book/<int:id>', methods=['POST'])
def edit_book(id):
    try:

        user = login_session.get('user')
        if user is None:
            return jsonify({ 'message': 'No currently logged in user' }), 401
        json = request.get_json()
        if json is None:
            return jsonify({'message': 'Bad request'}), 400

        with dal_fct() as dal:
            book = dal.get_book_by_id_and_user(id, user.id)
            if book is None:
                return jsonify({'message': 'Book not found'}), 404

            dal.update_book(book.id, json['name'], json['description'], json['weblink'])

        return '', 204

    except Exception as ex:
        print('DAL operation failed: ', ex)
        return jsonify({'message': 'Operation failed'}), 500


@main_app.route('/book/<int:id>', methods=['DELETE'])
def delete_book(id):
    try:

        user = login_session.get('user')
        if user is None:
            return jsonify({ 'message': 'No currently logged in user' }), 401

        with dal_fct() as dal:
            book = dal.get_book_by_id_and_user(id, user.id)
            if book is None:
                return jsonify({'message': 'Book not found'}), 404
            dal.delete_book(book)

        return '', 204

    except Exception as ex:
        print('DAL operation failed: ', ex)
        return jsonify({'message': 'Operation failed'}), 500
