import abc
import ast


class PatternBase(metaclass=abc.ABCMeta):
    """
    Defines an interface for a transformer plugin. 
    Every transformer should implement:
    visit(node): returns a boolean, true, if the node fits the pattern
    transform(node): returns an ast pattern, that can be used inside an ast.match_case 
    potential_subjects(): returns a set, containing nodes that the pattern recognises as a subject node. (subjects are used for ast.Match)
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'visit') and 
                callable(subclass.visit) and
                hasattr(subclass, 'transform') and
                callable(subclass.transform) and
                hasattr(subclass, 'potential_subjects') and
                callable(subclass.potential_subjects)
                )
