import os

# flask configuration
DATABASE = '/tmp/server.db'
DEBUG = True
SECRET_KEY = 'my-secret-key'
USERPROFILE = 'user_profile'
PASSWORD = 'default'
JSON_AS_ASCII = False

CREDENTIALS = 'credentials'
REDIRECT_URL = 'redirect_url'
FRONTEND_PATH = 'frontend'

IS_DEVELOPMENT = os.getenv('FLASK_ENV') == 'development'

STORAGE_LOCATION = os.getenv(
    'HOME') + "/Documents/pyworkspace/storage/" if IS_DEVELOPMENT else None

BUCKET_NAME = "movlog"

CLIENT_SECRET_FILE = "client_secret.json"
SCOPES = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/devstorage.full_control',
    'openid',
    'https://www.googleapis.com/auth/calendar.events.readonly',
    'https://www.googleapis.com/auth/userinfo.profile'
]
