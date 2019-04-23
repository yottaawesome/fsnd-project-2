from flask import (Flask, render_template, url_for, 
                    request, redirect, flash, jsonify,
                    session as login_session, make_response)
                    
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import random, string, httplib2, json, requests

from db import Dal, dal_factory
dal_fct = dal_factory()

from .flask_app import main_app, GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET

#https://developer.github.com/v3/guides/basics-of-authentication/

@main_app.route('/githubcallback/')
def github_callback():
    pass
    # get temporary GitHub code...
    #session_code = request.env['rack.request.query_hash']['code']

    # ... and POST it back to GitHub
    #result = RestClient.post('https://github.com/login/oauth/access_token',
    #                      {:client_id => CLIENT_ID,
    #                       :client_secret => CLIENT_SECRET,
    #                       :code => session_code},
    #                       :accept => :json)

    # extract the token and granted scopes
    #access_token = JSON.parse(result)['access_token']
