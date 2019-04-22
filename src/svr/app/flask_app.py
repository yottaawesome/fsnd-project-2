from flask import Flask

with open('clientid') as f:
    CLIENT_ID = f.read()
with open('clientsecret') as f:
    CLIENT_SECRET = f.read()

main_app = Flask(__name__)
