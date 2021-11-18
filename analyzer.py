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
    Patterns = None

    def __init__(self):
        self.branches = {} # Mapping If-nodes to a list of its branches. !!Only contains transformable if-nodes!!
        self.patterns = {} # Mapping branches to a pattern
        self.subjects = {} # Mapping the If-node to its selected subject !!Only contains transformable if-nodes!!
        
    def visit_If(self, node):
        self.branches[node] = get_branches(node)
        for branch in self.branches[node]:
                print(f"ANALYZER: BRANCH({branch.body[0].lineno-1})")
                if branch.test is None:
                    print(f"ANALYZER: TEST IS NONE. SKIPPING")
                    continue

                # Determine the main pattern of the branch
                for pattern in Analyzer.Patterns:
                    curr_pattern = pattern()
                    if curr_pattern.visit(branch.test):
                        self.patterns[branch] = curr_pattern
                        print(f"ANALYZER: ({ast.unparse(branch.test)}) RECOGNISED BY: {type(curr_pattern).__name__}")
                        break

                # If no pattern recognises the branch, then delete the whole if node from the dict and return
                if branch not in self.patterns.keys():
                    print(f"ANALYZER: NO PATTERN RECOGNISES BRANCH({branch.body[0].lineno -1})")
                    del self.branches[node]
                    return
                
                print(f"ANALYZER: BRANCH({branch.body[0].lineno-1}) RECOGNISED BY: {type(self.patterns[branch]).__name__}")

        # An if-node can be transformed, if all of its branches are recognised patterns, and these patterns can all recognise the same subject.
        # Intersecting the possible subjects for each branch
        potential_subjects = self.patterns[self.branches[node][0]].potential_subjects().copy()
        # Skipping "else:" branch
        for branch in [b for b in self.branches[node] if b.test is not None]:
            potential_subjects.intersection(self.patterns[branch].potential_subjects())
 
        if len(potential_subjects) == 0:
            print(f"ANALYZER: NO COMMON SUBJECT FOR IF-NODE AT: ({node.test.lineno})")
            del self.branches[node]
            return
        elif len(potential_subjects) > 1:
            print(f"ANALYZER: MORE THAN ONE COMMON SUBJECT FOR IF-NODE AT: ({node.test.lineno})")
        self.subjects[node] = potential_subjects.pop()
        print(f"ANALYZER: IF-NODE AT ({node.test.lineno}) HAS POTENTIAL SUBJECT: ({ast.unparse(self.subjects[node])})")



def main():
    Analyzer.Patterns = tuple(load_patterns())
    for pattern in Analyzer.Patterns:
        pattern.Patterns = Analyzer.Patterns
    
    with open("test.py", "r") as src:
        tree = ast.parse(src.read())    

    analyzer = Analyzer()    
    analyzer.visit(tree)
    with open("transformed.py", "w") as out:
        for ifNode, subjectNode in analyzer.subjects.items():
            _cases = []
            out.write("#" + "-"*10 + str(ifNode.lineno) + "-"*10 + f"[{type(subjectNode).__name__}]" +"\n")
            for branch in analyzer.branches[ifNode]:
                if branch.test is not None:
                    pattern = analyzer.patterns[branch]
                    transformed_branch = ast.match_case(pattern = pattern.transform(subjectNode), guard = pattern.guard(subjectNode), body = branch.body)
                else:
                    transformed_branch = ast.match_case(pattern = ast.MatchAs(), guard = None, body = branch.body)

                _cases.append(transformed_branch)

            transformed_node = ast.Match(subject = subjectNode, cases = _cases)
            out.write(ast.unparse(transformed_node) + "\n")



if __name__ == "__main__":
    main()


    
