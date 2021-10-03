import ast

class Analyzer(ast.NodeVisitor):

    def visit_If(self, node):
        print(f"## Found and If, at line number: {node.lineno} ##")
        

        

def main():
    with open("test.py", "r") as src:
        tree = ast.parse(src.read())
    Analyzer().visit(tree)

if __name__ == "__main__":
    main()
    print("Done")

    
