import ast
# TODO maybe not like this
def custom_hash(self):
    return hash(ast.dump(self))

def custom_eq(self, other):
    return hash(self) == hash(other)

ast.AST.__hash__ = custom_hash
ast.AST.__eq__ = custom_eq

from .analyzer import Analyzer
from .transformer import Transformer

