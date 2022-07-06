import json
from O365 import Account, FileSystemTokenBackend

creds = json.load(open('credentials.json', 'r'))

credentials = (
    creds['application_key'], 
    creds['secret_key']
)

scopes = ['https://graph.microsoft.com/Calendars.ReadWrite']

token_backend = FileSystemTokenBackend(token_path='auth', token_filename='o365_token.txt')
account = Account(credentials, token_backend=token_backend, main_resource=creds['user_email'], scopes=scopes, tenant_id=creds['tenant_id'])
account.authenticate()