import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from devtools import debug

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from search.utils import transform_json_list

es = Elasticsearch("elastic://search:9200")


@method_decorator(csrf_exempt, name='dispatch')
class ListIndexView(View):
    def get(self, request):
        result = es.indices.get_alias(index="*")
        return JsonResponse(result.body, safe=False, status=200)

    def post(self, request):
        body = json.loads(request.body)
        print(body)
        try:
            result = es.indices.create(
                index=body["name"], mappings=body["mappings"], settings=body["settings"])
        except Exception as e:
            debug(e)
            return JsonResponse({"error": str(e)}, status=400)
        return JsonResponse(result.body, safe=False, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class ShowIndexView(View):
    def get(self, request, index_name):
        result = es.indices.get_alias(index=index_name)
        return JsonResponse(result.body, safe=False, status=200)

    def delete(self, request, index_name):
        es.indices.delete(index=index_name)
        return JsonResponse({}, status=204)


@method_decorator(csrf_exempt, name='dispatch')
class DocumentIndexView(View):
    def get(self, request, index_name):
        response = es.search(index=index_name, body={
                             "query": {"match_all": {}}})
        documents = []
        for hit in response["hits"]["hits"]:
            doc = hit["_source"]
            doc["id"] = hit["_id"]
            documents.append(doc)
        return JsonResponse(documents, safe=False, status=200)

    def delete(self, request, index_name):
        es.delete_by_query(index=index_name, body={"query": {"match_all": {}}})
        return JsonResponse({}, status=204)


@method_decorator(csrf_exempt, name='dispatch')
class DocumentShowView(View):
    def get(self, request, index_name, id):
        response = es.get(index=index_name, id=id)
        return JsonResponse(response, safe=False, status=200)

    def post(self, request, index_name, id):
        body = json.loads(request.body)
        es.index(index=index_name, id=id, document=body)
        return JsonResponse(body, safe=False, status=200)

    def delete(self, request, index_name, id):
        es.delete(index=index_name, id=id)
        return JsonResponse({}, status=204)


@method_decorator(csrf_exempt, name='dispatch')
class SearchView(View):
    def post(self, request, index_name):
        body = json.loads(request.body)
        response = es.search(index=index_name, body=body)
        return JsonResponse(response.body, safe=False, status=200)

    def get(self, request, index_name):
        search_term = self.request.GET.get('q')
        query = {
            "query": {
                "function_score": {
                    "query": {
                        "bool": {
                            "should": [
                                {"match_phrase": {
                                    "name": {"query": search_term, "boost": 1}}},
                                {"match": {"brand": {"query": search_term, "boost": 1}}},
                                {"match": {"variety": {"query": search_term, "boost": 1}}},
                                {"match": {"size": {"query": search_term, "boost": 1}}},
                                {"match": {"unit": {"query": search_term, "boost": 1}}}
                            ]
                        }
                    },
                    "boost": 3,
                    "functions": [
                        {
                            "filter": {"match": {"class": "W"}},
                            "weight": 5
                        },
                        {
                            "filter": {"match": {"class": "V"}},
                            "weight": 5
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
                    "score_mode": "multiply",
                    "boost_mode": "multiply",
                }
            }
        }
        response = es.search(index=index_name, body=query)
        return JsonResponse(response.body, safe=False, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AddDocumentsView(View):
    def post(self, request, index_name):
        mappings = es.indices.get_mapping(index=index_name)
        mappings_list = mappings[index_name]['mappings']['properties'].keys()

        body = json.loads(request.body)
        body = transform_json_list(body, index_name, mappings_list)

        response = bulk(es, body)
        return JsonResponse(response, safe=False, status=200)
