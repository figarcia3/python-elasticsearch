def transform_json_list(json_list, index_name, mappings):
    transformed_list = []

    for input_json in json_list:
        source_data = {}
        for field in mappings:
            source_data[field] = input_json.get(field, None)

        transformed_json = {
            "_index": index_name,
            "_id": input_json["id"],
            "_source": source_data
        }

        transformed_list.append(transformed_json)

    return transformed_list


def build_doc(source):
    doc = source["_source"]
    doc["id"] = source["_id"]
    return doc
