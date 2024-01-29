from search.utils import extract_number_token_from_query
from decimal import Decimal

def products_query_test(search_term):
    measure_unit_list = extract_number_token_from_query(search_term)

    measure_unit = None
    if len(measure_unit_list) > 0:
        measure_unit = Decimal(measure_unit_list[0])
        return {
            "min_score": 7,
            "size": 100,
            "sort": [
                {
                    "product_class.id": {
                        "order": "desc",
                        "nested": {
                            "path": "product_class"
                        }
                    }
                },
                "_score"
            ],
            "query": {
                "function_score": {
                    "query": {
                        "bool": {
                            "should": [
                                {
                                    "nested": {
                                        "path": "product_name",
                                        "query": {
                                            "match": {
                                                "product_name.name": {
                                                    "query": search_term,
                                                    "boost": 2
                                                }
                                            }
                                        }
                                    }
                                },
                                {
                                    "nested": {
                                        "path": "brand",
                                        "query": {
                                            "match": {
                                                "brand.name": {
                                                    "query": search_term,
                                                    "boost": 3
                                                }
                                            }
                                        }
                                    }
                                },
                                {
                                    "term": {
                                        "quantity": measure_unit
                                    }
                                },
                                {
                                    "match": {
                                        "variety_name": {
                                            "query": search_term,
                                            "boost": 1
                                        }
                                    }
                                },
                                {
                                    "nested": {
                                        "path": "measure_unit",
                                        "query": {
                                            "match": {
                                                "measure_unit.name": {
                                                    "query": search_term,
                                                    "boost": 1
                                                }
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    "boost_mode": "sum"
                }
            }
        }

    else:
        return {
            "min_score": 7,
            "size": 100,
            "sort": [
                {
                    "product_class.id": {
                        "order": "desc",
                        "nested": {
                            "path": "product_class"
                        }
                    }
                },
                "_score"
            ],
            "query": {
                "function_score": {
                    "query": {
                        "bool": {
                            "should": [
                                {
                                    "nested": {
                                        "path": "product_name",
                                        "query": {
                                            "match": {
                                                "product_name.name": {
                                                    "query": search_term,
                                                    "boost": 2
                                                }
                                            }
                                        }
                                    }
                                },
                                {
                                    "nested": {
                                        "path": "brand",
                                        "query": {
                                            "match": {
                                                "brand.name": {
                                                    "query": search_term,
                                                    "boost": 3
                                                }
                                            }
                                        }
                                    }
                                },
                                {
                                    "match": {
                                        "variety_name": {
                                            "query": search_term,
                                            "boost": 1
                                        }
                                    }
                                },
                                {
                                    "nested": {
                                        "path": "measure_unit",
                                        "query": {
                                            "match": {
                                                "measure_unit.name": {
                                                    "query": search_term,
                                                    "boost": 1
                                                }
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    "boost_mode": "sum"
                }
            }
        }

def products_query(search_term):
    measure_unit_list = extract_number_token_from_query(search_term)

    measure_unit = None
    if len(measure_unit_list) > 0:
        measure_unit = Decimal(measure_unit_list[0])
        return {
            "size": 50,
            "query": {
                "function_score": {
                    "query": {
                        "bool": {
                            "should": [
                                {
                                    "nested": {
                                        "path": "product_name",
                                        "query": {
                                            "match": {
                                                "product_name.name": {
                                                    "query": search_term,
                                                    "boost": 2
                                                }
                                            }
                                        }
                                    }
                                },
                                {
                                    "nested": {
                                        "path": "brand",
                                        "query": {
                                            "match": {
                                                "brand.name": {
                                                    "query": search_term,
                                                    "boost": 3
                                                }
                                            }
                                        }
                                    }
                                },
                                {
                                    "match": {
                                        "variety_name": {
                                            "query": search_term,
                                            "boost": 1
                                        }
                                    }
                                },
                                {
                                    "term": {
                                        "quantity": measure_unit
                                    }
                                },
                                {
                                    "nested": {
                                        "path": "measure_unit",
                                        "query": {
                                            "match": {
                                                "measure_unit.name": {
                                                    "query": search_term,
                                                    "boost": 1
                                                }
                                            }
                                        }
                                    }
                                },
                            ]
                        }
                    },
                    "boost": 3,
                    "functions": [
                        {
                            "filter": {
                                "nested": {
                                    "path": "product_class",
                                    "query": {
                                        "match": {
                                            "product_class.id": "W"
                                        }
                                    }
                                }
                            },
                            "weight": 1
                        },
                        {
                            "filter": {
                                "nested": {
                                    "path": "product_class",
                                    "query": {
                                        "match": {
                                            "product_class.id": "V"
                                        }
                                    }
                                }
                            },
                            "weight": 1
                        },
                        {
                            "filter": {
                                "nested": {
                                    "path": "product_class",
                                    "query": {
                                        "match": {
                                            "product_class.id": "U"
                                        }
                                    }
                                }
                            },
                            "weight": 1
                        },
                        {
                            "filter": {
                                "nested": {
                                    "path": "product_class",
                                    "query": {
                                        "match": {
                                            "product_class.id": "C"
                                        }
                                    }
                                }
                            },
                            "weight": 1
                        }
                    ],
                    "score_mode": "multiply",
                    "boost_mode": "multiply",
                }
            }
        }

    else:
        return {
            "size": 50,
            "query": {
                "function_score": {
                    "query": {
                        "bool": {
                            "should": [
                                {
                                    "nested": {
                                        "path": "product_name",
                                        "query": {
                                            "match": {
                                                "product_name.name": {
                                                    "query": search_term,
                                                    "boost": 2
                                                }
                                            }
                                        }
                                    }
                                },
                                {
                                    "nested": {
                                        "path": "brand",
                                        "query": {
                                            "match": {
                                                "brand.name": {
                                                    "query": search_term,
                                                    "boost": 3
                                                }
                                            }
                                        }
                                    }
                                },
                                {
                                    "match": {
                                        "variety_name": {
                                            "query": search_term,
                                            "boost": 1
                                        }
                                    }
                                },
                                {
                                    "nested": {
                                        "path": "measure_unit",
                                        "query": {
                                            "match": {
                                                "measure_unit.name": {
                                                    "query": search_term,
                                                    "boost": 1
                                                }
                                            }
                                        }
                                    }
                                },
                            ]
                        }
                    },
                    "boost": 3,
                    "functions": [
                        {
                            "filter": {
                                "nested": {
                                    "path": "product_class",
                                    "query": {
                                        "match": {
                                            "product_class.id": "W"
                                        }
                                    }
                                }
                            },
                            "weight": 5
                        },
                        {
                            "filter": {
                                "nested": {
                                    "path": "product_class",
                                    "query": {
                                        "match": {
                                            "product_class.id": "V"
                                        }
                                    }
                                }
                            },
                            "weight": 5
                        },
                        {
                            "filter": {
                                "nested": {
                                    "path": "product_class",
                                    "query": {
                                        "match": {
                                            "product_class.id": "U"
                                        }
                                    }
                                }
                            },
                            "weight": 1
                        },
                        {
                            "filter": {
                                "nested": {
                                    "path": "product_class",
                                    "query": {
                                        "match": {
                                            "product_class.id": "C"
                                        }
                                    }
                                }
                            },
                            "weight": 1
                        }
                    ],
                    "score_mode": "multiply",
                    "boost_mode": "multiply",
                }
            }
        }
    
def store_products_query_test(search_term, store):
    measure_unit_list = extract_number_token_from_query(search_term)

    measure_unit = None

    if len(measure_unit_list) > 0:
        measure_unit = Decimal(measure_unit_list[0])
        query_stores = {
            "size": 50,
            "min_score": 15,
            "sort": [
                {
                    "product.product_class.id": {
                        "order": "desc",
                        "nested": {
                            "path": "product.product_class",
                            "nested": {
                                "path": "product"
                            }
                        }
                    }
                },
                "_score"
            ],
            "query": {
                "function_score": {
                    "query": {
                        "bool": {
                            "must": {
                                "term": {
                                    "store": store
                                }
                            },
                            "should": [
                                {
                                    "nested": {
                                        "path": "product",
                                        "query": {
                                            "nested": {
                                                "path": "product.product_name",
                                                "query": {
                                                    "match": {
                                                        "product.product_name.name": {
                                                            "query": search_term,
                                                            "boost": 2
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                {
                                    "nested": {
                                        "path": "product",
                                        "query": {
                                            "nested": {
                                                "path": "product.brand",
                                                "query": {
                                                    "match": {
                                                        "product.brand.name": {
                                                            "query": search_term,
                                                            "boost": 3
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                {
                                    "nested": {
                                        "path": "product",
                                        "query": {
                                            "match": {
                                                "product.variety_name": {
                                                    "query": search_term,
                                                    "boost": 1
                                                }
                                            }
                                        }
                                    }
                                },
                                {
                                    "nested": {
                                        "path": "product",
                                        "query": {'nested': {
                                            'path': 'product.measure_unit',
                                            'query': {
                                                    "match": {
                                                        "product.measure_unit.name": {
                                                            "query": search_term,
                                                            "boost": 1
                                                        }
                                                    }
                                                }
                                            }
                                        },
                                    }
                                },
                                {
                                    "nested": {
                                        "path": "product",
                                        "query": {
                                            "term": {
                                                "product.quantity": measure_unit
                                            }
                                        }
                                    }
                                },
                                {
                                    "nested": {
                                        "path": "product",
                                        "query": {
                                            "match": {
                                                "product.create_description": {
                                                    "query": search_term,
                                                    "boost": 2
                                                }
                                            }
                                        }
                                    }
                                },
                            ]
                        }
                    },
                    "boost_mode": "sum"
                }
            }
        }
    else:
            query_stores = {
                "size": 50,
                "min_score": 15,
                "sort": [
                    {
                        "product.product_class.id": {
                            "order": "desc",
                            "nested": {
                                "path": "product.product_class",
                                "nested": {
                                    "path": "product"
                                }
                            }
                        }
                    },
                    "_score"
                ],
                "query": {
                    "function_score": {
                        "query": {
                            "bool": {
                                "must": {
                                    "term": {
                                        "store": store
                                    }
                                },
                                "should": [
                                    {
                                        "nested": {
                                            "path": "product",
                                            "query": {
                                                "nested": {
                                                    "path": "product.product_name",
                                                    "query": {
                                                        "match": {
                                                            "product.product_name.name": {
                                                                "query": search_term,
                                                                "boost": 2
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    {
                                        "nested": {
                                            "path": "product",
                                            "query": {
                                                "nested": {
                                                    "path": "product.brand",
                                                    "query": {
                                                        "match": {
                                                            "product.brand.name": {
                                                                "query": search_term,
                                                                "boost": 3
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    {
                                        "nested": {
                                            "path": "product",
                                            "query": {
                                                "match": {
                                                    "product.variety_name": {
                                                        "query": search_term,
                                                        "boost": 1
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    {
                                        "nested": {
                                            "path": "product",
                                            "query": {'nested': {
                                                'path': 'product.measure_unit',
                                                'query': {
                                                        "match": {
                                                            "product.measure_unit.name": {
                                                                "query": search_term,
                                                                "boost": 1
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                        }
                                    },
                                    {
                                        "nested": {
                                            "path": "product",
                                            "query": {
                                                "match": {
                                                    "product.create_description": {
                                                        "query": search_term,
                                                        "boost": 2
                                                    }
                                                }
                                            }
                                        }
                                    },
                                ]
                            }
                        },
                        "boost_mode": "sum"
                    }
                }
            }

    
    return query_stores

def store_products_query(search_term, store):
    measure_unit_list = extract_number_token_from_query(search_term)

    measure_unit = None

    if len(measure_unit_list) > 0:
        measure_unit = Decimal(measure_unit_list[0])
        query_stores = {
            "min_score": 50,
            "query": {
                "function_score": {
                    "query": {
                        "bool": {
                            "must": {
                                "term": {
                                    "store": store
                                }
                            },
                            "should": [
                                {
                                    "nested": {
                                        "path": "product",
                                        "query": {
                                            "nested": {
                                                "path": "product.product_name",
                                                "query": {
                                                    "match": {
                                                        "product.product_name.name": {
                                                            "query": search_term,
                                                            "boost": 2
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                {
                                    "nested": {
                                        "path": "product",
                                        "query": {
                                            "nested": {
                                                "path": "product.brand",
                                                "query": {
                                                    "match": {
                                                        "product.brand.name": {
                                                            "query": search_term,
                                                            "boost": 3
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                {
                                    "nested": {
                                        "path": "product",
                                        "query": {
                                            "match": {
                                                "product.variety_name": {
                                                    "query": search_term,
                                                    "boost": 1
                                                }
                                            }
                                        }
                                    }
                                },
                                {
                                    "nested": {
                                        "path": "product",
                                        "query": {'nested': {
                                            'path': 'product.measure_unit',
                                            'query': {
                                                    "match": {
                                                        "product.measure_unit.name": {
                                                            "query": search_term,
                                                            "boost": 1
                                                        }
                                                    }
                                                }
                                            }
                                        },
                                    }
                                },
                                {
                                    "nested": {
                                        "path": "product",
                                        "query": {
                                            "term": {
                                                "product.quantity": measure_unit
                                            }
                                        }
                                    }
                                },
                                {
                                    "nested": {
                                        "path": "product",
                                        "query": {
                                            "match": {
                                                "product.create_description": {
                                                    "query": search_term,
                                                    "boost": 2
                                                }
                                            }
                                        }
                                    }
                                },
                            ]
                        }
                    },
                    "boost": 3,
                    "functions": [
                        {
                            "filter": {
                                "nested": {
                                    "path": "product",
                                    "query": {
                                        "nested": {
                                            "path": "product.product_class",
                                            "query": {
                                                "match": {
                                                    "product.product_class.id": "W"
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "weight": 5
                        },
                        {
                            "filter": {
                                "nested": {
                                    "path": "product",
                                    "query": {
                                        "nested": {
                                            "path": "product.product_class",
                                            "query": {
                                                "match": {
                                                    "product.product_class.id": "V"
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "weight": 5
                        },
                        {
                            "filter": {
                                "nested": {
                                    "path": "product",
                                    "query": {
                                        "nested": {
                                            "path": "product.product_class",
                                            "query": {
                                                "match": {
                                                    "product.product_class.id": "U"
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "weight": 1
                        },
                        {
                            "filter": {
                                "nested": {
                                    "path": "product",
                                    "query": {
                                        "nested": {
                                            "path": "product.product_class",
                                            "query": {
                                                "match": {
                                                    "product.product_class.id": "C"
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "weight": 1
                        }
                    ],
                    "score_mode": "multiply",
                    "boost_mode": "multiply"
                }
            }
        }
    else:
            query_stores = {
                "min_score": 50,
                "query": {
                    "function_score": {
                        "query": {
                            "bool": {
                                "must": {
                                    "term": {
                                        "store": store
                                    }
                                },
                                "should": [
                                    {
                                        "nested": {
                                            "path": "product",
                                            "query": {
                                                "nested": {
                                                    "path": "product.product_name",
                                                    "query": {
                                                        "match": {
                                                            "product.product_name.name": {
                                                                "query": search_term,
                                                                "boost": 2
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    {
                                        "nested": {
                                            "path": "product",
                                            "query": {
                                                "nested": {
                                                    "path": "product.brand",
                                                    "query": {
                                                        "match": {
                                                            "product.brand.name": {
                                                                "query": search_term,
                                                                "boost": 3
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    {
                                        "nested": {
                                            "path": "product",
                                            "query": {
                                                "match": {
                                                    "product.variety_name": {
                                                        "query": search_term,
                                                        "boost": 1
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    {
                                        "nested": {
                                            "path": "product",
                                            "query": {'nested': {
                                                'path': 'product.measure_unit',
                                                'query': {
                                                        "match": {
                                                            "product.measure_unit.name": {
                                                                "query": search_term,
                                                                "boost": 1
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                        }
                                    },
                                    {
                                        "nested": {
                                            "path": "product",
                                            "query": {
                                                "match": {
                                                    "product.create_description": {
                                                        "query": search_term,
                                                        "boost": 2
                                                    }
                                                }
                                            }
                                        }
                                    },
                                ]
                            }
                        },
                        "boost": 3,
                        "functions": [
                            {
                                "filter": {
                                    "nested": {
                                        "path": "product",
                                        "query": {
                                            "nested": {
                                                "path": "product.product_class",
                                                "query": {
                                                    "match": {
                                                        "product.product_class.id": "W"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                "weight": 3
                            },
                            {
                                "filter": {
                                    "nested": {
                                        "path": "product",
                                        "query": {
                                            "nested": {
                                                "path": "product.product_class",
                                                "query": {
                                                    "match": {
                                                        "product.product_class.id": "V"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                "weight": 3
                            },
                            {
                                "filter": {
                                    "nested": {
                                        "path": "product",
                                        "query": {
                                            "nested": {
                                                "path": "product.product_class",
                                                "query": {
                                                    "match": {
                                                        "product.product_class.id": "U"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                "weight": 1
                            },
                            {
                                "filter": {
                                    "nested": {
                                        "path": "product",
                                        "query": {
                                            "nested": {
                                                "path": "product.product_class",
                                                "query": {
                                                    "match": {
                                                        "product.product_class.id": "C"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                "weight": 1
                            }
                        ],
                        "score_mode": "multiply",
                        "boost_mode": "multiply"
                    }
                }
            }

    
    return query_stores

def numeric_products_query(eanid):
     return {
        "query": {
            "query_string":{  
                "default_field": "eanid",
                "query": f"*{eanid}*"
            }
        }
    }

def numeric_store_products_query(eanid, store):
    if len(eanid)<8:
        return {
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "store": store
                            },
                        },
                        {
                            "term":    {
                                "internal_code": int(eanid)
                            } 
                        },
                    ],
                },
            }
        }
    else:
        return {
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "store": store
                            },
                        },
                        {
                            "nested": {
                                "path": "product",
                                "query": {
                                        "query_string": {  
                                            "default_field": "product.eanid",
                                            "query": f"*{eanid}*"
                                        }
                                    }
                                }
                        }, 
                    ],
                },
            }
        }
    

def query_products_test_2(search_term):
     return{
    "size": 50,
    "sort": [
    {
        "product_class.id": {
            "order": "desc",
            "nested": {
                "path": "product_class"
            }
        }
    },
    "_score"
    ],
    "query": {
        "bool": {
        "should": [
            {
                "multi_match": {
                    "query": search_term,
                    "fields": ["product_name.name", "brand.name^2", "variety_name"],
                    "type": "cross_fields",
                    "minimum_should_match": "90%"
                }
            },
            {
                "nested": {
                    "path": "product_name",
                    "query": {
                    "multi_match": {
                            "query": search_term,
                            "fields": ["product_name.name", "brand.name^2", "variety_name"],
                            "type": "cross_fields",
                            "minimum_should_match": "100%"
                        }
                    },
                }
            },
            {
                "nested": {
                    "path": "brand",
                    "query": {
                        "multi_match": {
                            "query": search_term,
                            "fields": ["product_name.name", "brand.name^2", "variety_name"],
                            "type": "cross_fields",
                            "minimum_should_match": "100%"
                        }
                    },
                }
            }
        ],
        "minimum_should_match": 1
        }
    }
    }

def query_products_test_3(search_term):
     return {
        "size": 50,
        "sort": [
        {
            "product_class.id": {
                "order": "desc",
                "nested": {
                    "path": "product_class"
                }
            }
        },
        "_score"
        ],
        "query": {
            "bool": {
            "should": [
                {
                    "nested": {
                        "path": "product_name",
                        "query": {
                            "query_string":{  
                                "default_field": "product_name.name",
                                "query": f"*{search_term}*"
                            }
                        },
                    }
                },
                {
                    "nested": {
                        "path": "brand",
                        "query": {
                            "query_string":{  
                                "default_field": "brand.name",
                                "query": f"*{search_term}*"
                            }
                        },
                    }
                },
                {
                    "query_string": {  
                        "default_field": "variety_name",
                        "query": f"*{search_term}*"
                    }
                },
            ],
            "minimum_should_match": 1
            }
        }
    }