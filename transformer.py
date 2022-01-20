import ast
from copy import deepcopy
from analyzer.utils import count_lines
from analyzer.analyzer import Analyzer
import os, glob
import argparse
import shutil
from pathlib import Path

parser = argparse.ArgumentParser(description="Analyzes and transforms python projects.")
parser.add_argument("path", metavar='PATH', type=str, nargs=1, help="path to the directory / python file")
parser.add_argument('-i', '--inline', dest='mode', action='store_const',
                    const="inline", default="copy",
                    help='transform inline (default makes a copy)')
parser.add_argument('-o', '--overwrite', dest='ow', action='store_const', const="Y", default=None, help="automatically overwrite files, when not transforming inline")

class Transformer(ast.NodeTransformer):

    def __init__(self):
        self.analyzer = Analyzer()
        self.lines = {} # Mapping the linenos of the original If-nodes to their length
        self.results = {} # Mapping the linenos of the og If-nodes to their transformed counterpart
    def visit_If(self, node):
        #print(f"TRANSFORMER: NODE({node.test.lineno})")
        self.analyzer.visit(node)
        if node in self.analyzer.subjects.keys():
            self.lines[node.test.lineno-1] = count_lines(node) +1
            subjectNode = self.analyzer.subjects[node]
            _cases = []
            for branch in self.analyzer.branches[node]:
                if branch.flat:
                    for subBranch in branch.flat:
                        pattern = self.analyzer.patterns[subBranch]
                        transformed_branch = ast.match_case(pattern = pattern.transform(subjectNode), guard = pattern.guard(subjectNode), body = subBranch.body)
                        _cases.append(transformed_branch)
                else:
                    _pattern = ast.MatchAs() if branch.test is None else self.analyzer.patterns[branch].transform(subjectNode)
                    _guard = None if branch.test is None else self.analyzer.patterns[branch].guard(subjectNode)
                    temp = ast.Module(body = branch.body)
                    self.generic_visit(temp)
                    transformed_branch = ast.match_case(pattern = _pattern, guard = _guard, body = temp.body)
                    _cases.append(transformed_branch)
            result = ast.Match(subject = subjectNode, cases = _cases) 
            self.results[node.test.lineno-1] = result
            return result
        else:
            temp = ast.Module(body = node.body)
            self.generic_visit(temp)
            node.body = temp.body

    def transform(self, inFile, outFile):
        if inFile == outFile:
            self.inline_transform(inFile)
            return
        
        with open(inFile, "r") as src, open(outFile, "w") as out:
            tree = ast.parse(src.read())
            src.seek(0)
            lines = src.readlines()
            self.visit(tree)
            i = 0
            while i < len(lines):
                if i in self.results.keys():
                    #print(f"INSIDE IF AT {lines[i]} -- JUMPING TO: {lines[i+self.lines[i]]}")
                    out.write(ast.unparse(self.results[i]) + "\n")
                    i += self.lines[i] 
                else:
                    out.write(lines[i])
                i += 1
                    
    def inline_transform(self, file):
        self.transform(file, "temp.py")
        with open("temp.py") as temp, open(file, "w") as f:
            f.write(temp.read())
        os.remove("temp.py")

def main():
    args = parser.parse_args()
    path = Path(args.path[0])
    files_to_transform = []
    overwrite = args.ow

    if not path.exists():
        parser.error("Given path does not exist!")
    if args.mode == "copy":
        print("Copying file(s)...")
        newDir = (path.parent / f"transformed-{path.parts[-1]}").resolve()
        if path.is_dir():
            #print(path.parent / f"transformed-{path.parts[-1]}")
            try:
                path = shutil.copytree(path, newDir).resolve()
            except FileExistsError:
                while not (overwrite == "Y" or overwrite == "N"):
                    overwrite = input(f">> Directory '{newDir}' already exists! Want to overwrite? (Y/N)\n")

                if overwrite == "Y":
                    print(f"Overwriting '{newDir}'")
                    shutil.rmtree(newDir)
                    path = shutil.copytree(path, newDir).resolve()
                else:
                    print("Quitting.")
                    return
            files_to_transform = [f for f in path.rglob('*.py') if f.is_file()]
        else:
            if newDir.is_file():
                while not (overwrite == "Y" or overwrite == "N"):
                    overwrite = input(f">> File '{newDir}' already exists! Want to overwrite? (Y/N)\n")
                
                if overwrite == "Y":
                    print(f"Overwriting '{newDir}'")
                else:
                    print("Quitting.")
                    return
            path = shutil.copy(path,newDir).resolve()
            files_to_transform = [path]
    print("The following file(s) will be transformed:")
    for i in range(len(files_to_transform)):
        print(f"{files_to_transform[i]}")




if __name__ == "__main__":
    main()