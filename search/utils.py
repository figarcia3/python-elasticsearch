from django.conf import settings
from functools import wraps


def transform_json_list(json_list, index_name, mappings, id_name):
    transformed_list = []
    for input_json in json_list:
        source_data = {}
        for field in mappings:
            source_data[field] = input_json.get(field, None)

        transformed_json = {
            "_index": index_name,
            "_id": input_json[id_name],
            "_source": source_data
        }

        transformed_list.append(transformed_json)

    return transformed_list


def build_doc(source, id_name="id"):
    doc = source["_source"]
    doc[id_name] = source["_id"]
    return doc


def check_api_key(request):
    api_key = request.headers.get("X-API-KEY", None)
    if api_key is None:
        return False
    return api_key == settings.API_KEY


def auth_decorator(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        api_key = args[0].request.headers.get("X-API-KEY", None)
        if api_key is None or api_key != settings.API_KEY:
            raise PermissionError("Invalid API Key")
        return func(*args, **kwargs)
    return func_wrapper


def extract_number_token_from_query(query):
    tokens = query.split(" ")
    number_tokens = []
    for token in tokens:
        if is_digit(token):
            number_tokens.append(token)
    return number_tokens

def is_digit(token):
    try:
        int(token)
        return True
    except ValueError:
        return False