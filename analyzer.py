import ast

MIN_BRANCHES = 4


def get_var_const(node): 
    #Returns a tuple of (id,const) 
    #Returns false if the If-node's test is not either in the form 'id == constant' or 'constant == id'

    if(isinstance(node, ast.If)):
        test = node.test
    elif(isinstance(node, ast.Compare)):
        test = node
    else:
        raise ValueError(f"Cannot check the 'test' of type: ({node.__class__.__name__})!")

    match test:
        case ast.Compare(left=ast.Name(id=var_id, ctx = _), ops =[ast.Eq()], comparators=[ast.Constant(const)]) | ast.Compare(left=ast.Constant(const), ops =[ast.Eq()], comparators=[ast.Name(id=var_id, ctx = _)]):
            return (var_id, const)
        case _:
            return False





class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.save_file = open("to_transform.py", "w")
        

    def __del__(self):
        self.save_file.close()

    def save_code(self, node, start, end):
        self.save_file.write(f"# {start} - {end}\n" + ast.unparse(node) + "\n")



    def visit_If(self, node):
        print(f"## Found and If, at line number: {node.lineno} ##")
        # Checking if the main If node is in correct form
        subject = get_var_const(node)[0]
        if not subject:
            return

        # Checking if all the branches are in correct form
        branches = get_branches(node)
        for branch in branches:
            test = branch[0]
            if test != 0 and get_var_const(test)[0] != subject:
                return
                
        # The last line is equal to the last node in the body of the last branch
        # This might need to be refactored
        last_line = branches[-1][1][-1].lineno        

        if len(branches) >= MIN_BRANCHES:
            print(f"# This If that spans from line number ({node.lineno} - {last_line}) has ({len(branches)}) branches and has correct form. #")
            self.save_code(node, node.lineno, last_line)

        

def main():
    with open("test.py", "r") as src:
        tree = ast.parse(src.read())
    Analyzer().visit(tree)

if __name__ == "__main__":
    main()
    print("Done")

    
