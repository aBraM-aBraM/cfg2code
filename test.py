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

if __name__ == "__main__":
    
    for file_group in file_groups:
        file_groups[file_group] = sorted(file_groups[file_group])
        frontend = file_group[1:]
        fail, schema, success = file_groups[file_group]

        try:
            assert 0 == subprocess.Popen(f"python3 cfg2code.py {success} --schema {schema}",
                                        shell=True,
                                            cwd=os.path.dirname(__file__),
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE).wait()
            assert 0 != subprocess.Popen(f"python3 cfg2code.py {fail} --schema {schema}",
                                        shell=True,
                                            cwd=os.path.dirname(__file__),
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE).wait()
            print(f" [V] {frontend} works!")
        except AssertionError:
            print(f" [X] {frontend} failed!")