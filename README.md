# cfg2code

suckless config to code converter

receives json/yml/etc as input, (optional) validation schema and converts to c/c++/etc header.

The purpose is to simplify configs for c/c++ programs

## Example

examples/success.json

```json
{
    "PersonObject": {
        "name": "Alice Johnson",
        "age": 25,
        "id": "123456789"
    }
}
```

```sh
python3 examples/success.json --schema examplkes/schema.json --output-file out.h
```

```c
struct PersonObject {
	char name[13];
	int age;
	char id[9];
};
```

> Note: you may notice that strings are sized char arrays. This is
> intended with the purpose of compatbility with embedded code without heap

## Design

* Frontend - parses generic highlevel datatypes like json, yaml etc. to python dictionary
* Backend  - parses python dictionary to code like c header, c++ header, rust etc.

This separation between frontend and backend shortens development time (obviously takes inspiration from llvm).
