import abc
import ast
from collections.abc import Sequence

MIN_BRANCHES = 4

class TransformerBase(metaclass=abc.ABCMeta):
    """
    Defines an interface for a transformer module. 
    Every transformer should implement a visit(node), and a transform(node) method.
    visit(node): Analyzes the node, and determines if it can be transformed by the module. Returns a boolean.
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


def get_branches(node) :
    # Returns a list of Branches for each branch of the given 'If' node

    if not isinstance(node, ast.If):
        raise ValueError(f"Cannot get branches for type: ({node.__class__.__name__})!")
    branches = []
    current = node

    while(True):
        #branches.append((current.test, current.body))
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