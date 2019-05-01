'''Contains the main routes for the REST API.'''
from db import dal_factory
from flask import (Flask, render_template, jsonify, session as login_session, request)
from .flask_app import (main_app, GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, 
                        GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)

dal_fct = dal_factory()

@main_app.route('/')
def home():
    '''
    Base route.
    '''
    return render_template('index.html', google_client_id=GOOGLE_CLIENT_ID,
                            github_client_id=GITHUB_CLIENT_ID)


@main_app.route('/user/')
def user():
    '''
    Gets the current user's details.

    Returns:
        200 and the user's details as JSON.
        215 if no user is currently logged.
    '''

    user = login_session.get('user')
    if user is None:
        return jsonify({ 'message': 'No currently logged in user' }), 215

    return jsonify(user)


@main_app.route('/logout/', methods=['DELETE'])
def logout():
    '''
    Logs the current user out.

    Returns:
        204. 
    '''

    login_session.clear()
    return '', 204

@main_app.route('/bookshelf/', methods=['GET'])
def get_bookshelf():
    '''
    Gets all the books for the user's bookshelf as JSON.

    Returns:
        200 and the bookshelf books in JSON format. 
        401 if the user is not authenticated.
        404 if the book does not exist. 
        500 if an unexpected error.
    '''

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
    '''
    Creates a new book in the user's bookshelf.

    Returns:
        200 and the created book in JSON format. 
        401 if the user is not authenticated.
        400 for a malformed request.
        404 if the book does not exist.
        500 if an unexpected error.
    '''

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
                weblink=json['web_link'])
            dal.flush()

            return jsonify(book.serialize), 200
    
    except Exception as ex:
        print('DAL operation failed: ', ex)
        return jsonify({'message': 'Operation failed'}), 500


@main_app.route('/book/<int:id>', methods=['GET'])
def get_book(id):
    '''
    Gets the book identified by the id segment of the URI as JSON.

    Returns:
        200 and the book in JSON format. 
        401 if the user is not authenticated.
        404 if the book does not exist. 
        500 if unexpected error occurs.
    '''

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
    '''
    Updates the book identified by the id segment of the URI.

    Returns:
        200 and the updated book in JSON format. 
        400 for a malformed request.
        401 if the user is not authenticated.
        404 if the book does not exist. 
        500 if an unexpected error occurs.
    '''

    try:

        user = login_session.get('user')
        if user is None:
            return jsonify({ 'message': 'No currently logged in user' }), 401
        json = request.get_json()
        if json is None:
            return jsonify({'message': 'Bad request'}), 400

        with dal_fct() as dal:
            book = dal.get_book_by_id_and_user(id, user['id'])
            if book is None:
                return jsonify({'message': 'Book not found'}), 404

            book = dal.update_book(book.id, json['name'], json['description'], json['web_link'])

            return jsonify(book.serialize), 200

    except Exception as ex:
        print('DAL operation failed: ', ex)
        return jsonify({'message': 'Operation failed'}), 500


@main_app.route('/book/<int:id>', methods=['DELETE'])
def delete_book(id):
    '''
    Deletes the book identified by the id segment of the URI.

    Returns:
        204 if the book was successfully deleted.
        401 if the user is not authenticated.
        404 if the book does not exist. 
        500 if an unexpected error occurs.
    '''
    try:

        user = login_session.get('user')
        if user is None:
            return jsonify({ 'message': 'No currently logged in user' }), 401

        with dal_fct() as dal:
            book = dal.get_book_by_id_and_user(id, user['id'])
            if book is None:
                return jsonify({'message': 'Book not found'}), 404
            dal.delete_book(book.id)

        return '', 204

    except Exception as ex:
        print('DAL operation failed: ', ex)
        return jsonify({'message': 'Operation failed'}), 500
