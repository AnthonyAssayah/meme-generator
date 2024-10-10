# Meme Generator API

## Table of Contents  

- [Introduction](#introduction)
- [Features](#features)
- [Technologies](#technologies)
- [Usage](#usage)

## Introduction

The Meme Generator **API** is a RESTful web service that allows users to create, retrieve, rate, and view memes. The API is built using **Django** and **Django Rest Framework**, 
with **PostgreSQL** as the database. The entire application is containerized using **Docker** and **Docker Compose** for easy local development and deployment.
This API offers several endpoints for interacting with meme templates and user-generated memes. Users can create memes using pre-defined templates, 
rate them, view top-rated memes, and get random memes. Additionally, the API includes token-based authentication to secure access.

The project also comes with automated database management via Docker and Django, making it simple to run migrations, create a superuser, 
and start the application using a single command (```docker-compose up```).

## Features

- Meme Creation: Users can create memes using predefined templates. If no custom text is provided, the default text from the template is used.
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
