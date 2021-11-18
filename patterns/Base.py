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
                callable(subclass.transform) and
                hasattr(subclass, 'get_potential_subjects') and
                callable(subclass.get_potential_subjects))
