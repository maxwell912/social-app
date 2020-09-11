FROM python:3

ARG  APP_ENV

### install base deps
RUN apt-get update && apt-get install -y libgdal-dev nginx supervisor

### install rattus (maybe for DB creds)
RUN curl -LSs -o /usr/bin/rattus \
https://github.com/Saritasa/rattus/releases/download/0.2/rattus-linux-amd64 &&\
chmod +x /usr/bin/rattus

### setup run parameters 
EXPOSE 80
WORKDIR /app
ENTRYPOINT [ "supervisord", "-c", "/etc/supervisor.conf" ]

### set up environment variables
ENV CPLUS_INCLUDE_PATH=/usr/inulcde/gdal
ENV C_INCLUDE_PATH=/usr/inulcde/gdal
ENV DJANGO_SETTINGS_MODULE=config.settings.${APP_ENV}

ENV VAULT_SECRET=https://vault.saritasa.io/v1/project/data/pycamp_socialapp_dev
ENV TEMPLATE_PATH=/app/config/settings/deploy.py.template
### install deps
COPY requirements/development.txt ./
RUN pip install --no-cache-dir -r development.txt

### copy container configuration
COPY ci/docker/etc /etc/

### copy source code to container
COPY . /app

### 
RUN ./manage.py collectstatic --settings config.settings.base --no-input