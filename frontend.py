import json
import jsonschema
import yaml
import pykwalify.core
from dataclasses import dataclass
from typing import Callable

@dataclass
class FrontendDatatype:
    loads: Callable[[str], dict]
    validate: Callable[[str, str], None]

file_extension_to_frontend = {"json": FrontendDatatype(json.loads, lambda data, schema: jsonschema.validate(instance=data, schema=schema)),
                              "yml": FrontendDatatype(lambda data: yaml.load(data, Loader=yaml.SafeLoader), 
                                                      lambda data, schema: pykwalify.core.Core(source_data=data, schema_data=schema).validate())}