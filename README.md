# Twitter-clone

´docker-compose up -d --build
´

### Review of some django files
manage.py : 
Tool through which you initiate the development server, create applications, run migrations ...

settings.py:
this is where you define how your application functions. 

urls.py:
This file determines which view is displayed when a specific URL is accessed.

wsgi.py:
Bridge connecting your application to the web server, enabling it to handle incoming requests.

asgi.py:
Entry point for asynchronous web servers.

__init__py: 
Transforms a directory into a Python package

models.py:
Data structures that uses Django's ORM

views:
Encapsulates the logic that defines how your application interacts with users' requests. Views handle data processing, rendering templates, and responding to actions. 

Serializers facilitate the conversion of complex data types into native Python data types and vice versa. They play a vital role in data serialization and deserialization, validating incoming data, and handling different serialization formats like JSON and XML.

REST framework includes an abstraction for dealing with ViewSets, that allows the developer to concentrate on modeling the state and interactions of the API, and leave the URL construction to be handled automatically, based on common conventions.

ViewSet classes are almost the same thing as View classes, except that they provide operations such as retrieve, or update, and not method handlers such as get or put.