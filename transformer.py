import ast
from analyzer import Analyzer

class Transformer(ast.NodeTransformer):

    def __init__(self):
        self.analyzer = Analyzer()
            #analyzer_results.branches = {} # Mapping If-nodes to a list of its branches. !!Only contains transformable if-nodes!!
            #analyzer_results.patterns = {} # Mapping branches to a pattern
            #analyzer_results.subjects = {} # Mapping the If-node to its selected subject !!Only contains transformable if-nodes!!

    def visit_If(self, node):
        print(f"TRANSFORMER: NODE({node.test.lineno})")
        self.analyzer.visit(node)
        if node in self.analyzer.subjects.keys():
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
            return ast.Match(subject = subjectNode, cases = _cases)
        else:
            temp = ast.Module(body = node.body)
            self.generic_visit(temp)
            node.body = temp.body




def main():
    tr = Transformer()
    tree = None
    with open("test.py") as src:
        tree = ast.parse(src.read())
        tr.visit(tree)

    with open("transformed.py", "w") as out:
        newTree = ast.fix_missing_locations(tree)
        out.write(ast.unparse(newTree))


if __name__ == "__main__":
    main()