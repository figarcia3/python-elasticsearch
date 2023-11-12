from flask import Flask, request, jsonify

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


@app.route("/index", methods=['POST', 'GET'])
def list_index():
    if request.method == 'GET':
        return jsonify(es.indices.get_alias("*")), 200
    if request.method == 'POST':
        body = request.get_json()
        es.indices.create(index=body["name"], mappings=body["mappings"])
        return jsonify(body), 201
    return jsonify(), 400


@app.route("/index/<string:index_name>", methods=['GET', 'DELETE'])
def show_index(index_name):
    if request.method == 'DELETE':
        es.indices.delete(index=index_name)
        return jsonify(), 204
    if request.method == 'GET':
        result = es.indices.get_alias(index=index_name)
        return jsonify(result.body), 200
    return jsonify(), 400


@app.route("/index/<string:index_name>/document/<string:id>", methods=['POST', 'GET', 'DELETE'])
def document_index(index_name, id):
    if request.method == 'POST':
        body = request.get_json()
        es.index(index=index_name, id=id, document=body)
        return jsonify(body), 200
    if request.method == 'DELETE':
        es.delete(index=index_name, id=id)
        return jsonify(), 204
    if request.method == 'GET':
        response = es.get(index=index_name, id=id)
        return jsonify(response.body), 200
    return jsonify(), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
