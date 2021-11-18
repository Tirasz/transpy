import ast
def custom_hash(self):
    return hash(ast.dump(self))

def custom_eq(self, other):
    return hash(self) == hash(other)

ast.AST.__hash__ = custom_hash
ast.AST.__eq__ = custom_eq

import importlib
import pkgutil
import inspect
import patterns

ValidPatterns = []

def load_patterns():
    """Loads and adds valid pattern implementations to the Base.ValidPatterns list."""
    # Loading python modules from patterns folder
    Modules = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules(patterns.__path__, patterns.__name__ + ".")
    }
    for plugin_name in Modules.keys():
        # Checking every class in the module
        for name, cls in inspect.getmembers(Modules[plugin_name], inspect.isclass):
            #print(f"PLUGIN TEST: {name} : {cls}")
            if issubclass(cls, patterns.Base.PatternBase):
                ValidPatterns.append(cls)
                print(f"PATTERN: {name} succesfully loaded!")

class Branch:
    def __init__(self, body, test = None):
        self.test = test
        self.body = body

def get_branches(node) :
    # Returns a list of Branches for each branch of the given 'If' node
    if not isinstance(node, ast.If):
        raise ValueError(f"Cannot get branches for type: ({node.__class__.__name__})!")

    branches = []
    current = node
    while(True):
        if isinstance(current.test, ast.BoolOp):
            branches.append(Branch(current.body, simplify(current.test)))
        else:
            branches.append(Branch(current.body, current.test))
        #The 'orelse' of an 'If' node can be: 
        match current.orelse:
            case []: # an empty list, if there are no more branches
                return branches
            case [ast.If(test=_, body=_, orelse=_)]: # an 'If' node if there is another branch
                current = current.orelse[0]
            case [*nodes]: # can be a list of nodes, if its the last 'else:' block
                branches.append(Branch(nodes))
                return branches

def _simplify(node, parent):
    # Gets called on each node in the parents BoolOp's values
    new_values = []
    match node:
        case ast.BoolOp(op, [*values]) if op == parent.op: ## If the node is also a boolOp, with the same operator, we can simplify
            for value in values:
                for n in _simplify(value, node):
                    new_values.append(n)
            return new_values
        case ast.BoolOp(op, [*values]): ## If the node is also a BoolOp, with a different operator, try to simplify the node on its own
            new_values.append(simplify(node))
            return new_values
        case _:
            new_values.append(node)
            return new_values

def simplify(node):
    '''Removes unnecessary parentheses from a BoolOp node'''
    new_values = []
    for value in node.values:
        for n in _simplify(value, node):
            new_values.append(n)
    return ast.BoolOp(node.op, new_values)



class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.branches = {} # Mapping If-nodes to a list of its branches
        self.patterns = {} # Mapping branches to a pattern
        
    def visit_If(self, node):
        self.branches[node] = get_branches(node)
        for branch in self.branches[node]:
                # Determine the main pattern of the branch
                for pattern in ValidPatterns:
                    curr_pattern = pattern()
                    if curr_pattern.visit(branch.test):
                        self.patterns[branch] = curr_pattern
                # If no pattern recognises the branch, then delete it from the dict and return
                if branch not in self.patterns.keys():
                    print(f"NO PATTERN RECOGNISES BRANCH({branch.body[0].lineno -1})")
                    del self.branches[node]
                    return
                print(f"BRANCH ({branch.body[0].lineno -1}): {self.patterns[branch]} ==> {self.patterns[branch].get_potential_subjects()}")




def main():
    load_patterns()
    with open("test.py", "r") as src:
        tree = ast.parse(src.read())    

    analyzer = Analyzer()    
    analyzer.visit(tree)


if __name__ == "__main__":
    main()


    
