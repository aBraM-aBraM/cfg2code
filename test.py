import glob
import os
import subprocess
import frontend

EXAMPLES_DIR = os.path.join(os.path.dirname(__file__),"examples")
SCHEMAS = set(glob.glob(os.path.join(EXAMPLES_DIR, "schema.*")))
EXAMPLES = set(glob.glob(os.path.join(EXAMPLES_DIR, "*"))).difference(SCHEMAS)
EXAMPLES = {group: sorted([x for x in EXAMPLES if group in os.path.basename(x)]) for group in frontend.file_extension_to_frontend.keys()}

def assert_execution(input_file: str, schema_file: str, result: bool):
    try:
        process = subprocess.Popen(f"python3 cfg2code.py {input_file} --schema {schema_file}",
                                    shell=True,
                                        cwd=os.path.dirname(__file__),
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        assert result == (0 == process.wait())
    except AssertionError:
        _, stderr = process.communicate()
        print(f" [X] {frontend} failed!")
        print(stderr.decode())
        raise

if __name__ == "__main__":
    
    for file_group in EXAMPLES:
        fail, success = EXAMPLES[file_group]

        try:
            for schema in SCHEMAS:
                assert_execution(success, schema, True)
                assert_execution(fail, schema, False)
            print(f" [V] {file_group} works!")
        except AssertionError:
            continue
