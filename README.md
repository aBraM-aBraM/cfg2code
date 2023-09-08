# cfg2code

suckless config to code converter

receives json as input, jsonschema and converts the json to c header.

The purpose is to simplify configs for c/c++ programs.

## Design

Frontend - parses generic highlevel datatypes like json, yaml etc. to python dictionary
Backend  - parses python dictionary to code like c header, c++ header, rust etc.

This separation between frontend and backend shortens development time (obviously takes inspiration from llvm).
