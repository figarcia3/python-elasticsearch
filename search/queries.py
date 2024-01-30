from search.utils import extract_number_token_from_query
from decimal import Decimal

def products_query_test(search_term):
    return {
            "min_score": 5,
            "size": 40,
            "query": {
                "bool": {
                "must": {
                    "multi_match": {
                        "query": search_term,
                        "fields": ["product_name.name", "brand.name", "variety_name"],
                        "type": "cross_fields"
                    }
                },
                "filter": [
                    {
                    "nested": {
                        "path": "product_class",
                        "query": {
                        "terms": {
                            "product_class.id": ["U", "C"]
                        }
                        }
                    }
                    }
                ]
                }
            }
        }

def products_query_weight_test(search_term):
    return {
            "min_score": 5,
            "query": {
                "bool": {
                "must": {
                    "multi_match": {
                        "query": search_term,
                        "fields": ["product_name.name", "brand.name", "variety_name"],
                        "type": "cross_fields"
                    }
                },
                "filter": [
                    {
                    "nested": {
                        "path": "product_class",
                        "query": {
                            "terms": {
                                "product_class.id": ["W", "V"]
                            }
                        }
                    }
                    }
                ]
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
                                                            "boost": 5
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
                                                                "boost": 5
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