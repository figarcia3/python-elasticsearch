from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from flask import (
    Flask,
    request,
    jsonify
)

import pandas as pd
import logging


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
        result = es.indices.get_alias(index="*")
        return jsonify(result.body), 200
    if request.method == 'POST':
        body = request.get_json()
        es.indices.create(
            index=body["name"], mappings=body["mappings"], settings=body["settings"],)
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


@app.route("/index/<string:index_name>/bulk-update", methods=['POST'])
def bulk_update(index_name):
    df = pd.read_csv("data/sample_products.csv")

    bulk_data = []
    for _i, row in df.iterrows():
        print(f"Adding {row['id']}")
        bulk_data.append(
            {
                "_index": index_name,
                "_id": row["id"],
                "_source": {
                    "name": row["name"],
                    "variety": row["variety"],
                    "brand": row["brand"],
                    "size": row["size"],
                    "unit": row["unit"],
                    "class": row["class"],
                }
            }
        )

    bulk(es, bulk_data)
    return jsonify(), 200


@app.route("/index/<string:index_name>/search", methods=['POST', 'GET'])
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
def add_documents():
    if request.method == 'POST':
        data = request.get_json()
        response = bulk(es, data["bulk_data"])
        return jsonify(response), 200
    return jsonify(), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
