FROM python:3

EXPOSE 80
WORKDIR /app

RUN apt-get update && apt-get install -y vim libgdal-dev nginx supervisor

ENV CPLUS_INCLUDE_PATH=/usr/inulcde/gdal
ENV C_INCLUDE_PATH=/usr/inulcde/gdal

CMD supervisord

COPY ci /

COPY requirements/development.txt ./
RUN pip install --no-cache-dir -r development.txt

COPY . /app
RUN ./manage.py collectstatic --settings config.settings.base --no-input
