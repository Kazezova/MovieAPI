# MovieAPI
## Introduction
The MovieAPI provides a RESTful web service to perform create movies web applications. It is written using a powerful and flexible toolkit, the Django REST framework (DRF). To see all the available methods and endpoints, you must read the project description. P.S. description not ready yet:)
## Getting started
#### Clone the repository to your local machine:
* `git clone https://github.com/Kazezova/MovieAPI.git`
* `cd MovieAPI/MovieAPI`
#### Install Python 3, if you don't have it installed:
* https://www.python.org/downloads/
#### Create and activate a virtual environment:
> You can take this step using your preferred method.
* `python3 -m venv env`
* `source env/bin/activate`
#### Install necessary packages:
* `pip install -r requirements.txt`
#### Create PostgreSQL database:
* https://www.postgresqltutorial.com/postgresql-getting-started/
#### Configure database in settings.py:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your_db_name',
        'USER': 'your_username',
        'PASSWORD': 'your_pasword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
#### Run database migrations:
* `python manage.py migrate`
#### Create a superuser:
* `python manage.py createsuperuser`
#### Run the API server:
* `python manage.py runserver`
