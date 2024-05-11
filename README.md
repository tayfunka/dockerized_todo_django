# ListApp Project Report

## Introduction

The ListApp project is a Django-based to-do list application developed to meet user task management needs efficiently. The application provides users with a simple yet effective single-screen interface for managing their tasks.

### Technologies Used

- Django
- Django Rest Framework
- PostgreSQL
- HTMX
- TailwindCSS
- JavaScript
- Docker
- GitHub
- Flake8

GitHub Actions were configured to automate testing and linting processes using the tool "flake8" for code quality assurance.

## Structure

The project is organized into three main apps: Core, User, and Todo.

- **Core App**: Contains models and views, including the home view.
- **User and Todo Apps**: Responsible for user authentication and task management functionalities respectively.

An API endpoint was established at `/api/todos/` to list all todos. SessionAuthentication was specified as the authentication method, but TokenAuthentication can be used by uncommenting the relevant lines.

## Features

The project includes Todo and User models with a REST API created using DRF, supporting SessionAuthentication and TokenAuthentication (not activated). Endpoints for CRUD operations are provided.

**Swagger UI:** Test all endpoints using the following URL: [Swagger UI](http://127.0.0.1:8000/api/docs/)

## Known Issues

### Warning:

- Accessing the `/api/todos` endpoint directly via a browser may result in a TypeError due to discrepancies in response formatting.

**Note:** Swagger UI provides correct responses. Use [this link](http://127.0.0.1:8000/api/docs/#/api/api_todos_list) to test.

### Authentication

**With Swagger:**

1. Create a user from `/api/user/create/`
2. Obtain the token from `/api/user/token`
3. Paste the token into the `tokenAuth` (apiKey) section in the Authentication menu.

**Without Swagger:** Access the `/register` URL directly at [http://127.0.0.1:8000/register](http://127.0.0.1:8000/register)

### Errors:

- Item count does not change when an object is deleted from the list.
- Token authentication cannot be performed with the frontend; SessionAuthentication is used instead.
- The endpoint `/api/tasks` should be `/api/todos`.
