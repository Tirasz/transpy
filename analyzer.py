import ast

MIN_BRANCHES = 4

def get_var_const_from_if(node):
    #Returns a tuple of (id,const) 
    #Returns false if the If-node's test is not either in the form 'id == constant' or 'constant == id'

    match node.test:
        case ast.Compare(left=ast.Name(id=var_id, ctx = _), ops =[ast.Eq()], comparators=[ast.Constant(const)]) | ast.Compare(left=ast.Constant(const), ops =[ast.Eq()], comparators=[ast.Name(id=var_id, ctx = _)]):
            return (var_id, const)
        case _:
            return False


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.save_file = open("to_transform.py", "w")
        self.valid_nodes = []

    def __del__(self):
        self.save_file.close()

    def save_code(self, node, start, end):
        self.save_file.write(f"# {start} - {end}\n" + ast.unparse(node) + "\n")

 

    def visit_If(self, node):
        print(f"## Found and If, at line number: {node.lineno} ##")
        variable_id = get_var_const_from_if(node)[0]

        if not variable_id:
            return

        branches = 1
        current = node 
        # Going through and counting all the elif nodes and checking their form
        while len(current.orelse) and isinstance(current.orelse[0], ast.If):
            branches += 1
            current = current.orelse[0]
            if not get_var_const_from_if(current)[0] == variable_id:
                return

            
        if not len(current.orelse): # If there is no last else: block
            last_line = current.body[-1].lineno
        else:
            branches += 1
            last_line = current.orelse[-1].lineno

        if branches >= MIN_BRANCHES:
            print(f"# This If that spans from line number ({node.lineno} - {last_line}) has ({branches}) branches and has correct form. #")
            self.save_code(node, node.lineno, last_line)

        

def main():
    with open("test.py", "r") as src:
        tree = ast.parse(src.read())
    Analyzer().visit(tree)

if __name__ == "__main__":
    main()
    print("Done")

    