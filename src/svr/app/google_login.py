'''Contains the main logic for Google Logins.'''

from .flask_app import main_app, GOOGLE_CLIENT_ID
from flask import request, jsonify, session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from db import Dal, dal_factory
from cfg import GOOGLE_SECRETS_FILE
import json
import requests

dal_fct = dal_factory()


def revoke_token(access_token):
    '''
    Revokes the Google token.
    '''

    response = requests.post(
        'https://accounts.google.com/o/oauth2/revoke',
        params={'token': access_token},
        headers={'content-type': 'application/x-www-form-urlencoded'})

    if response.status_code == 200:
        print('Token successfully revoked')
    else:
        print('Token revocation failed with status {}'.format(
            response.status_code))


@main_app.route('/api/v1/googleauth/', methods=['POST'])
def google_auth():
    '''
    Authenticates to Google using the temporary client code. This endpoint
    is not intended for general public use.
    '''

    # Validate state token
    json_req = request.get_json()
    login_session_state = login_session.get('state')
    if login_session_state is None or json_req['state'] != login_session_state:
        return jsonify('Invalid state parameter'), 401

    # Obtain authorization code
    code = json_req['code']

    try:

        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(
            GOOGLE_SECRETS_FILE, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)

    except FlowExchangeError as ex:

        print(ex)
        return jsonify(
            {'message': 'Failed to upgrade the authorization code.'}), 401

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'
        .format(access_token))
    check_json = requests.get(url).json()
    # If there was an error in the access token info, abort.
    if check_json.get('error') is not None:
        return jsonify({'message': check_json.get('error')}), 500

    """ https://www.googleapis.com/oauth2/v1/tokeninfo
    {
        "issued_to": <app client id>,
        "audience": <app client id>,
        "user_id": <user id>,
        "scope": "openid https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email", # noqa
        "expires_in": <seconds to expiry>,
        "email": "<user email>",
        "verified_email": true,
        "access_type": "offline"
    }
    """

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if check_json['user_id'] != gplus_id:
        return jsonify(
            {'message': 'Token\'s user ID doesn\'t match given user ID.'}), 401

    # Verify that the access token is valid for this app.
    if check_json['issued_to'] != GOOGLE_CLIENT_ID:
        return jsonify(
            {'message': 'Token\'s client ID does not match app\'s'}), 401

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    user_details_data = answer.json()

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

    with dal_fct() as dal:
        user_record = dal.get_user_by_email(user_details_data['email'])
        if(user_record is None):
            user_record = dal.create_user(
                                user_details_data['name'],
                                user_details_data['email'],
                                user_details_data['avatar_url'])
            dal.flush()
        else:
            user_record.picture = user_details_data['picture']
            dal.update_user(user_record)

        login_session['user'] = user_record.serialize
        # the bookshelf must also exist
        if dal.get_bookshelf_by_user(user_record.id) is None:
            dal.create_bookshelf(user_record.id)

    revoke_token(access_token)

    return jsonify(login_session['user']), 200
