import ast
from analyzer import Analyzer
import os
from pathlib import Path
from functools import lru_cache

@lru_cache(maxsize=128)
def is_inside_if(lines, pos, base_indent):
    #Supposing that base_indent is the indentation of the If-node returns True if the lines[pos] is inside that If-node
    indent = indentation(lines[pos])
    #print(f"Indent at line: ({lines[pos].strip()}): {indent}")
    stripped = lines[pos].strip()
    if indent > base_indent:
        # Line is indented inside base_indent
        return True
    elif indent == base_indent and (stripped.startswith("else:") or stripped.startswith("elif") or stripped.startswith(")") or stripped.startswith("#")):
        # Line is at the same indentation, but its just another branch or smth
        return True
    elif indent == 0 and not bool(stripped) and (pos+1 < len(lines)):
        # Empty line, have to check recursively until we find something, or end of file
        return is_inside_if(lines, pos+1, base_indent)
    else:
        return False

def count_actual_lines( lines, pos):
    # At pos is the beginning of the If-node in the source code's string of lines
    offset = 0
    if not lines[pos].startswith('if'):
        while not lines[pos+offset].strip().startswith('if'):
            offset -= 1
        
    base_indent = indentation(lines[pos+offset])
    #print(f"Base-Indent at line: ({lines[pos+offset].strip()}): {base_indent}")
    res = 1 - offset
    pos += 1
    while pos < len(lines) and is_inside_if(lines, pos, base_indent):
        res += 1
        pos += 1
    #print(f" ACTUAL LINES: {res}, OFFSET: {offset}")
    return (res, offset)

def indentation(s, tabsize=4):
    sx = s.expandtabs(tabsize)
    return 0 if sx.isspace() else len(sx) - len(sx.lstrip())

class Transformer(ast.NodeTransformer):

    def __init__(self):
        self.analyzer = Analyzer()
        self.results = {} # Mapping the linenos of the og If-nodes to their transformed counterpart

    def visit_If(self, node):
        #print(f"TRANSFORMER: NODE({node.test.lineno})")
        self.analyzer.visit(node)
        if node in self.analyzer.subjects.keys():
           #self.lines[node.test.lineno-1] = count_lines(node) 
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


    def transform(self, file):
        with open(file, "r") as src:
            try:
                tree = ast.parse(src.read())
            except SyntaxError:
                #print(f"SyntaxError found in file:\n {file} \n Skipping file!")
                return

            self.visit(tree)
            if len(self.results.keys()) == 0:
                return
            
            src.seek(0)
            lines = tuple(src.readlines())

        with open(file, "w") as out:
            i = 0
            while i < len(lines):
                if i in self.results.keys():
                    #print(f"LINE {i} IS IN RESULTS")
                    if_length, offset = count_actual_lines(lines, i)
                    self.results[i] = (self.results[i], if_length)
                    if offset != 0:
                        #print(f" AT LINE ({i}) OFFSET IS: {offset}")
                        self.results[i+offset] = self.results[i]
                i += 1
            
            i = 0
            while i < len(lines):
                if i in self.results.keys():
                    indent = indentation(lines[i])
                    res = ast.unparse(self.results[i][0]).splitlines()
                    for newLine in res:
                        out.write(indent * " " + newLine + "\n")
                    i += self.results[i][1] -1
                else:
                    out.write(lines[i])
                i += 1