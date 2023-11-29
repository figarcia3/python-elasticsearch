import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from devtools import debug

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from search.utils import auth_decorator, build_doc, transform_json_list

from functools import wraps


es = Elasticsearch("elastic://search:9200")


class BulkIndexError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


@method_decorator(csrf_exempt, name='dispatch')
class ListIndexView(View):

    @auth_decorator
    def get(self, request):
        result = es.indices.get_alias(index="*")
        return JsonResponse(result.body, safe=False, status=200)

    @auth_decorator
    def post(self, request):
        body = json.loads(request.body)
        result = es.indices.create(
            index=body["name"], mappings=body["mappings"], settings=body["settings"])
        return JsonResponse(result.body, safe=False, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class ShowIndexView(View):

    @auth_decorator
    def get(self, request, index_name):
        result = es.indices.get_alias(index=index_name)
        return JsonResponse(result.body, safe=False, status=200)

    @auth_decorator
    def delete(self, request, index_name):
        es.indices.delete(index=index_name)
        return JsonResponse({}, status=204)


@method_decorator(csrf_exempt, name='dispatch')
class DocumentIndexView(View):

    @auth_decorator
    def get(self, request, index_name):
        response = es.search(index=index_name, body={
                             "query": {"match_all": {}}})
        documents = []
        for hit in response["hits"]["hits"]:
            documents.append(build_doc(hit))
        return JsonResponse(documents, safe=False, status=200)

    @auth_decorator
    def delete(self, request, index_name):
        es.delete_by_query(index=index_name, body={"query": {"match_all": {}}})
        return JsonResponse({}, status=204)


@method_decorator(csrf_exempt, name='dispatch')
class DocumentShowView(View):

    @auth_decorator
    def get(self, request, index_name, id):
        response = es.get(index=index_name, id=id)
        doc = build_doc(response.body)
        return JsonResponse(doc, safe=False, status=200)

    @auth_decorator
    def post(self, request, index_name, id):
        body = json.loads(request.body)
        es.index(index=index_name, id=id, document=body)
        return JsonResponse(body, safe=False, status=200)

    @auth_decorator
    def delete(self, request, index_name, id):
        es.delete(index=index_name, id=id)
        return JsonResponse({}, status=204)


@method_decorator(csrf_exempt, name='dispatch')
class SearchView(View):

    @auth_decorator
    def post(self, request, index_name):
        body = json.loads(request.body)
        response = es.search(index=index_name, body=body)
        return JsonResponse(response.body, safe=False, status=200)

    @auth_decorator
    def get(self, request, index_name):
        search_term = self.request.GET.get('q')
        query = {
            "query": {
                "function_score": {
                    "query": {
                        "bool": {
                            "should": [
                                {"match": {
                                    "product_name.name": {"query": search_term, "boost": 1}}},
                                {"match": {"brand.name": {
                                    "query": search_term, "boost": 1}}},
                                {"match": {"variety_name": {
                                    "query": search_term, "boost": 1}}},
                                {"match": {"quantity": {"query": search_term, "boost": 1}}},
                                {"match": {"measure_unit.name": {
                                    "query": search_term, "boost": 1}}}
                            ]
                        }
                    },
                    "boost": 3,
                    "functions": [
                        {
                            "filter": {"match": {"product_class.id": "W"}},
                            "weight": 5
                        },
                        {
                            "filter": {"match": {"product_class.id": "V"}},
                            "weight": 5
                        },
                        {
                            "filter": {"match": {"product_class.id": "U"}},
                            "weight": 1
                        },
                        {
                            "filter": {"match": {"product_class.id": "C"}},
                            "weight": 1
                        }
                    ],
                    "score_mode": "multiply",
                    "boost_mode": "multiply",
                }
            }
        }
        response = es.search(index=index_name, body=query)
        return JsonResponse(response.body, safe=False, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AddDocumentsView(View):

    @auth_decorator
    def post(self, request, index_name):
        mappings = es.indices.get_mapping(index=index_name)
        mappings_list = mappings[index_name]['mappings']['properties'].keys()

        body = json.loads(request.body)
        docs = transform_json_list(body, index_name, mappings_list)
        # print(docs)
        try:
            response = bulk(es, docs)
        except Exception as e:
            print(f"List of errors: {e.errors}")
        return JsonResponse(response, safe=False, status=200)
