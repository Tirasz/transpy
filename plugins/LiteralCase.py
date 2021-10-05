import ast
from plugins.Base import get_branches, MIN_BRANCHES

def get_var_const(node): 
    #Returns a tuple of (id,const) 
    #Returns false if the If-node's test is not either in the form 'id == constant' or 'constant == id'

    if not (isinstance(node, ast.If) or isinstance(node, ast.Compare)):
        raise ValueError(f"Cannot check the 'test' of type: ({node.__class__.__name__})!")

    test = node
    if(isinstance(node, ast.If)):
        test = node.test
    
    match test:
        case ast.Compare(left=ast.Name(id=var_id, ctx = _), ops =[ast.Eq()], comparators=[ast.Constant(const)]) | ast.Compare(left=ast.Constant(const), ops =[ast.Eq()], comparators=[ast.Name(id=var_id, ctx = _)]):
            return (var_id, const)
        case _:
            return False


class LiteralCase:
    def visit(self, node):
        branches = get_branches(node)
        if len(branches) < MIN_BRANCHES:
            return False 

        subject = get_var_const(node)[0]
        # Checking if all the branches are in correct form
        for branch in branches:
            if branch.test is not None and get_var_const(branch.test)[0] != subject:
                return False
        return True

    def transform(self, node):
        # A match node has a 'subject': Should be a Name node 
        subject = ast.Name(id=get_var_const(node)[0], ctx=ast.Load())
        # and a list of 'cases': each case being a 'match_case' Node
        # a 'match_case' has a 'pattern': in this case, either a MatchValue(value=Constant(x)) or a MatchAs()
        # and a 'body': This should just be the main 'If' node's body
        cases = []
        # Since the analyzer already made sure, that the subject is the same in all branches, we can skip that here
        # We also know that every branch has a test of the form 'id == constant' or 'constant == id'
        branches = get_branches(node)
        for branch in branches:
            curr_pattern = ast.MatchValue(value = ast.Constant(get_var_const(branch.test)[1])) if branch.test != 0 else ast.MatchAs()
            cases.append(ast.match_case(pattern = curr_pattern, body = branch.body))

        return ast.Match(subject = subject, cases = cases)
        