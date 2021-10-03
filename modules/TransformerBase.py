import abc
import ast

class TransformerBase(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'visit') and 
                callable(subclass.visit) and
                hasattr(subclass, 'transform') and
                callable(subclass.transform))