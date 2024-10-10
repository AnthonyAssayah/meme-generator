# Meme Generator API

## Table of Contents  

- [Introduction](#introduction)
- [Features](#features)
- [Technologies](#technologies)
- [Usage](#usage)
- [File Structure](#file-structure)

## Introduction

The Meme Generator **API** is a RESTful web service that allows users to create, retrieve, rate, and view memes. The API is built using **Django** and **Django Rest Framework**, 
with **PostgreSQL** as the database. The entire application is containerized using **Docker** and **Docker Compose** for easy local development and deployment.
This API offers several endpoints for interacting with meme templates and user-generated memes. Users can create memes using pre-defined templates, 
rate them, view top-rated memes, and get random memes. Additionally, the API includes token-based authentication to secure access.

The project also comes with automated database management via Docker and Django, making it simple to run migrations, create a superuser, 
and start the application using a single command (```docker-compose up```).

## Features

- Meme Creation: Users can create memes wit pagination using predefined templates. If no custom text is provided, the default text from the template is used.
- Meme Rating: Users can rate memes on a scale of 1 to 5. Each user can only rate a meme once but can update their rating.
- Top Memes: The API calculates the average rating of memes and returns the top 10 most highly-rated memes.
- Random Meme: Users can request a random meme.
- Authentication: Token-based authentication ensures that users can securely access the API.
- Dockerized Application: The app and database are containerized using Docker Compose, making setup and running the project easy.
- Testing: Unit tests are included to ensure proper functionality and high test coverage for all endpoints.

## Technologies

- Backend: Django, Django Rest Framework (DRF)
- Database: PostgreSQL
- Containerization: Docker, Docker Compose
- Authentication: Token-based Authentication (DRF Token Auth)

## Usage

1- **Run the Project Locally**: After cloning the repository, you can start the application with the following command:

      docker-compose up 

This command will:

- Build the Docker image for the Django app
- Start the PostgreSQL database
- Apply all migrations
- Create the superuser
- Start the Django development server

2- **API endpoints**: 

To effectively develop and document the API endpoints, you can access the Django Rest Framework's API interface at:

 ``` http://127.0.0.1:8000/api/ ```

This interface allows you to interact with your API endpoints in a user-friendly way, view all available endpoints, and make requests to them. 
You can perform actions like:

- GET ```/api/templates/``` - List all meme templates
- GET ```/api/memes/``` - List all memes (with pagination)
- POST ```/api/memes/``` - Create a new meme
- GET ```/api/memes/<id>/``` - Retrieve a specific meme
- POST ```/api/memes/<id>/rate/``` - Rate a meme (1-5)
- GET ```/api/memes/random/``` - Get a random meme
- GET ```/api/memes/top/``` - Get top 10 rated memes

You can also interact with the Meme Generator API using ```curl``` commands directly from the Docker container. This allows you to perform actions such as listing templates, creating memes, rating memes, and fetching random or top-rated memes. Here's how you can use curl to make requests to the API.

- ```docker exec -it meme-generator-web-1```: Executes the command inside the ```meme-generator-web-1 container```.
- ```curl -X <METHOD>```: Executes the HTTP method (GET, POST, etc.).
- ```http://localhost:8000/api/<endpoint>```: The API endpoint you want to interact with.
- ```-H "Content-Type: application/json"```: Sets the content type to JSON (for POST requests).
- ```-H "Authorization: Token <your_token>```": Passes the authentication token for the request.
- ```-d "<data>"```: The data to be sent with the request (for POST requests).

  examples:
  - for list all memes: ```docker exec -it meme-generator-web-1 curl -X GET http://localhost:8000/api/memes/```
  - for rate a meme: ```docker exec -it meme-generator-web-1 curl -X POST http://localhost:8000/api/memes/4/rate/ -H "Content-Type: application/json" -H "Authorization: Token a4a9644c7b8ab4540a34fc80e501e494707b89c4" -d "{\"rating\": 5}"```
  - for get a random meme: ```docker exec -it meme-generator-web-1 curl -X GET http://localhost:8000/api/memes/random/```
 
  While inside the Docker environment, you can run the automated tests for the Meme Generator API using the following command:
      ``` docker-compose exec web python manage.py test ```

 

    ## File Structure

Within the download you'll find the following directories and files:

```
MEME-GENERATOR
  ├── memegenerator
  |     ├── settings.py
  |     ├── urls.py
  |     ├── asgi.py
  |     └── wsgi.py
  ├── memes
  │   ├── migrations
  │   ├── app.py
  │   ├── models.py
  │   ├── tests.py
  │   ├── urls.py
  │   ├── views.py
  │   └── serializers.py
  ├── Dockerfile
  ├── docker-compose.yml
  ├── server.js
  ├── manage.py
  └── requirements.py
```

