### Setup (in root directory):
Preconditions:
- Clone this repository: git clone https://github.com/nikiturka/SpyCat
- Open the project locally at the project root (...\SpyCat)
- Start Docker Desktop or ensure the Docker service is running

#### Build docker containers
```shell
docker-compose build
```

#### Apply initial migrations
```shell
docker-compose run app python manage.py migrate 
```

#### Run docker-compose
```shell
docker-compose up
```

### Additional commands

### Create test data

#### Firstly, SpyCat objects need to be created:
```shell
docker-compose run app python manage.py create_test_cats
```

#### After that you can create Mission objects:
```shell
docker-compose run app python manage.py create_test_missions
```

### Run tests:
```shell
docker-compose run app pytest
```

### Create superuser for admin panel:
```shell
docker-compose run app python manage.py createsuperuser
```


### General Info

- **Docker-compose setup:** demonstrates Docker skills by containerizing the application in a separate app along with a PostgreSQL database.
- **Tests:** unit tests for core business logic are written using pytest.
- Country field in Target model is currently implemented as a simple `CharField`. Potentially, it could be extracted into a separate model or even a 
dedicated application, if more business logic will be associated with countries in the future.