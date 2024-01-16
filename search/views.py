import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from devtools import debug

from elasticsearch import Elasticsearch, RequestError
from elasticsearch.helpers import bulk
from search.queries import numeric_products_query, numeric_store_products_query, products_query, store_products_query

from search.utils import auth_decorator, build_doc, extract_number_token_from_query, transform_json_list

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
        doc = build_doc(response.body, "eanid" if "products" == index_name else "id")
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
        query = products_query(search_term)
        response = es.search(index=index_name, body=query)
        documents = []
        for hit in response["hits"]["hits"]:
            documents.append(hit["_source"])
        return JsonResponse(documents, safe=False, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class MultiSearchView(View):

    @auth_decorator
    def get(self, request):
        search_term = self.request.GET.get('q')
        store = self.request.GET.get('store')

        query_products = products_query(search_term)
        query_stores = store_products_query(search_term, store)
        if search_term.isnumeric():
            print('NUMERIC SEARCH')
            query_products = numeric_products_query(search_term)
            query_stores = numeric_store_products_query(search_term, store)

        response = es.search(index='products', body=query_products)
        documents_products = []
        for hit in response["hits"]["hits"]:
            documents_products.append(hit["_source"])

        
        response_store = es.search(index='store_products', body=query_stores)
        documents_store_products = []

        for hit in response_store["hits"]["hits"]:
            documents_store_products.append(hit["_source"])

        return JsonResponse({"products": documents_products, "store_products": documents_store_products}, safe=False, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class AddDocumentsView(View):

    @auth_decorator
    def post(self, request, index_name):
        mappings = es.indices.get_mapping(index=index_name)
        mappings_list = mappings[index_name]['mappings']['properties'].keys()

        body = json.loads(request.body)
        body = transform_json_list(body, index_name, mappings_list, "eanid" if "eanid" in mappings_list else "id")

        try:
            response = bulk(es, body)
        except BulkIndexError as e:
            print("ERRORS: ", e.errors)
            response = {}
        return JsonResponse(response, safe=False, status=200)
