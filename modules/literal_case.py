import ast
from TransformerBase import get_branches, MIN_BRANCHES

def get_var_const(node): 
    #Returns a tuple of (id,const) 
    #Returns false if the If-node's test is not either in the form 'id == constant' or 'constant == id'

    if not isinstance(node, ast.If) or isinstance(node, ast.Compare):
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
        # Checking if the main If node is in correct form
        subject = get_var_const(node)[0]
        if not subject:
            return False

        
        branches = get_branches(node)
        if len(branches) < MIN_BRANCHES:
            return False 

        # Checking if all the branches are in correct form
        for branch in branches:
            curr_subject = get_var_const(branch.test)[0]
            if branch.test is not None and curr_subject != subject:
                return False

        