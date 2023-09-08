import json
import jsonschema
import yaml
import pykwalify.core

def from_json(data: str, schema: str = None):
    data = json.loads(data)
    if schema:
        jsonschema.validate(instance=data, schema=json.loads(schema))
    
    return data

def from_yml(data: str, schema: str = None):
    data = yaml.load(data, Loader=yaml.SafeLoader)
    schema = yaml.load(schema, Loader=yaml.SafeLoader)
    if schema:
        pykwalify.core.Core(source_data=data, schema_data=schema).validate()
    return data

file_extension_to_func = {"json": from_json, "yml": from_yml}