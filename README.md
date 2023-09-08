# cfg2code

suckless config to code converter

receives json/yml/etc as input, (optional) validation schema and converts to c/c++/etc header.

The purpose is to simplify configs for c/c++ programs

> Note: The schema and input files don't have to be of the same language.
> For example, a yml input file can be validated with a json schema.

## Example

This example is from `examples/success.json`

```json
{
    "name": "Alice Johnson",
    "age": 25,
    "id": "123456789"
}
```

```shell
python3 cfg2code.py examples/success.json --schema examples/schema.json --typename Config --instance my_config
```

```c
struct Config {
        char name[13];
        int age;
        char id[9];
};
typedef struct Config Config;
Config my_config = {"Alice Johnson", 25, "123456789"};
```

> Note: you may notice that strings are sized char arrays. This is
> intended with the purpose of compatbility with embedded code without heap

## Design

* Frontend - parses generic highlevel datatypes like json, yaml etc. to python dictionary
* Backend  - parses python dictionary to code like c header, c++ header, rust etc.

This separation between frontend and backend shortens development time (obviously takes inspiration from llvm).
