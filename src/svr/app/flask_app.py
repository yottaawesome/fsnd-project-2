from flask import Flask
import json

with open('secret.google_client_secrets.json') as f:
    json_secrets = json.load(f)
    GOOGLE_CLIENT_ID = json_secrets['web']['client_id']
    GOOGLE_CLIENT_SECRET = json_secrets['web']['client_secret']

with open('secret.github_client_secrets.json') as f:
    json_secrets = json.load(f)
    GITHUB_CLIENT_ID = json_secrets['client_id']
    GITHUB_CLIENT_SECRET = json_secrets['client_secret']

main_app = Flask(__name__)
