import ast
from copy import deepcopy
from analyzer.utils import count_lines
from analyzer.analyzer import Analyzer
import os

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
    tr = Transformer()
    tr.transform("test.py", "test.py")
    #test

if __name__ == "__main__":
    main()