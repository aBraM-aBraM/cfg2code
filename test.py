import json
import glob
import os
import subprocess

EXAMPLES_DIR = os.path.join(os.path.dirname(__file__),"examples")
EXAMPLES = glob.glob(os.path.join(EXAMPLES_DIR, "*"))

file_groups = dict()

for filename in os.listdir(EXAMPLES_DIR):
    if os.path.isfile(os.path.join(EXAMPLES_DIR, filename)):
        
        file_extension = os.path.splitext(filename)[1]
        
        if file_groups.get(file_extension) is None:
            file_groups[file_extension] = []

        file_groups[file_extension].append(os.path.join(EXAMPLES_DIR, filename))

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
    
    for file_group in file_groups:
        file_groups[file_group] = sorted(file_groups[file_group])
        frontend = file_group[1:]
        fail, schema, success = file_groups[file_group]

        try:
            assert_execution(success, schema, True)
            assert_execution(fail, schema, False)
            print(f" [V] {frontend} works!")
        except AssertionError:
            continue