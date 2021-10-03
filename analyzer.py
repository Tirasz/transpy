import ast

class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.save_file = open("to_transform.py", "w")
        

    def __del__(self):
        self.save_file.close()

    def save_code(self, node, start, end):
        self.save_file.write(f"# {start} - {end}\n" + ast.unparse(node) + "\n")



    def visit_If(self, node):
        print(f"## Found and If, at line number: {node.lineno} ##")
        
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

    
