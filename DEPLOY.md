# Deploy Template

#### Create a config/settings/deploy.py to override the current application settings. 
#### As a template, you can use deploy.py.template.

###### Add your host to ALLOWED_HOSTS. This is a list of strings - hostnames that this Django site can serve.

##### The project uses: PostgreSQL.
###### Modify the DATABASE params like name, user, password, host and port to connect to the database.

#### To run the image:

``` 
$ docker-compose up -d postgres
```