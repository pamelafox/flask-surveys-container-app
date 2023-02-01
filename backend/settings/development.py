import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

TIME_ZONE = "UTC"

STATICFILES_DIRS = (str(BASE_DIR.joinpath("static")),)
STATIC_URL = "static/"

SECRET_KEY = os.environ.get("FLASKSECRET", "flask-insecure-7ppocbnx@w71dcuinn*t^_mzal(t@o01v3fee27g%rg18fc5d@")

DBUSER = os.environ["DBUSER"]
DBPASS = os.environ["DBPASS"]
DBHOST = os.environ["DBHOST"]
DBNAME = os.environ["DBNAME"]
DATABASE_URI = f"postgresql+psycopg2://{DBUSER}:{DBPASS}@{DBHOST}/{DBNAME}"
TEST_DATABASE_URI = f"postgresql+psycopg2://{DBUSER}:{DBPASS}@localhost/{DBNAME}"
