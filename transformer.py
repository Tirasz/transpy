import ast
from analyzer import get_var_const, get_branches




class Transformer(ast.NodeTransformer):
    
    def visit_If(self, node):
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
            curr_pattern = ast.MatchValue(value = ast.Constant(get_var_const(branch[0])[1])) if branch[0] != 0 else ast.MatchAs()
            cases.append(ast.match_case(pattern = curr_pattern, body = branch[1]))

        return ast.Match(subject = subject, cases = cases)
            




 

def main():
    with open("to_transform.py", "r") as f:
        tree = ast.parse(f.read())
    tree = Transformer().visit(tree)

    with open("transformed.py", "w") as out:
        out.write(ast.unparse(tree))


if __name__ == "__main__":
    main()
