# Twitter-clone

## To do:
- Arrumar layout. Dificuldade :star::star:
Descrição:
    Arrumar Html e css, de forma a ficar mais parecido com o Twitter. Há uma extensão PixelPerfect no chrome que tem como colocar uma imagem abaixo da aplicação como referência.Estou me baseando na seguinte imagem do figma: [Flex Grid](https://www.figma.com/community/file/1013470200889674140)
- Deixar o site responsivo , para desktop , tablet e celular. Dificuldade: :star::star: 
- Incorporar Ajax. Dificuldade: :star::star::star::star: 
Descrição:
    Para não precisar recarregar a página toda vez que executar a função de login, registro , tweet e demais, basta adicionar Ajax na pasta static->js.
- Adicionar a funcionalidade de responder a tweets. Dificuldade: :star::star::star::star:
- Adicionar paginação. Dificuldade: :star::star::star:
Descrição:
    As mensagens em home e a lista de profile possuem limite por página. Fazer uso de django-rest-framework ou a própria biblioteca do Django.
- Usuários podem adicionar imagem aos tweets. Dificuldade: :star::star::star::star::star:
    O problema é salvar as imagens.



manage.py : 
It’s the tool through which you initiate the development server, create applications, run migrations, and more. manage.py is the conductor's baton, guiding your project's activities.

settings.py:
From database configurations to middleware lists, this is where you define how your application functions. 

urls.py:
This file determines which view is displayed when a specific URL is accessed. It's like a roadmap that navigates users through the intricacies of your application's pages.

wsgi.py:
It's the bridge connecting your application to the web server, enabling it to handle incoming requests.

asgi.py:
is the entry point for asynchronous web servers.

__init__py: 
transforms a directory into a Python package

models.py:
This is where you define the data structures using Django's ORM (Object-Relational Mapping). Each model class represents a table in the database. This file forms the foundation of your application's data management.

views:
ile encapsulates the logic that defines how your application interacts with users' requests. Views handle data processing, rendering templates, and responding to actions. 

Serializers are a crucial component in Django Rest Framework that facilitate the conversion of complex data types into native Python data types and vice versa. They play a vital role in data serialization and deserialization, validating incoming data, and handling different serialization formats like JSON and XML.

REST framework includes an abstraction for dealing with ViewSets, that allows the developer to concentrate on modeling the state and interactions of the API, and leave the URL construction to be handled automatically, based on common conventions.

ViewSet classes are almost the same thing as View classes, except that they provide operations such as retrieve, or update, and not method handlers such as get or put.