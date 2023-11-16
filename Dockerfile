FROM python:3.9.10-alpine3.14

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src

RUN pip install --upgrade pip
RUN pip install flask
RUN pip install elasticsearch
RUN pip install python-dotenv


COPY . /src
ENV FLASK_APP=app

RUN ["chmod", "+x", "/src/init.sh"]
CMD ["/src/init.sh"]