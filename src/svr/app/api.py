'''Contains the main routes for the REST API.'''

from db import dal_factory
from flask import render_template, jsonify, session as login_session, request
from .flask_app import (
    main_app,
    GITHUB_CLIENT_ID,
    GOOGLE_CLIENT_ID,
    doc_route,
    API_DOC)
import random
import string

dal_fct = dal_factory()


@main_app.route('/api/v1/docs/')
def docs():
    '''Serializes the docs collection into JSON for client consumption'''

    return jsonify(API_DOC), 200


@main_app.route('/')
def home():
    ''' Base route. '''

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state

    return render_template(
                            'index.html',
                            google_client_id=GOOGLE_CLIENT_ID,
                            github_client_id=GITHUB_CLIENT_ID,
                            page_state=state)


@doc_route('/api/v1/authproviders/')
def get_auth_providers():
    '''
    Gets the supported authentication providers as a list. This list will
    be either ['google'] or ['google','github'].

    Returns:
        200 and a list of supported third-party authentication providers.
    '''

    auths = ['google']
    if GITHUB_CLIENT_ID:
        auths.append('github')
    return jsonify(auths), 200


@doc_route('/api/v1/user/')
def user():
    '''
    Gets the current user's details.

    Returns:
        200 and the user's details as JSON.
        215 if no user is currently logged in.
    '''

    try:

        user = login_session.get('user')
        if user is None:
            return jsonify({'message': 'No currently logged in user'}), 215

        return jsonify(user)

    except Exception as ex:

        print('Exception: ', ex)
        return jsonify({'message': 'Fetching user details failed'}), 500


@doc_route('/api/v1/user/', methods=['DELETE'])
def logout():
    '''
    Logs the current user out.

    Returns:
        204.
    '''

    try:

        # preserve the state
        state = login_session.get('state')
        login_session.clear()
        login_session['state'] = state
        return '', 204

    except Exception as ex:

        print('Exception: ', ex)
        return jsonify({'message': 'Logging out failed'}), 500


@doc_route('/api/v1/bookshelf/', methods=['GET'])
def get_bookshelf():
    '''
    Gets all the books for the user's bookshelf as JSON.

    Returns:
        200 and the bookshelf books in JSON format.
        401 if the user is not authenticated.
        404 if the book does not exist.
        500 if an unexpected error.
    '''

    try:

        user = login_session.get('user')
        if user is None:
            return jsonify({'message': 'No currently logged in user'}), 401

        with dal_fct() as dal:
            bookshelf = dal.get_books_by_user(user['id'])
            if bookshelf is None:
                return jsonify([]), 200

            return jsonify([book.serialize for book in bookshelf]), 200

    except Exception as ex:

        print('Exception: ', ex)
        return jsonify({'message': 'Retrieving books failed'}), 500


@doc_route('/api/v1/bookshelf/sorted/', methods=['GET'])
def get_sorted_bookshelf():
    '''
    Gets all the books sorted by category for the user's bookshelf as JSON.

    Returns:
        200 and the bookshelf books in JSON format.
        401 if the user is not authenticated.
        404 if the book does not exist.
        500 if an unexpected error.
    '''

    try:

        user = login_session.get('user')
        if user is None:
            return jsonify({'message': 'No currently logged in user'}), 401

        with dal_fct() as dal:
            bookshelf = dal.get_books_by_user(user['id'])
            result = {}
            if bookshelf is None:
                return jsonify([]), 200

            for book in bookshelf:
                for category in book.categories:
                    if(result.get(category.name) is None):
                        result[category.name] = {
                            'books': []
                        }
                        # merge the dict with category dict
                        result[category.name] = {
                            **result[category.name],
                            **category.serialize
                        }
                    result[category.name]['books'].append(book.serialize)

            result = {
                'totalBooks': len(bookshelf),
                'categories': list(result.values())
            }
            return jsonify(result), 200

    except Exception as ex:

        print('Exception: ', ex)
        return jsonify({'message': 'Retrieving books failed'}), 500


@doc_route('/api/v1/bookshelf/', methods=['POST'])
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
            return jsonify({'message': 'No currently logged in user'}), 401

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
                weblink=json['web_link'],
                categories=json['categories'],
                author=json['author'],
                publisher=json['publisher']
            )
            dal.flush()

            return jsonify(book.serialize), 200

    except Exception as ex:

        print('Exception: ', ex)
        return jsonify({'message': 'Creating a new book failed'}), 500


@doc_route('/api/v1/book/<int:id>', methods=['GET'])
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
            return jsonify({'message': 'No currently logged in user'}), 401

        with dal_fct() as dal:
            book = dal.get_book_by_id_and_user(id, user['id'])
            if book is None:
                return jsonify({'message': 'Book not found'}), 404

            return jsonify(book.serialize)

    except Exception as ex:

        print('Exception: ', ex)
        return jsonify({'message': 'Fetching book failed'}), 500


@doc_route('/api/v1/book/<int:id>', methods=['POST'])
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
            return jsonify({'message': 'No currently logged in user'}), 401
        json = request.get_json()
        if json is None:
            return jsonify({'message': 'Bad request'}), 400

        with dal_fct() as dal:
            book = dal.get_book_by_id_and_user(id, user['id'])
            if book is None:
                return jsonify({'message': 'Book not found'}), 404

            book = dal.update_book(
                book.id, json['name'],
                json['description'],
                json['web_link'],
                json['categories'],
                json['author'],
                json['publisher']
            )

            return jsonify(book.serialize), 200

    except Exception as ex:
        print('Exception: ', ex)
        return jsonify({'message': 'Editing book failed'}), 500


@doc_route('/api/v1/book/<int:id>', methods=['DELETE'])
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
            return jsonify({'message': 'No currently logged in user'}), 401

        with dal_fct() as dal:
            book = dal.get_book_by_id_and_user(id, user['id'])
            if book is None:
                return jsonify({'message': 'Book not found'}), 404
            dal.delete_book(book.id)

        return '', 204

    except Exception as ex:

        print('Exception: ', ex)
        return jsonify({'message': 'Deleting a book failed'}), 500


@doc_route('/api/v1/categories/', methods=['GET'])
def get_categories():
    '''
    Gets all book categories.

    Returns:
        200.
        500 if an unexpected error occurs.
    '''

    try:

        with dal_fct() as dal:
            result = [cat.serialize for cat in dal.get_categories()]
            return jsonify(result), 200

    except Exception as ex:

        print('Exception: ', ex)
        return jsonify({'message': 'Fetching categories failed'}), 500
