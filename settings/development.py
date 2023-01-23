from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

TIME_ZONE = 'UTC'

STATICFILES_DIRS = (str(BASE_DIR.joinpath('static')),)
STATIC_URL = 'static/'

DBUSER=os.environ['DBUSER']
DBPASS=os.environ['DBPASS']
DBHOST=os.environ['DBHOST']
DBNAME=os.environ['DBNAME']
DATABASE_URI = f'postgresql+psycopg2://{DBUSER}:{DBPASS}@{DBHOST}/{DBNAME}'
