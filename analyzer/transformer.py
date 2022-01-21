import ast
from analyzer import Analyzer
from analyzer.utils import count_lines
import os
from pathlib import Path

def indentation(s, tabsize=4):
    sx = s.expandtabs(tabsize)
    return 0 if sx.isspace() else len(sx) - len(sx.lstrip())

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
                    #print(f"TRANSFORMER: BRANCH IS FLATTENED")
                    for subBranch in branch.flat:
                        pattern = self.analyzer.patterns[subBranch]
                        transformed_branch = ast.match_case(pattern = pattern.transform(subjectNode), guard = pattern.guard(subjectNode), body = subBranch.body)
                        _cases.append(transformed_branch)
                else:
                    #print(f"TRANSFORMER: BRANCH IS NOT FLATTENED")
                    _pattern = ast.MatchAs() if branch.test is None else self.analyzer.patterns[branch].transform(subjectNode)
                    _guard = None if branch.test is None else self.analyzer.patterns[branch].guard(subjectNode)
                    temp = ast.Module(body = branch.body, type_ignores=[])
                    self.generic_visit(temp)
                    #print("TRANSFORMER TEMP:")
                    #print(ast.unparse(temp))
                    transformed_branch = ast.match_case(pattern = _pattern, guard = _guard, body = temp.body)
                    _cases.append(transformed_branch)
            result = ast.Match(subject = subjectNode, cases = _cases) 
            self.results[node.test.lineno-1] = result
            return result
        else:
            temp = ast.Module(body = node.body)
            self.generic_visit(temp)
            node.body = temp.body
            return node

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
                    indent = indentation(lines[i])
                    #print(f"INSIDE IF AT {lines[i]} -- JUMPING TO: {lines[i+self.lines[i]]}")
                    res = ast.unparse(self.results[i]).splitlines()
                    for newLine in res:
                        out.write(indent * " " + newLine + "\n")
                    #out.write("\n")
                    i += self.lines[i] 
                else:
                    out.write(lines[i])
                i += 1
                    
    def inline_transform(self, file):
        tempFile = (file.parent / f"temp-{file.parts[-1]}")
        self.transform(file, tempFile)
        with open(tempFile) as temp, open(file, "w") as f:
            f.write(temp.read())
        os.remove(tempFile)