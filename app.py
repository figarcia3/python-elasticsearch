from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from functools import wraps

import os

from flask import (
    Flask,
    request,
    jsonify,
)

from dotenv import load_dotenv
import logging


load_dotenv()
logging.basicConfig(level=logging.DEBUG)

es = Elasticsearch("elastic://search:9200")
app = Flask(__name__)


def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if not api_key or not api_key == os.environ.get("API_KEY"):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def hello_world():
    result = es.indices.get_alias(index="*")
    return jsonify(result.body), 200


@app.route("/index", methods=['POST', 'GET'])
@require_api_key
def list_index():
    if request.method == 'GET':
        result = es.indices.get_alias(index="*")
        return jsonify(result.body), 200
    if request.method == 'POST':
        body = request.get_json()
        es.indices.create(
            index=body["name"], mappings=body["mappings"], settings=body["settings"],)
        return jsonify(body), 201
    return jsonify(), 400


@app.route("/index/<string:index_name>", methods=['GET', 'DELETE'])
@require_api_key
def show_index(index_name):
    if request.method == 'DELETE':
        es.indices.delete(index=index_name)
        return jsonify(), 204
    if request.method == 'GET':
        result = es.indices.get_alias(index=index_name)
        return jsonify(result.body), 200
    return jsonify(), 400


@app.route("/index/<string:index_name>/document/<string:id>", methods=['POST', 'GET', 'DELETE'])
@require_api_key
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


@app.route("/index/<string:index_name>/search", methods=['POST', 'GET'])
@require_api_key
def search(index_name):
    if request.method == 'POST':
        query = request.get_json()
        response = es.search(index=index_name, body=query)
        return jsonify(response.body), 200
    if request.method == 'GET':
        search_term = request.args.get('q')
        query = {
            "query": {
                "function_score": {
                    "query": {
                        "bool": {
                            "should": [
                                {"match": {"name": {"query": search_term, "boost": 1.6}}},
                                {"match": {"brand": {"query": search_term, "boost": 1.1}}},
                                {"match": {"variety": {
                                    "query": search_term, "boost": 1.1}}},
                                {"match": {"size": {"query": search_term, "boost": 1}}},
                                {"match": {"unit": {"query": search_term, "boost": 1}}}
                            ]
                        }
                    },
                    "boost": "5",
                    "functions": [
                        {
                            "filter": {"match": {"class": "W"}},
                            "weight": 1.1
                        },
                        {
                            "filter": {"match": {"class": "V"}},
                            "weight": 1.1
                        },
                        {
                            "filter": {"match": {"category": "U"}},
                            "weight": 1
                        },
                        {
                            "filter": {"match": {"category": "C"}},
                            "weight": 1
                        }
                    ],
                    "score_mode": "avg",
                    "boost_mode": "multiply"
                }
            }
        }
        response = es.search(index=index_name, body=query)
        return jsonify(response.body), 200
    return jsonify(), 400


@app.route("/index/add-documents", methods=['POST'])
@require_api_key
def add_documents():
    if request.method == 'POST':
        data = request.get_json()
        response = bulk(es, data["documents"])
        return jsonify(response), 200
    return jsonify(), 400


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5002)
