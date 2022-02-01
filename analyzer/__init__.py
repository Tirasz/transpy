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

conf_file = Path(__file__).parent / 'config.ini'
config = ConfigParser()
config.read(conf_file)

log_config = {}
from .analyzer import Analyzer
from .transformer import Transformer

