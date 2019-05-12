from flask import Flask
import json
from pathlib import Path

with open('secret.google_client_secrets.json') as f:
    json_secrets = json.load(f)
    GOOGLE_CLIENT_ID = json_secrets['web']['client_id']
    GOOGLE_CLIENT_SECRET = json_secrets['web']['client_secret']

GITHUB_CLIENT_ID = None
GITHUB_CLIENT_SECRET = None
github_file = Path('secret.github_client_secrets.json')
if github_file.is_file():
    with github_file.open() as f:
        json_secrets = json.load(f)
        GITHUB_CLIENT_ID = json_secrets['client_id']
        GITHUB_CLIENT_SECRET = json_secrets['client_secret']

main_app = Flask(__name__)

API_DOC = []


def doc_route(rule, **options):
    def decorator(f):
        endpoint = options.pop("endpoint", None)
        main_app.add_url_rule(rule, endpoint, f, **options)
        methods = options.get("methods")
        if methods is None or len(methods) == 0:
            methods = ['GET']

        route = None
        for r in API_DOC:
            if r['route'] == rule:
                route = r
                break

        if route is None:
            route = {
                'methods': [],
                'route': rule
            }
            API_DOC.append(route)

        doc_string = f.__doc__ or 'No documentation found'

        for method in methods:
            route['methods'].append({
                'description': doc_string,
                'method': method
            })

        return f
    return decorator
