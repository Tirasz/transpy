import ast
from copy import deepcopy
from analyzer import Transformer, log_config
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
parser.add_argument('-s', '--silent',          dest='silent',  action='store_const', const=True,     default=False,  help="prevents transpy from generating 'path/transpy-logs'")
parser.add_argument('-gd','--generate-diffs',  dest='gen_di',  action='store_const', const=True,     default=False,  help="generates diff file in 'path/transpy-logs/'")



def transform_helper(file):
    tr = Transformer()
    tr.transform(file)

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
    files_to_transform = []
    ow = args.ow

    if not path.exists():
        parser.error("Given path does not exist!")
    if args.silent and args.gen_di:
        parser.error("Cannot generate diffs while in silent mode!")


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
    if not args.silent:
        logs_dir = (path / 'transpy-logs') if path.is_dir() else (path.parent / 'transpy-logs')
        os.mkdir(logs_dir)
        log_config["LOGS"] = logs_dir
        if args.gen_di:
            log_config["DIFFS"] = (logs_dir / 'diffs.diff')

    print(f"Transforming files: ")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(transform_helper, files_to_transform), total=len(files_to_transform)))


if __name__ == "__main__":
    main()