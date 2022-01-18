import ast
import importlib
import pkgutil
import inspect
import patterns

def load_patterns():
    """Returns a list of valid pattern classes"""
    result = []
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
                result.append(cls)
                print(f"LOAD_PATTERN: {name} succesfully loaded!")
    return result
    
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
    '''Removes unnecessary parentheses from a BoolOp node, and returns a new BoolOp node'''
    new_values = []
    for value in node.values:
        for n in _simplify(value, node):
            new_values.append(n)
    return ast.BoolOp(node.op, new_values)

class Branch:
    def __init__(self, body, test = None):
        self.test = test
        self.body = body
        self.nested_Ifs = {} # Mapping every nested If-node to its list of branches
        for node in self.body:
            if isinstance(node, ast.If):
                self.nested_Ifs[node] = get_branches(node)

    def get_preNest(self, nested_IfNode):
        """Returns a list of nodes from the branches body, that appear before the given nested If-node"""
        if not isinstance(nested_IfNode, ast.If) or nested_IfNode not in self.nested_Ifs.keys():
            raise ValueError(f"Given If-node: ({ast.unparse(nested_IfNode.test)}) is not nested inside this branch: ({ast.unparse(self.test)})")
        
        preNest = []
        for i in range(len(self.body)):
            if self.body[i] == nested_IfNode:
                break
            else:
                preNest.append(self.body[i])
        return preNest

    def get_postNest(self, nested_IfNode):
        """Returns a list of nodes from the branches body, that appear after the given nested If-node"""
        if not isinstance(nested_IfNode, ast.If) or nested_IfNode not in self.nested_Ifs.keys():
            raise ValueError(f"Given If-node: ({ast.unparse(nested_IfNode.test)}) is not nested inside this branch: ({ast.unparse(self.test)})")

        postNest = []
        flag = False
        for i in range(len(self.body)):
            if self.body[i] == nested_IfNode:
                flag = True
                continue
            if flag:
                postNest.append(self.body[i])
        return postNest

    

def get_branches(node) :
    """Returns a list of Branches for each branch of the given 'If' node"""
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

def flatten(branch):
    """Tries to flatten the branch. Returns a list of the flattened sub-branches. Return None if flattening is not possible. """
    if branch.test is None:
        return None
        
    preNest = []
    postNest = []
    nestedIf = None
    for node in branch.body:
        # Looping through every node in the branches body
        if isinstance(node, ast.If): # An If-node is found
            if nestedIf is not None: # If its not the only nested If-node
                return None
            nestedIf = node
            continue

        if nestedIf is None: # node is not an If-node, and we havent found one yet
            preNest.append(node)
        else:
            postNest.append(node) # node is not an If-node, and we have already found one

    if nestedIf is None:
        return None

    mainTest = branch.test
    nestedBranches = get_branches(nestedIf)
    flattened = []

    for branch in nestedBranches:
        newBody = preNest + branch.body + postNest
        newTest = ast.BoolOp(ast.And(), [mainTest])
        if branch.test is not None:
            newTest.values.append(branch.test)
            newTest = simplify(newTest)
        flattened.append(Branch(newBody, newTest))
    
    return flattened