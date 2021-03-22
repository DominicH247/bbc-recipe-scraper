# BBC Food Recipe Scraper
A practice project for learning Python. It scrapes all the recipes from BBC Food and stores them in MongoDB.

Uses Beautuful Soup to collect the available cuisines. For each cuisine it gathers all available recipe URLs and from the recipe URLs we can then obtain the recipe details i.e
ingredients, methods, prep time etc

## Requirements
- Python 3.8 or higher
- Poetry
- Docker
- Docker Compose

## Running the application
- `poetry install` - install project dependencies
- `docker-compose up --build` - build docker image and runs the MongoDB container (requires setting of environment variables - see below)
- `poetry run python3 main.py` - run the project

## Environment Variables
The MongoDB container instance requires to following environment varaibles:
```
MONGO_USER
MONGO_PASSWORD
HOST_PORT
DATABASE_NAME
```
I typically use Direnv and add the environment variables to .envrc file at the project root. e.g.
```
export MONGO_USER=mongoadmin
export MONGO_PASSWORD=supersecure
export HOST_PORT=27017
export DATABASE_NAME=recipes_db
```

## Caveats
Project is very much WIP and was created as an excercise for learning Python.
There are ~5000 recipes available, it currently takes a while (30-40 mins) to gather and store all the recipes. 
I have to to experiment with async calls to try and speed this up but end up hitting request limits. Thus have settled on using synchronous requests for now.

Feel free to leave any comments or suggestions on where to improve. I would appreciate the feedback!

## TODO
- add tests
- fix some of the inconsistent module names
- fix the type hinting
- tidy up the code
