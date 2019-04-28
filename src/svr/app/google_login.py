from flask import (Flask, render_template, url_for, 
                    request, redirect, flash, jsonify,
                    session as login_session, make_response)
                    
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import random, string, httplib2, json, requests

from db import Dal, dal_factory
dal_fct = dal_factory()

from .flask_app import main_app, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

def revoke_token(access_token):
    response = requests.post('https://accounts.google.com/o/oauth2/revoke',
        params={'token': access_token},
    headers = {'content-type': 'application/x-www-form-urlencoded'})
    if response.status_code == 200:
        print('Token successfully revoked')
    else:
        print('Token revocation failed with status {}'.format(response.status_code))

def clear_session():
    del login_session['access_token']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']

def check_token_status(access_token):
    response = requests.get(
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}', 
        params={'token': access_token})
    return response.status_code == 200

@main_app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(
            'secret.google_client_secrets.json',
            scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'
            .format(access_token))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    """ https://www.googleapis.com/oauth2/v1/tokeninfo
    {
        "issued_to": <app client id>,
        "audience": <app client id>,
        "user_id": <user id>,
        "scope": "openid https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email",
        "expires_in": <seconds to expiry>,
        "email": "<user email>",
        "verified_email": true,
        "access_type": "offline"
    }
    """

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != GOOGLE_CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        print('Current token: {}'.format(stored_access_token))
        print('New token: {}'.format(credentials.access_token))
        revoke_token(login_session['access_token'])
        login_session['access_token'] = credentials.access_token
        response = make_response(json.dumps('Current user is already connected.'),
                                200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    login_session['token_expiry'] = credentials.token_expiry

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    """
    https://www.googleapis.com/oauth2/v1/userinfo
    {
        "id": <numeric id as string>,
        "email": <email>,
        "verified_email": true,
        "name": "Vasilios Magriplis",
        "given_name": "Vasilios",
        "family_name": "Magriplis",
        "picture": <user content picture path>,
        "locale": "en-GB"
    }
    """

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    login_session['user'] = {
        'uid': data['id'],
        'name': data['name'],
        'email': data['email'],
        'picture': data['picture']
    }

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output

@main_app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    revoke_token(login_session['access_token'])
    clear_session()
    response = make_response(json.dumps('Successfully disconnected.'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
