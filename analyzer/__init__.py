import ast
# TODO maybe not like this
def custom_hash(self):
    return hash(ast.dump(self))

def custom_eq(self, other):
    return hash(self) == hash(other)

ast.AST.__hash__ = custom_hash
ast.AST.__eq__ = custom_eq

from pathlib import Path
from configparser import ConfigParser
import os
import glob
import shutil

conf_file = Path(__file__).parent / 'config.ini'
config = ConfigParser()
config.read(conf_file)

from .analyzer import Analyzer
from .transformer import Transformer
from .utils import OutputHandler


def init_output(default_path):
    if not config["OUTPUT"].getboolean("AllowOutput"):
        return
    
    print(f"Output is enabled!")
    output_dir = config["OUTPUT"]["OutputFolderPath"]
    if not (Path(output_dir).exists() and Path(output_dir).is_dir()):
        output_dir = (default_path) if default_path.is_dir() else (default_path.parent)
    
    output_dir = (Path(output_dir) / 'transpy-output').resolve()

    print(f"Output directory is: '{output_dir}'")
    try:
        os.mkdir(output_dir)
        os.mkdir(output_dir / 'diffs')
    except FileExistsError:
        print(f"Output directory already exists! Deleting..")
        shutil.rmtree(output_dir)
        os.mkdir(output_dir)
    OutputHandler.OUTPUT_FOLDER = output_dir