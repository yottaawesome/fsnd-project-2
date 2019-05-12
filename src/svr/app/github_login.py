'''Contains the main logic for GitHub Logins.'''

import string
import json
import requests
from flask import (
    url_for,
    request,
    redirect,
    session as login_session)
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from requests.auth import HTTPBasicAuth

from .flask_app import (
    main_app,
    GITHUB_CLIENT_ID,
    GITHUB_CLIENT_SECRET,
    doc_route)

from db import Dal, dal_factory, User
dal_fct = dal_factory()


def revoke_token(access_token):
    '''
    Revokes the GitHub token.
    '''

    url = 'https://api.github.com/applications/{}/tokens/{}'.format(
        GITHUB_CLIENT_ID,
        access_token)
    # Don't put the Authorization header in manually with manual base64
    # encoding via base64 lib, it doesn't seem to work.
    response = requests.delete(
        url,
        auth=HTTPBasicAuth(GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET))

    if response.status_code == 204:
        print("GitHub token revoked")
    else:
        print('Revocation failed: {} {}'.format(
            response.status_code, response.text))


# Code adapted from:
# https://developer.github.com/v3/guides/basics-of-authentication/
# GitHub endpoints: https://developer.github.com/apps/building-github-apps/identifying-and-authorizing-users-for-github-apps/ # noqa
@main_app.route('/githubcallback/')
def github_callback():
    # We don't need to verify the state token, because the endpoint is invoked
    # directly by GitHub, bypassing the client.
    if GITHUB_CLIENT_ID is None:
        return '', 401

    # Temporary GitHub code passed in via the querystring
    session_code = request.args.get('code')

    # Swap the the temporary code for an access token
    url = 'https://github.com/login/oauth/access_token'
    data = {
        'client_id': GITHUB_CLIENT_ID,
        'client_secret': GITHUB_CLIENT_SECRET,
        'code': session_code
    }
    headers = {'accept': 'application/json'}
    access_token_response = requests.post(url, data=data, headers=headers)

    if access_token_response.status_code != 200:
        raise Exception('Token flow failed with status code {}'
                        .format(access_token_response.status_code))

    access_token = access_token_response.json()['access_token']

    url = 'https://api.github.com/user'
    # As per https://developer.github.com/v3/, GitHub recommends putting the
    # token into the headers as opposed to in the query string, as
    # "URLs can be logged by any system along the request path".
    headers = {'Authorization': 'token {}'.format(access_token)}
    user_details_response = requests.get(url, headers=headers)
    user_details_data = user_details_response.json()

    with dal_fct() as dal:
        user_record = dal.get_user_by_email(user_details_data['email'])
        if(user_record is None):
            user_record = dal.create_user(
                                    user_details_data['name'],
                                    user_details_data['email'],
                                    user_details_data['avatar_url'])
            dal.flush()
        else:
            user_record.picture = user_details_data['avatar_url']
            dal.update_user(user_record)

        login_session['user'] = user_record.serialize
        # the bookshelf must also exist
        if dal.get_bookshelf_by_user(user_record.id) is None:
            dal.create_bookshelf(user_record.id)

    # Once we have the user's details, we don't actually need the token
    # anymore, so let's just immediately revoke it.
    revoke_token(access_token)

    return redirect(url_for("home"), code=303)
