# Twitter-clone

## Overview
Twitter-clone project build in Django which has the main functionalities of social networks. 
The user can :
:small_orange_diamond: register/login/logout;
:small_orange_diamond: create/edit a profile;
:small_orange_diamond: comment/delete a comment/favorite/reply to a comment;
:small_orange_diamond: follow and unfollow another user;

### Prerequisites

```
- Docker (installation guide: https://docs.docker.com/get-docker/ )
- docker-compose
- git
```

Optional:
```
poetry (installation guide: https://python-poetry.org/docs/#installation )
python
```

### Getting Started
Follow these instructions to run this project on your local machine 

1. Clone this project

```
git clone https://github.com/Bee-ah/Twitter-clone.git
cd Twitter-clone
```

2. Build and run docker container

**You must be in the project directory to run this command**
```
docker-compose up -d --build
```

3. Run Django migrations

Applies the database migrations needed for the project:
```
docker-compose exec web poetry run python manage.py migrate
```

4. If needed , create a superuser

If you want to access Django admin interface or test features that require superuser privileges, you can create a superuser.
```
docker-compose exec web poetry run python manage.py createsuperuser
```

5. Access the application
The application should be accessible at http://localhost:8001/ 


#### Review of some django files

- manage.py : 
Tool through which you initiate the development server, create applications, run migrations ...

- settings.py:
This is where you define how your application functions. 

- urls.py:
This file determines which view is displayed when a specific URL is accessed.

- wsgi.py:
Bridge connecting your application to the web server, enabling it to handle incoming requests.

- asgi.py:
Entry point for asynchronous web servers.

- __init__py: 
Transforms a directory into a Python package

- models.py:
Data structures that uses Django's ORM

- views:
Encapsulates the logic that defines how your application interacts with users' requests. Views handle data processing, rendering templates, and responding to actions. 

- Serializers:
Facilitate the conversion of complex data types into native Python data types and vice versa. They play a vital role in data serialization and deserialization, validating incoming data, and handling different serialization formats like JSON and XML.

- REST framework:
Includes an abstraction for dealing with ViewSets, that allows the developer to concentrate on modeling the state and interactions of the API, and leave the URL construction to be handled automatically, based on common conventions.

- viewSet:
Are almost the same thing as View classes, except that they provide operations such as retrieve, or update, and not method handlers such as get or put.