import ast
from copy import deepcopy
from analyzer import Transformer, init_output
import os, glob
import argparse
import shutil
from pathlib import Path
import concurrent.futures 
import threading
from tqdm import tqdm
import time
from datetime import timedelta
from memory_profiler import memory_usage
import json
import subprocess

parser = argparse.ArgumentParser(description="Analyzes and transforms python projects.")
parser.add_argument("path", metavar='PATH', type=str, nargs=1, help="path to the directory / python file")
parser.add_argument('-i', '--inline',          dest='mode',    action='store_const', const="inline", default="copy", help='transform inline (default makes a copy)')
parser.add_argument('-o', '--overwrite',       dest='ow',      action='store_const', const="Y",      default=None,   help="automatically overwrite files, when not transforming inline")
parser.add_argument('-t', '--test',            dest='test',   action='store_const', const=True,      default=False,   help="run in test mode, provides additional info on runtime and memory usage, etc.")
parser.add_argument('-mt','--max-threads',dest='max_threads', const=None, default=None, type=int, help='maximum number of threads to use', nargs=1)

TEST_DATA = {
    "project_size_MiB" : 0, 
    "no_files" : 0,
    "cloc_py": {},
    "no_nodes_visited" : 0,
    "no_nodes_transformed" : 0,
    "runtime_s" : 0,
    "max_memory_MiB" : 0
}

def cloc(path):
    CLOC = subprocess.run(['cloc', path], stdout=subprocess.PIPE).stdout.decode('utf-8')
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


def test_helper(path):
    global TEST_DATA
    files_to_transform = [f for f in path.rglob('*.py')] if path.is_dir() else [path]
    init_output(path)

    TEST_DATA["no_files"] = len(files_to_transform)
    print(f"Transforming files: ")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(transform_helper, files_to_transform), total=len(files_to_transform)))

    for res in results:
        TEST_DATA["no_nodes_visited"] += res[0]
        TEST_DATA["no_nodes_transformed"] += res[1]
    return 


def transform_helper(file):
    tr = Transformer()
    tr.transform(file)
    return (tr.visited_nodes, len(tr.results.keys()))

def make_copy(schizo, newPath):
    prompt = "Overwriting" if newPath.exists() else "Creating"
    print(f"{prompt} '{newPath}'")
    path = schizo[0]
    if path.is_dir():
        if newPath.exists():
            shutil.rmtree(newPath)
        schizo[0] = shutil.copytree(path, newPath)
    else:
        schizo[0] = shutil.copy(path,newPath)

def main():
    args = parser.parse_args()
    path = Path(args.path[0]).resolve()
    max_threads = args.max_threads[0] if args.max_threads is not None else None
    ow = args.ow
    test_mode = args.test
    files_to_transform = []
    

    if not path.exists():
        parser.error("Given path does not exist!")

    if max_threads is not None and max_threads <= 0:
        parser.error(f"You want to use {max_threads} threads, huh?")

    if args.mode == "copy":
        newPath = (path.parent / f"transformed-{path.parts[-1]}")
        if newPath.exists():
            while not (ow == "Y" or ow == "N"):
                prompt = "Directory" if path.is_dir() else "File"
                ow = input(f">> {prompt} '{newPath}' already exists! Want to overwrite? (Y/N)\n")
                
            if ow == "N":
                print("Quitting")
                return
        
        path = [path]
        #make_copy(path, newPath)
        thread = threading.Thread(target = make_copy, args = (path, newPath), name="Copying thread")
        thread.start()
        eli_count = 0
        while thread.is_alive():
            print('Copying files', '.'*(eli_count+1), ' '*(2-eli_count), end='\r')
            eli_count = (eli_count + 1) % 3
            time.sleep(0.1)
        thread.join()
        path = path[0]
        print('Done                 ')


    if test_mode:
        global TEST_DATA
        start_time = time.monotonic()
        mem = max(memory_usage((test_helper, (path,), {})))
        end_time = time.monotonic()
        TEST_DATA["runtime_s"] = timedelta(seconds=end_time - start_time).total_seconds()
        TEST_DATA["max_memory_MiB"] = mem 
        TEST_DATA["project_size_MiB"] = get_size(path) / 1048576 # get size returns bytes, 1 MiB = 2^20 bytes which is 1048576
        TEST_DATA["cloc_py"] = cloc(path)
        
        print(f"Writing test data in: {path / f'TEST_DATA.json'}")
        with open(path / f"TEST_DATA.json", "w") as f:
            json.dump(TEST_DATA, f, indent=4)
    else:
        files_to_transform = [f for f in path.rglob('*.py')] if path.is_dir() else [path]
        init_output(path)
        print(f"Transforming files: ")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(tqdm(executor.map(transform_helper, files_to_transform), total=len(files_to_transform)))
   

if __name__ == "__main__":
    main()


