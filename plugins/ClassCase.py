


"""
If the tests root is an OR:
    - It could be a single LiteralOr where the subject is obj.prop
    - Or it could be multiple Cases
If the tests root is an AND:
    - It could be a ClassCase and a GUARD
    - Or its just a single ClassCase

ClassCase(subject = subj):
if [ isinstance(subj, Class) and ] ( LiteralOr(subject = subj.attr) | ClassCase(subject = subj.attr) )+ [ and ClassCase(subject = subj.otherAttr) ]* [ and Guard() ]

LiteralOr(subject = subj):
if subj == Constant [or subj == Constant]*


if isinstance(obj, Class1) and (obj.attr == 1 or obj.attr == 2 or ...) and (obj.attr2.attr1 == 3 or obj.attr2.attr2 == 4)
BoolOp(And, [isinstance(obj, Class1), BoolOp(OR, [obj.attr == 1, obj.attr == 2, ...]), BoolOp(OR, [obj.attr2.attr1 == 3, obj.attr2.attr2 == 4])])

if isinstance(obj, Class2) and (obj.attr1 == 1 or obj.attr1 == 2) and isinstance(obj.attr2, Class1) and obj.attr2.attr2 == 3:
BoolOp(AND, [isinstance(obj, Class2), BoolOp(OR, [obj.attr1 == 1, obj.attr1 == 2]), isinstance(obj.attr2, Class1), obj.attr2.attr2 == 3])
"""



"""
    # LiteralOr(subject = subj):
    #  if subj == Constant [or subj == Constant]* 
    # ClassCase(subject = subj):
    # if [ isinstance(subj, Class) and ] ( LiteralOr(subject = subj.attr) | ClassCase(subject = subj.attr) )+ [ and ClassCase(subject = subj) ]* [ and Guard() ]
    pass




    LiteralOr(subj):
    subj == Constant [OR subj == Constant]*

    ClassCaseBase(subj): --> Class(attr = v1 | v2 | ..., otherAttr = v1 | v2 | ..., attrN = ...)
    [ isinstance(subj, Class) AND ]  LiteralOr(subj.attr) [ AND LiteralOr(subj.otherAttr) ]*
    e.g. ==> 
    isinstance(obj, Class) and ( obj.attr == 2 or obj.attr == 3 ) and (obj.attr2 == 4 or obj.attr2 == 5)           --> subj: obj, class: Class
    isinstance(obj.attr, Class) and (obj.attr.x == 1 or obj.attr.x == 2) and (obj.attr.y == 3 or obj.attr.y == 4)  --> subj: obj.attr, class: Class
    ( obj.attr == 1 or obj.attr == 2) and (obj.attr2 == 3 or obj.attr2 == 4)                                       --> subj: obj, class: object
    
    

    ClassCase(subj): --> Class([attr = constant | Class([attr = constant]*)]*)
    if isinstance(subj, Class) [AND ( LiteralOr(subj.attr) || ClassCaseBase(subj.attr) ) ]*
    e.g. ==>
    if isinstance(obj, Class) and (obj.attr = 2 or obj.attr = 3) and (isinstance(obj.pos, OtherClass) and (obj.pos.x == 2 or obj.pos.x == 3) and (obj.pos.y == 4 or obj.pos.y == 5))

If the tests root is an OR:
    - It could be a single LiteralOr where the subject is obj.prop --> ClassCase with class = 'object' and only attribute "prop"
        - A LiteralCase where the subject is obj.prop
    - Or it could be multiple Cases
        - ClassCase OR LiteralCase OR SomeCase OR ...
    - Otherwise reject

If the tests root is an AND:
    - It could be a ClassCase and a GUARD
    - Or its just a single ClassCase


if isinstance(obj, Class) and ....
    ..
elif obj.prop == 2 or obj.prop == 3 ...
    ..
elif obj.prop.x == 2 or obj.prop.y == 3
"""
import ast
from Base import Branch
from LiteralCase import _get_subject

#TODO: DELETE
def custom_hash(self):
    return hash(ast.dump(self))

def custom_eq(self, other):
    return hash(self) == hash(other)

def custom_repr(self):
    return ast.unparse(self)

ast.AST.__hash__ = custom_hash
ast.AST.__eq__ = custom_eq
ast.AST.__repr__ = custom_repr


def lit_analyze(test):
    # Input is a BoolOp(OR) or a single expression
    # If every node in its values is literal with the same subject return the subject oherwise return false
    match test:
        case ast.BoolOp(ast.Or()):
            potential_subjects = set()
            for node in test.values:
                curr_subj = _get_subject(node, (ast.Eq,))
                if curr_subj:
                    potential_subjects.add(curr_subj)
                    #print(f"({ast.unparse(node)}) : {potential_subjects}")
                else:
                    return False
            if len(potential_subjects) == 1:
                return potential_subjects.pop()
            return False

        case ast.BoolOp(ast.And()):
            return False

        case ast.Compare():
            return _get_subject(test, (ast.Eq,))

        case _:
            return False

def get_potential_subjects(attrNode):
    # For an attribute node, representing "obj.prop.x" returns the set: (obj, obj.prop, obj.prop.x)
    # In some cases, they all could be considered a subject
    potential_subjects = set()
    currNode = attrNode
    potential_subjects.add(currNode)
    while isinstance(currNode, ast.Attribute): 
        potential_subjects.add(currNode.value)
        currNode = currNode.value
    potential_subjects.add(currNode)
    return potential_subjects


class ClassCase():
    def __init__(self):
        self.guards = {}
        pass
    
    def visit(self, branch):
        """Returns with a set of potential subjects for the branch"""
        self.guards[branch] = set()
        match branch.test:
            #If the tests root is an AND:
            # - It could be a ClassCase and a GUARD
            # - Or its just a single ClassCase
            case ast.BoolOp(ast.And(), [*values]):
                potential_subjects = {}
                for node in values:
                    potential_subjects[node] = set()
                    temp = self.visit(Branch(test = node, body = None))
                    if temp is None:
                        #print(f"{node} IS A GUARD!")
                        self.guards[branch].add(node)
                        del potential_subjects[node]
                        continue

                    for sj in temp:
                        if sj:
                            potential_subjects[node].add(sj)
                    #print(f"POTSUBJECTS: '{ast.unparse(node)}': {potential_subjects[node]}")
                res = set()
                for asd in potential_subjects[list(potential_subjects.keys())[0]]:
                    res.add(asd)
                for node in potential_subjects.keys():
                    res = res.intersection(potential_subjects[node])
                    #print(f"RESULTS: {potential_subjects[node]}")
                return res


            # If the tests root is an OR:
            case ast.BoolOp(ast.Or(), [*values]):
                #print(f"BRANCH ({branch.test.lineno}) HAS OR AS ROOT! --> {branch.test}")
                    # It could be a single LiteralOr where the subject is obj.prop --> ClassCase with class = 'object' and only attribute "prop"
                lit_res = lit_analyze(branch.test)
                #print(f"LITRES: {lit_res}")
                if lit_res and isinstance(lit_res, ast.Attribute): # Check if its an Attribute -- (If its not, LiteralCase will handle it)
                    #print(f"ITS A SINGLE LITERAL-OR WITH POTENTIAL SUBJECTS: {get_potential_subjects(lit_res)}")
                    return get_potential_subjects(lit_res)

                    # Or it could be multiple Cases
                    # Have to check every node in its list of values
                    # See, if those values can be transformed by any plugin #TODO
                    # and returning the intersection of their possible subjects
                    # For now, checking if Literal or ClassCase
                potential_subjects = {}
                for node in values:
                    potential_subjects[node] = set()
                    potential_subjects[node].add(lit_analyze(node))
                    temp = Branch(test = node, body = None)
                    for sj in self.visit(temp):
                        if sj:
                            potential_subjects[node].add(sj)
                    #print(f"SELFVISIT({temp.test}): {self.visit(temp)}" )
                    #print(f"POTENTIAL SUBJECTS FOR: '{ast.unparse(node)}': {potential_subjects[node]}")
                res = set()
                for asd in potential_subjects[values[0]]:
                    res.add(asd)
                for node in values:
                    res = res.intersection(potential_subjects[node])
                    #print(f"RESULTS: {res}")
                return res

            case expression:
                match expression:
                    # If its an isinstance call
                    case ast.Call(func = ast.Name(id="isinstance"), args=[subj, Class]):
                        return get_potential_subjects(subj)
                    # or its a literal expression
                    case _:
                        res = lit_analyze(expression)
                        if res:
                            return get_potential_subjects(res)

                    


    def transform(self, branch, subject_node):
        """Given a branch, and a subject, transform the branch into a match_case"""
        pass



















# TODO: DELETE


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

class Analyzer(ast.NodeVisitor):
    def visit_If(self, node):
        branches = get_branches(node)
        anal = ClassCase()
        for branch in branches:
            print(f"POTENTIAL SUBJECTS FOR: {branch.test.lineno} --> {anal.visit(branch)}")


def main():
    with open("../test.py", "r") as src:
        tree = ast.parse(src.read())    

    anal = Analyzer()
    anal.visit(tree)
        

if __name__ == "__main__":
    main()
