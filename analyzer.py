import ast


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.valid_nodes = []

    def visit_If(self, node):
        print(f"Found and If, at line number: {node.lineno}")
        variable_id = ""
        match node.test:
            case ast.Compare(left=ast.Name(id=var_id, ctx = _), ops =[ast.Eq()], comparators=[ast.Constant(_)]) | ast.Compare(left=ast.Constant(_), ops =[ast.Eq()], comparators=[ast.Name(id=var_id, ctx = _)]):
                # Either 'if id == constant' or 'constant == id' 
                variable_id = var_id
                print(var_id)
            case _:
                print("This If is not the one you are looking for.")
                return
            
        depth = 0
        current = node 
        while len(current.orelse) and isinstance(current.orelse[0], ast.If):
            depth += 1
            current = current.orelse[0]
        print(f"Its depth is {depth}")






def main():
    with open("test.py", "r") as src:
        tree = ast.parse(src.read())
    Analyzer().visit(tree)

if __name__ == "__main__":
    main()

    