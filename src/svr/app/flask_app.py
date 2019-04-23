from flask import Flask

with open('secret.google_clientid') as f:
    GOOGLE_CLIENT_ID = f.read()
with open('secret.google_clientsecret') as f:
    GOOGLE_CLIENT_SECRET = f.read()
with open('secret.github_clientid') as f:
    GITHUB_CLIENT_ID = f.read()
with open('secret.github_clientsecret') as f:
    GITHUB_CLIENT_SECRET = f.read()

main_app = Flask(__name__)
