import abc
import ast


class PatternBase(metaclass=abc.ABCMeta):
    """
    Defines an interface for a transformer plugin. 
    Every transformer should implement a visit(node), and a transform(node) method.
    visit(node): Analyzes the node, and determines if it can be transformed. Returns a boolean.
    transform(node): Returns the transformed node. 
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'visit') and 
                callable(subclass.visit) and
                hasattr(subclass, 'transform') and
                callable(subclass.transform))


class Branch:
    def __init__(self, body, test = None):
        self.test = test
        self.body = body

class SubjectTransformer(ast.NodeTransformer):
    '''
    Replaces the id of every Name node from the given id to a new id
    '''
    def __init__(self, subj_name, new_name):
        self.subj_name = subj_name
        self.new_name = new_name
        
    def visit_Name(self, node):
        if node.id == self.subj_name:
            return ast.Name(id = self.new_name, ctx = node.ctx)
        else:
            return node



def get_branches(node) :
    # Returns a list of Branches for each branch of the given 'If' node
    if not isinstance(node, ast.If):
        raise ValueError(f"Cannot get branches for type: ({node.__class__.__name__})!")

    branches = []
    current = node
    while(True):
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