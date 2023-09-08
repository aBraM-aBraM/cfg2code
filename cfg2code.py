import jsonschema
import click
import os

import frontend
import backend

@click.command
@click.argument("input-file", type=click.Path(exists=True))
@click.option("--schema", type=click.Path(exists=True), required=False)
@click.option("--output-file", type=click.Path(), default="out.h")
def main(input_file, schema, output_file):
    frontend_extension = os.path.splitext(input_file)[1][1:]
    schema_extension = os.path.splitext(schema)[1][1:]
    backend_extension = os.path.splitext(output_file)[1][1:]
    

    try:
        load_func = frontend.file_extension_to_frontend[frontend_extension].loads
    except KeyError:
        print(f"Error: {frontend_extension} is not a supported frontend")
        exit(1)

    try:
        schema_datatype = frontend.file_extension_to_frontend[schema_extension]
    except KeyError:
        print(f"Error: {frontend_extension} is not a supported schema frontend")
        exit(1)

    try:
        dump_func = backend.file_extension_to_func[backend_extension]
    except KeyError:
        print(f"Error: {backend} is not a supported backend")
        exit(1)

    data = None
    with open(input_file) as in_file:
        in_file_data = in_file.read()
        data = load_func(in_file_data)


    schema_data = None
    if schema:
        with open(schema) as schema_file:
            schema_data = schema_file.read()
            schema_data = schema_datatype.loads(schema_data)
        schema_datatype.validate(data, schema_data)

    out_data = dump_func(data)

    with open(output_file, "w") as out_file:
        out_file.write(out_data)


if __name__ == "__main__":
    main()