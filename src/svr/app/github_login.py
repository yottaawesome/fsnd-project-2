from flask import (Flask, render_template, url_for, 
                    request, redirect, flash, jsonify,
                    session as login_session, make_response)
                    
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import random, string, httplib2, json, requests

from db import Dal, dal_factory
dal_fct = dal_factory()

from .flask_app import main_app, GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET

# Code adapted from https://developer.github.com/v3/guides/basics-of-authentication/
# GitHub endpoints: https://developer.github.com/apps/building-github-apps/identifying-and-authorizing-users-for-github-apps/
@main_app.route('/githubcallback/')
def github_callback():
    # this is the temporary GitHub code passed in via the querystring
    session_code = request.args.get('code')
    
    # swap the the temportary code for an access token
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

    #with dal_fct() as dal:
    #    dal.get_user()
    
    """
    relevant fields:
        id?
        name
        email
        avatar_url
    """
