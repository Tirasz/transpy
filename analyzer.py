import ast
def custom_hash(self):
    return hash(ast.dump(self))

def custom_eq(self, other):
    return hash(self) == hash(other)

ast.AST.__hash__ = custom_hash
ast.AST.__eq__ = custom_eq

import pkgutil
import importlib
import inspect
import patterns
from patterns.Base import get_branches, simplify

def load_plugins():
    """Returns a list of objects that implement the Base plugin interface."""
    Plugins = []
    # Loading python modules from plugins folder
    Modules = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules(patterns.__path__, patterns.__name__ + ".")
    }
    for plugin_name in Modules.keys():
        # Checking every class in the module
        for name, cls in inspect.getmembers(Modules[plugin_name], inspect.isclass):
            if issubclass(cls, patterns.Base.PatternBase):
                Plugins.append(cls())
                print(f"PLUGIN: {name} succesfully loaded!")
    return Plugins

class Analyzer(ast.NodeVisitor):
    def __init__(self, transformers):
        self.transformers = transformers
        self.branches = {} # Mapping If-nodes to a list of its branches
    def visit_If(self, node):
        self.branches[node] = get_branches(node)
        # Removing unnecessary parentheses from BoolOp-s 
        for branch in self.branches[node]:
            if isinstance(branch.test, ast.BoolOp):
                branch.test = simplify(branch.test)


def main():
    with open("test.py", "r") as src:
        tree = ast.parse(src.read())    

    analyzer = Analyzer(load_plugins())    
    analyzer.visit(tree)
        

if __name__ == "__main__":
    main()


    
