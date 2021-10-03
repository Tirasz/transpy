import abc
import ast

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