import ast
from typing import Pattern
from plugins.Base import get_branches, MIN_BRANCHES

def _get_subject(compare, ops):
    #A compare node is "literal" if its left attribute is:
    # - A Name node and its comparators atribute is:
    #       - A single Constant ->(number or string)
    #       - An UnaryOp whose operator is USub ->(negative number)
    # - A single Constant ->(number or string) and its comparators attribute is a Name node
    # - An UnaryOp whose operator is USub ->(negative number) and its comparators attribute is a Name node 
    # The tuple of accepted operators for the comparator node is the second input
    
    match compare:
        case ast.Compare(ast.Name(id=var_id, ctx = _), [comp], [ast.Constant(_)]) if isinstance(comp, ops):
            return var_id
        case ast.Compare(ast.Constant(_), [comp], [ast.Name(id=var_id, ctx = _)]) if isinstance(comp, ops):
            return var_id
        case ast.Compare(ast.Name(id=var_id, ctx = _), [comp], [ast.UnaryOp(ast.USub(), ast.Constant(_))]) if isinstance(comp, ops):
            return var_id
        case ast.Compare(ast.UnaryOp(ast.USub(), ast.Constant(_)), [comp], [ast.Name(id=var_id, ctx = _)]) if isinstance(comp, ops):
            return var_id

    return False

def get_const_node(compare):
    # It is guaranteed that the input is a compare node that is literal
    if isinstance(compare.left, ast.Name):
        return compare.comparators[0]
    elif isinstance(compare.comparators[0], ast.Name):
        return compare.left
    raise ValueError(f"Cannot get the const node out of: \n {ast.dump(compare)}")

def get_subject(expr, ops = (ast.Eq,)):
    # An expression is literal if it compares a subject to a constant with the ast.Eq operator
    # In case of a list of nodes, like in a BoolOp, the BoolOp is considered literal if all of its values are literal, and have the same subject
    match expr:
        case [*nodes]:
            subject = {}
            for node in nodes:
                subj = get_subject(node, ops)
                if not subj:
                    return False
                subject[subj] = 1
            subject = False if len([*subject]) != 1 else [*subject][0]
            return subject
        case node:
            return _get_subject(node, ops) #!= False

def analyze_test(test):
    # The root node of the test of a branch can be:
    match test:
        # A list of expressions inside a BoolOp with OR
        case ast.BoolOp(ast.Or(), [*values]):          
            # Need to check if every expression is an equality check with the same subject against a constant
            return get_subject(values)

        # A list of expressions inside a BoolOp with AND
        case ast.BoolOp(ast.And(), [*values]):          
            # Need to check if there is a BoolOp(OR) in the list of expressions, that is literal,
            # or at least single expression that is literal
            best_subj_candidate = None
            foundBoolOr = False
            for node in values:
                match node:
                    case ast.BoolOp(ast.Or(), [*exprs]):
                        if foundBoolOr:
                            return False
                        best_subj_candidate = get_subject(exprs)
                        foundBoolOr = True
                        #return get_subject(exprs)
                    case _:
                        if not best_subj_candidate:
                            best_subj_candidate = get_subject(node)
                        #return get_subject(node)
            # The only other way is if every expression is literal, with the operators being comparisons
            if not best_subj_candidate:
                best_subj_candidate = get_subject(values, (ast.Lt, ast.LtE, ast.Gt, ast.GtE))
            return best_subj_candidate

        # Nothing (else: block)
        case None:  
            #print("NONE")
            return "ELSE:"

        # A single expression
        case expr: 
            return get_subject(expr, (ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Eq, ast.NotEq))
 
        
def transform_test(test):
    match test:
        case ast.BoolOp(ast.Or(), [*values]):
            #It is guaranteed, that every node in the values is literal
            patterns = []
            for node in values:
                curr_pattern = ast.matchValue() 

class LiteralCase:
    def visit(self, node):
        branches = get_branches(node)
        if len(branches) < MIN_BRANCHES:
            return False 

        subject = None
        # Checking if all the branches are in correct form and have the same subject
        for branch in branches:
            print(f"BRANCH: {branch.body[0].lineno -1}")
            curr_subject = analyze_test(branch.test)
            print(f"SUBJECT: {curr_subject}")
            if subject == None:
                subject = curr_subject
            
            if not curr_subject or (subject != curr_subject and curr_subject != "ELSE:"):
                print(f"NOT VALID IF NODE! CURR SUBJ: {curr_subject}, SUBJECT: {subject}")
                return False
            
        return True

    def transform(self, node):
        branches = get_branches(node)
        # A match node has a 'subject': Should be a Name node 
        # Since the analyzer already made sure, that the subject is the same in all branches, we can skip that here
        subject = ast.Name(id=analyze_test(branches[0].test), ctx=ast.Load())
        # and a list of 'cases': each case being a 'match_case' Node
        # a 'match_case' has a 
        # - 'pattern': in this case, either a MatchValue(value=Constant(x)), a MatchAs(), or a MatchOr(patterns)
        # - 'body': This should just be the main 'If' node's body
        # - 'guard': an optional attribute, contains an expression that will be evaluated if the pattern matches the subject
        cases = []
        
        # We also know that every branch has a test of the form 'id == constant' or 'constant == id'
        
        for branch in branches:
            curr_pattern = ast.MatchValue(value = ast.Constant(get_var_const(branch.test)[1])) if branch.test is not None else ast.MatchAs()
            cases.append(ast.match_case(pattern = curr_pattern, body = branch.body))

        return ast.Match(subject = subject, cases = cases)
        