from search.utils import extract_number_token_from_query
from decimal import Decimal


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
                                                    "boost": 2
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
                                                    "boost": 2
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

def store_products_query(search_term, store):
    measure_unit_list = extract_number_token_from_query(search_term)

    measure_unit = None

    if len(measure_unit_list) > 0:
        measure_unit = Decimal(measure_unit_list[0])
        query_stores = {
            "size": 50,
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
                "size": 50,
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

    
    return query_stores

def numeric_products_query(eanid):
     print('numeric_products_query: ', eanid)
     return {
        "query": {
            "query_string":{  
                "default_field": "eanid",
                "query": f"*{eanid}*"
            }
        }
    }

def numeric_store_products_query(eanid, store):
    print('numeric_store_products_query: ', eanid)
    print('numeric_store_products_query: ', store)
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