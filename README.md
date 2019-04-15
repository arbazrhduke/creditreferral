# defrag
[![CodeFactor](https://www.codefactor.io/repository/github/arbazrhduke/defrag/badge/master)](https://www.codefactor.io/repository/github/arbazrhduke/defrag/overview/master)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)


###### This project is developed as an assignment to defraglabs

### Installation
1. Create a virtualenv to setup environment to run application
   `virtualenv venv -p python3`
2. Install dependencies using following command
   `pip install -r requirements/dev.txt` for local settings for production
   run following command
   `pip install -r requirements/prod.txt`

3. Installing RabbitMQ on Ubuntu
`apt-get install -y erlang`
`apt-get install rabbitmq-server`
Then enable and start the RabbitMQ service

4. Enable RabbitMQ
`systemctl enable rabbitmq-server`
`systemctl start rabbitmq-server`
Check the status to make sure everything is running

`systemctl status rabbitmq-server`
   
### Running the Project
To run project.
+ Locally update create a .env file, copy contents from .env.dev add appropriate values then, run the following command..
   `python manage.py runserver --settings defrag.settings.local`
+ To run in production create a .env file copy contents from .env.prod add required values for config and run following command.
   `python manage.py runserver --settings defrag.settings.production`

### Running Celery
+ Open another terminal activate virtual environment and go to project path
and run the following command
`celery -A defrag worker -l info`

### Important Links
* [User model](/users/models.py)
* [Test Cases](/users/tests.py)
* [Rest API](/users/views.py)
* [Templates](/templates)

