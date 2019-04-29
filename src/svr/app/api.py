from db import Dal, dal_factory
from flask import (Flask, render_template, url_for, 
                    request, redirect, flash, jsonify, Response,
                    session as login_session, make_response)
from .flask_app import (main_app, GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, 
                        GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
import base64, requests

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

@main_app.route('/logout/', methods=['DELETE'])
def logout():
    login_session.clear()
    return '', 204

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

@main_app.route('/test')
def test_fetch():
    return jsonify({ 'cool':'super'}), 200
