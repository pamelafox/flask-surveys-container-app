## Using this project with the Azure Developer CLI (azd)

This project is designed to work well with the [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview),
which makes it easier to develop apps locally, deploy them to Azure, and monitor them.

### Local development

This project has devcontainer support, so you can open it in Github Codespaces or local VS Code with the Dev Containers extension. 

Steps for running the server: 

1. (Optional) If you're unable to open the devcontainer, [create a Python virtual environment](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) and activate that.

2. Install the requirements:

```shell
pip install -r requirements.txt
```

3. Create an `.env` file using `.env.sample` as a guide. Set the value of `DBNAME` to the name of an existing database in your local PostgreSQL instance. Set the values of `DBHOST`, `DBUSER`, and `DBPASS` as appropriate for your local PostgreSQL instance. If you're in the devcontainer, copy the values from `.env.sample.devcontainer`.

4. Run the migrations:

```shell
flask db upgrade
```

5. Run the local server: (or use VS Code "Run" button and select "Run server")

```shell
flask run
```

### Local development with Docker

Since this app depends on a database, there's a docker-compose.yaml that creates two containers (one for the app, one for the DB)
as well as a volume to store the database data.

Start the services with this command:

```
docker-compose up --build
```

### Deployment

This repo is set up for deployment on Azure Container Apps (w/PostGreSQL server) using the configuration files in the `infra` folder.

Steps for deployment:

1. Sign up for a [free Azure account](https://azure.microsoft.com/free/)
2. Install the [Azure Dev CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd). (If you opened this repository in a devcontainer, that part will be done for you.)
3. Provision and deploy all the resources:

```shell
azd up
```

It will prompt you to login and to provide a name (like "flask-app") and location (like "eastus"). Then it will provision the resources in your account and deploy the latest code. If you get an error with deployment, changing the location (like to "centralus") can help, as there are availability constraints for some of the resources.

4. When `azd` has finished deploying, you'll see an endpoint URI in the command output. Visit that URI, and you should see the front page of the restaurant review app! 🎉 If you see an error, open the Azure Portal from the URL in the command output, navigate to the App Service, select Logstream, and check the logs for any errors.

![Screenshot of Flask restaurants website](screenshot_website.png)

5. When you've made any changes to the app code, you can just run:

```shell
azd deploy
```


## Getting help

If you're working with this project and running into issues, please post in [Discussions](/discussions). 
