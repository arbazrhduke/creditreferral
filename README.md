# defrag
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)


###### This project is developed as an assignment to defraglabs

### Installation
1. Create a virtualenv to setup environment to run application
   `virtualenv venv -p python3`
2. Install dependencies using following command
   `pip install -r requirements/dev.txt` for local settings for production
   run following command
   `pip install -r requirements/prod.txt`
3. To run project.
+ locally run the following command..
   `python manage.py runserver --settings defrag.settings.local`
+ to run in production mode update .env file with required values and run following command.
   `python manage.py runserver --settings defrag.settings.production`

### Important Links
* [User model](/users/models.py)
* [Test Cases](/users/tests.py)
* [Rest API](/users/views.py)
* [Templates](/templates)

