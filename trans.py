import ast
from copy import deepcopy
from analyzer import Transformer
import os, glob
import argparse
import shutil
from pathlib import Path

parser = argparse.ArgumentParser(description="Analyzes and transforms python projects.")
parser.add_argument("path", metavar='PATH', type=str, nargs=1, help="path to the directory / python file")
parser.add_argument('-i', '--inline', dest='mode', action='store_const',
                    const="inline", default="copy",
                    help='transform inline (default makes a copy)')
parser.add_argument('-o', '--overwrite', dest='ow', action='store_const', const="Y", default=None, help="automatically overwrite files, when not transforming inline")



def make_copy(path, newPath):
    prompt = "Overwriting" if newPath.exists() else "Creating"
    print(f"{prompt} '{newPath}'")
    if path.is_dir():
        if newPath.exists():
            shutil.rmtree(newPath)
        return shutil.copytree(path, newPath)
    return shutil.copy(path,newPath)

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
        path = make_copy(path, newPath)

    
    files_to_transform = [f for f in path.rglob('*.py')] if path.is_dir() else [path]
 
    print("The following file(s) will be transformed:")
    for i in range(len(files_to_transform)):
        print(f"{files_to_transform[i]}")




if __name__ == "__main__":
    main()