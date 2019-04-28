from flask import (Flask, render_template, url_for, 
                    request, redirect, flash, jsonify,
                    session as login_session, make_response)
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import random, string, httplib2, json, requests
import base64

from .flask_app import main_app, GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, GOOGLE_CLIENT_ID
from db import Dal, dal_factory, User
dal_fct = dal_factory()

def revoke_token():
    # returns 404
    #url = 'https://api.github.com/applications/{}/tokens/{}'.format(GITHUB_CLIENT_ID, access_token)
    #secret = base64.urlsafe_b64encode('{}:{}'.format(GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET).encode())
    #headers = { 'Authorization': 'Basic {}'.format(secret)}
    #revoke_response = requests.delete(url, headers=headers)
    
    # returns 401
    # apparently, requires the user to enter their password, which is silly
    # https://stackoverflow.com/questions/17217750/revoking-oauth-access-token-results-in-404-not-found
    #url = 'https://api.github.com/authorizations/{}'.format(access_token)
    #secret = base64.urlsafe_b64encode('{}:{}'.format(GITHUB_CLIENT_SECRET).encode())
    #headers = { 'Authorization': 'Basic {}'.format(secret)}
    #revoke_response = requests.delete(url, headers=headers)
    #if revoke_response.status_code == 204:
    #    print("Token revoked")
    #else:
    #    print(revoke_response.status_code)
    #    print(revoke_response.text)
    pass

# Code adapted from https://developer.github.com/v3/guides/basics-of-authentication/
# GitHub endpoints: https://developer.github.com/apps/building-github-apps/identifying-and-authorizing-users-for-github-apps/
@main_app.route('/githubcallback/')
def github_callback():
    # this is the temporary GitHub code passed in via the querystring
    session_code = request.args.get('code')
    
    # swap the the temporary code for an access token
    url = 'https://github.com/login/oauth/access_token'
    data = {
        'client_id': GITHUB_CLIENT_ID,
        'client_secret': GITHUB_CLIENT_SECRET,
        'code': session_code
    }
    headers = { 'accept': 'application/json' }
    access_token_response = requests.post(url, data=data, headers=headers)

    if access_token_response.status_code != 200:
        raise Exception('Token flow failed with status code {}'
                        .format(access_token_response.status_code))
        
    access_token = access_token_response.json()['access_token']
    
    url = 'https://api.github.com/user?access_token={}'.format(access_token)
    user_details_response = requests.get(url)
    user_details_data = user_details_response.json()

    with dal_fct() as dal:
        user_record = dal.get_user_by_email(user_details_data['email'])
        if(user_record is None):
            user_record = dal.create_user(
                                    user_details_data['name'],
                                    user_details_data['email'],
                                    user_details_data['avatar_url'])
            dal.flush()
        login_session['user'] = user_record.serialize

    return redirect(url_for("home"), code=303)
