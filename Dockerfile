FROM python:3.9.10-alpine3.14
WORKDIR /src

RUN pip install --upgrade pip
RUN pip install flask
RUN pip install elasticsearch
COPY . /src
ENV FLASK_APP=app

RUN ["chmod", "+x", "/src/init.sh"]
CMD ["/src/init.sh"]