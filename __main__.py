import ast
from copy import deepcopy
from analyzer import Transformer, init_output, transform_helper
import os, glob
import argparse
import shutil
from pathlib import Path
import concurrent.futures 
import threading
from tqdm import tqdm
import time

parser = argparse.ArgumentParser(description="Analyzes and transforms python projects.")
parser.add_argument("path", metavar='PATH', type=str, nargs=1, help="path to the directory / python file")
parser.add_argument('-i', '--inline',          dest='mode',    action='store_const', const="inline", default="copy", help='transform inline (default makes a copy)')
parser.add_argument('-o', '--overwrite',       dest='ow',      action='store_const', const="Y",      default=None,   help="automatically overwrite files, when not transforming inline")


def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.
    
    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise Exception("Cannot write to file!")



def make_copy(schizo, newPath):
    prompt = "Overwriting" if newPath.exists() else "Creating"
    print(f"{prompt} '{newPath}'")
    path = schizo[0]
    if path.is_dir():
        if newPath.exists():
            shutil.rmtree(newPath, onerror=onerror)
        schizo[0] = shutil.copytree(path, newPath)
    else:
        schizo[0] = shutil.copy(path,newPath)

def main():
    args = parser.parse_args()
    path = Path(args.path[0]).resolve()
    files_to_transform = []
    ow = args.ow

    if not path.exists():
        parser.error("Given path does not exist!")


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

    files_to_transform = [f for f in path.rglob('*.py')] if path.is_dir() else [path]
    init_output(path)

    print(f"Transforming files: ")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(transform_helper, files_to_transform), total=len(files_to_transform)))
        # _ = [executor.submit(transform_helper, file) for file in files_to_transform]

if __name__ == "__main__":
    main()