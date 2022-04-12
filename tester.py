import json
from pathlib import Path, WindowsPath
import subprocess
import os
import shutil
import glob


PROJECTS_PATH_BASE = Path("E:/TRANSPY/projects")
PROJECTS = ["discord.py", "django", "pylint", "pandas", "keras", "InstaPy"]
TRY_THREADS = [1,2,4,6,12]
SAMPLE_SIZE = 3
TEST_DATA_FOLDER = Path("E:/TRANSPY/transpy/test-data")
CLOC_COMMAND = 'E:\TRANSPY\cloc.exe'

def cloc(path):
    CLOC = subprocess.run([CLOC_COMMAND, path], stdout=subprocess.PIPE).stdout.decode('utf-8')
    pythonLine = next(line for line in CLOC.splitlines() if line.strip().startswith("Python"))
    data = [d for d in pythonLine.split(" ") if d]

    return {
        "files" : int(data[1]),
        "blank" : int(data[2]),
        "comment" : int(data[3]),
        "code" : int(data[4])
    }

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


if __name__ == '__main__':
    cloc_data = {}
    size_data = {}
    os.chdir('..')

    for project in PROJECTS:
        path = PROJECTS_PATH_BASE / project
        cloc_data[project] = cloc(path)
        size_data[project] = get_size(path) / 1048576 # get size returns bytes, 1 MiB = 2^20 bytes which is 1048576

        for max_threads in TRY_THREADS:
            for i in range(SAMPLE_SIZE):
                print(f"{i+1}. TEST ON PROJECT {project.upper()} WITH {max_threads} THREADS")
                print("--"*20)
                subprocess.run(["python","transpy",f"{path.resolve()}", "-mt", f"{max_threads}", "-t", "-o", "-p", f"{project}"])
                print("--"*20)


    test_files = [f for f in TEST_DATA_FOLDER.rglob('*.json')]


    # Need to add cloc and size data to json files 
    for file in test_files:
        with open(file, 'r') as f:
            data = json.loads(f.read())
        data['cloc_py'] = cloc_data[data['project']]
        data['project_size_MiB'] = size_data[data['project']]
        with open(file, 'w') as f:
            json.dump(data, f, indent = 4)




