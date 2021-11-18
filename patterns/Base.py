import abc
import ast


class PatternBase(metaclass=abc.ABCMeta):
    """
    Defines an interface for a transformer plugin. 
    Every transformer should implement:
    visit(node): returns a boolean, true, if the node fits the pattern
    transform(node): returns an ast pattern, that can be used inside an ast.match_case 
    guard(subjectNode): Returns an expression, to put in guard. Can be different based on chosen subjectNode.
    potential_subjects(): returns a set, containing nodes that the pattern recognises as a subject node. (subjects are used for ast.Match)
    Every valid pattern class gets a static attribute 'Patterns', which is a tuple of all valid Pattern classes. This can be used to recognise sub-patterns.
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'visit') and 
                callable(subclass.visit) and
                hasattr(subclass, 'transform') and
                callable(subclass.transform) and
                hasattr(subclass, 'potential_subjects') and
                callable(subclass.potential_subjects) and
                hasattr(subclass, 'guard') and
                callable(subclass.guard)
                )
