This project is a demonstration of a Flask app that uses a database and is designed to be used with Docker containers,
both for local development and deployment.


### Local development with Docker

Since this app depends on a database, there's a `docker-compose.yaml` file that creates two containers
(one for the app, one for the DB) as well as a volume to store the database data.

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/). (If you opened this inside Github Codespaces or a Dev Container in VS Code, installation is not needed.)

2. Create an `.env` file by copying `.env.example`.

3. Start the services with this command:

    ```shell
    docker-compose up --build
    ```

4. Try creating a new survey and answering your newly created survey.

Alternatively, if you are iterating frequently on the app code, you might want to run only the database in a container.

1. Create a volume to store the database data:

```shell
docker volume create postgres-data
```

2. Export the environment variables:

```shell
source .env
```

3. Run a `postgres` container and expose on localhost:5432:

```shell
docker run --rm -d -v postgres-data:/var/lib/postgresql/data \
    -e POSTGRES_USER=DBUSER -e POSTGRES_PASSWORD=DBPASS \
    --publish 5432:5432 postgres
```

4. Upgrade the database and run the server:

```shell
flask db migrate && flask run
```

4. Try creating a new survey and answering your newly created survey.


### Deployment

This repo is set up for deployment on Azure Container Apps with a PostGreSQL server using the `Dockerfile` and the configuration files in the `infra` folder.

Steps for deployment:

1. Sign up for a [free Azure account](https://azure.microsoft.com/free/)
2. Install the [Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd). (If you opened this repository in a devcontainer, that part will be done for you.)
3. Provision and deploy all the resources:

    ```shell
    azd up
    ```

    It will prompt you to login and to provide a name (like "flask-app") and location (like "eastus"). Then it will provision the resources in your account and deploy the latest code. If you get an error with deployment, changing the location (like to "centralus") can help, as there are availability constraints for some of the resources.

4. When `azd` has finished deploying, you'll see an endpoint URI in the command output. Visit that URI, and you should see the front page of the app! 🎉

5. When you've made any changes to the app code, you can just run:

    ```shell
    azd deploy
    ```


## Getting help

If you're working with this project and running into issues, please post in [Discussions](/discussions).
