import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["FLASK_SECRET"]

# Configure allowed host names that can be served and trusted origins for Azure Container Apps.
ALLOWED_HOSTS = [".azurecontainerapps.io"] if "RUNNING_IN_PRODUCTION" in os.environ else []
CSRF_TRUSTED_ORIGINS = ["https://*.azurecontainerapps.io"] if "RUNNING_IN_PRODUCTION" in os.environ else []

# Configure database connection for Azure PostgreSQL Flexible server instance.
DBUSER = os.environ["DBUSER"]
DBPASS = os.environ["DBPASS"]
DBHOST = os.environ["DBHOST"]
DBNAME = os.environ["DBNAME"]
DATABASE_URI = f"postgresql+psycopg2://{DBUSER}:{DBPASS}@{DBHOST}/{DBNAME}"
