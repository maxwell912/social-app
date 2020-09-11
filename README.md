# Django Project Template

Works with PostgreSQL.

## Start a project

```shell
$ django-admin startproject project-name --template ./django-project-template/
```

## Install requirements

```shell
$ pip install -r requirements/development.txt
```

## Run a database

```shell
$ docker-compose up -d postgres
```

## Set up local settings

```shell
$ vi config/settings/local.py
```

Put your local settings in the `local.py`, you can override settings
consider your local environment. Start with lines below:

```python
from .base import *
```


## Apply migrations

```shell
$ ./manage.py migrate
```

### Create Superuser

The project will use E-Mail address as username.

```shell
$ ./manage.py createsuperuser
```
