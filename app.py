from flask import Flask
from flask import request

import json

import logging
from elasticsearch import Elasticsearch

logging.basicConfig(level=logging.DEBUG)

es = Elasticsearch("http://localhost:9200")
app = Flask(__name__)


@app.route("/")
def hello_world():
    app.logger.info(es.info().body)
    app.logger.info("Hello World")
    return "<h1>Starter Flask App</h1>"


@app.route("/create-index", methods=['POST'])
def create_index():
    data = request.get_json()
    app.logger.info(data)
    return {}


@app.route("/set-config", methods=['POST'])
def set_config():
    request.form
    return {}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
