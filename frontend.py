import json
import jsonschema

def from_json(data: str, schema: str = None):
    data = json.loads(data)
    if schema:
        jsonschema.validate(instance=data, schema=json.loads(schema))
    
    return data

file_extension_to_func = {"json": from_json}