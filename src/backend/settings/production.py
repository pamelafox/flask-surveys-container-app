import os

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def get_secret(secret_name):
    if key_vault_name := os.environ.get("KEY_VAULT_NAME"):
        key_vault_uri = f"https://{key_vault_name}.vault.azure.net"
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=key_vault_uri, credential=credential)
        return client.get_secret(secret_name).value
    raise RuntimeError("KEY_VAULT_NAME not set.")


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("FLASKSECRET")

# Configure allowed host names that can be served and trusted origins for Azure Container Apps.
ALLOWED_HOSTS = [".azurecontainerapps.io"] if "RUNNING_IN_PRODUCTION" in os.environ else []
CSRF_TRUSTED_ORIGINS = ["https://*.azurecontainerapps.io"] if "RUNNING_IN_PRODUCTION" in os.environ else []

# Configure database connection for Azure PostgreSQL Flexible server instance.
DBUSER = os.environ["DBUSER"]
DBPASS = get_secret("DBPASS")
DBHOST = os.environ["DBHOST"]
DBNAME = os.environ["DBNAME"]
DATABASE_URI = f"postgresql+psycopg2://{DBUSER}:{DBPASS}@{DBHOST}/{DBNAME}?sslmode=require"
