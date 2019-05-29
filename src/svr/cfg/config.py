import os
import json

current_file_path = __file__
current_file_dir = os.path.dirname(__file__)
cfg_file_path = os.path.join(current_file_dir, 'secret.cfg.json')

with open(cfg_file_path) as cfg_file:
    CFG = json.load(cfg_file)

SECRET_KEY = CFG['secret_key']
GOOGLE_SECRETS_FILE = CFG['google_secrets_file']
GITHUB_SECRETS_FILE = CFG['github_secrets_file']
CONNECTION_STRING = CFG['conn_string']
