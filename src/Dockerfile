# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Set directory for the app
WORKDIR /code

# Install pip requirements
RUN apt-get update && apt-get -y install libpq-dev gcc
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Copy application code
COPY . .

# Creates a non-root user with an explicit UID and adds permission to access the /code folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /code
USER appuser

# Expose the default Flask port
EXPOSE 50505

ENTRYPOINT ["/code/entrypoint.sh"]
