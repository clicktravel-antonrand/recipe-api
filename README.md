# Recipe API

## Description

TK onboarding exercise using the Django REST framework to create an API allowing CRUD on recipes.

## Getting Started

### Running the application
The application is encapsulated inside a Docker container, to get the API running locally you need to run:

`docker-compose up`

Which will run both the django app and db containers.

### Contributing
When contributing, the Travis pipeline expects all tests to pass and no lint failures

You can run the tests with the following command:

`docker-compose run --rm app sh -c "python manage.py test`

You can run the linter with the following command:

`docker-compose run --rm app sh -c "flake8"`

Or chain them:

`docker-compose run --rm app sh -c "python manage.py test && flake8"`

### Updating the model
When you change the model you will need to run the `makemigrations` command for these changes to be reflected.

`docker-compose run app sh -c "python manage.py makemigrations core"`

## Usage

The following endpoints are supported:

- Get all recipes
  - GET /recipes/
- Get recipe by ID
  - GET /recipes/\<id>
- Get recipe containing name
  - GET /recipes/?name=\<name>
- Create recipe
  - POST /recipes/
  ```json
  {
    "name": "Margherita Pizza", 
    "description": "Put it in the oven", 
    "ingredients": [
      { "name": "cheese" }, 
      { "name": "tomato" }, 
      { "name": "dough" }
    ]
  }
  ```
- Update recipe
  - PATCH /recipes/\<id>
    ```json
    {
      "name": "Pepperoni Pizza", 
      "description": "Put it in the oven", 
      "ingredients": [
        { "name": "pepperoni" }, 
        { "name": "cheese" }, 
        { "name": "tomato" }, 
        { "name": "dough" }
      ]
    }
    ```
- Delete recipe
  - DELETE /recipes/\<id>

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/f9acdc09b38ccd446721)