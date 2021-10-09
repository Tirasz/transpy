import ast
import pkgutil
import importlib
import inspect
import sys
import plugins
vprint = print if ("-v" in sys.argv[1:]) else lambda *a, **k: None

def load_plugins():
    """Returns a list of objects that implement the Base plugin interface."""
    Plugins = []
    # Loading python modules from plugins folder
    Modules = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules(plugins.__path__, plugins.__name__ + ".")
    }

    for plugin_name in Modules.keys():
        # Checking every class in the module
        for name, cls in inspect.getmembers(Modules[plugin_name], inspect.isclass):
            if issubclass(cls, plugins.Base.TransformerBase):
                Plugins.append(cls())
                vprint(f"PLUGIN: {name} succesfully loaded!")
    return Plugins

class Analyzer(ast.NodeVisitor):
    def __init__(self, transformers):
        self.transformers = transformers
        self.results = {}

    def visit_If(self, node):
        vprint(f"ANALYZER: Found and If, at line number: {node.lineno}")
        for transformer in self.transformers:
            if transformer.visit(node):
                self.results[node] = transformer
        

def main():
    with open("test.py", "r") as src:
        tree = ast.parse(src.read())    

    analyzer = Analyzer(load_plugins())    
    analyzer.visit(tree)
    with open("transformed.py", "w") as out:
        for node in analyzer.results.keys():
            print(f"If node at line number [{node.lineno}] can be transformed with plugin: [{analyzer.results[node].__class__.__name__}]")
            out.write(ast.unparse(analyzer.results[node].transform(node)))
        

if __name__ == "__main__":

    main()
    vprint("Done")

    
