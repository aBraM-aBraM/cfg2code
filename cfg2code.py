import jsonschema
import click
import os

import frontend
import backend

@click.command
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--schema", type=click.Path(exists=True), required=False)
@click.option("--output_file", type=click.Path(), default="out.h")
def main(input_file, schema, output_file):
    frontend_extension = os.path.splitext(input_file)[1][1:]

    try:
        frontend_func = frontend.file_extension_to_func[frontend_extension] 
    except KeyError:
        print(f"Error: {frontend_extension} is not a supported frontend")
        exit(1)

    backend_extension = os.path.splitext(output_file)[1][1:]
    try:
        backend_func = backend.file_extension_to_func[backend_extension]
    except KeyError:
        print(f"Error: {backend} is not a supported backend")
        exit(1)


    schema_data = None
    if schema:
        with open(schema) as schema_file:
            schema_data = schema_file.read()

    data = None
    with open(input_file) as in_file:
        in_file_data = in_file.read()
        data = frontend_func(in_file_data, schema_data)
    
    out_data = backend_func(data)

    with open(output_file, "w") as out_file:
        out_file.write(out_data)


if __name__ == "__main__":
    main()