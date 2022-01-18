import ast

def custom_hash(self):
    return hash(ast.dump(self))

def custom_eq(self, other):
    return hash(self) == hash(other)

ast.AST.__hash__ = custom_hash
ast.AST.__eq__ = custom_eq

from utils import get_branches, load_patterns


class Analyzer(ast.NodeVisitor):
    Patterns = None

    def recognise_Branch(self, branch):
        """Passes the branch to all known Patterns. Returns the pattern that recognises it. Returns None, if no pattern recognises the branch."""
        for pattern in Analyzer.Patterns:
            curr_pattern = pattern()
            if curr_pattern.visit(branch.test):
                print(f"ANALYZER: ({ast.unparse(branch.test)}) RECOGNISED BY: {type(curr_pattern).__name__}")
                return curr_pattern
        print(f"ANALYZER: NO PATTERN RECOGNISES: ({ast.unparse(branch.test)})")
        return None

    def __init__(self):
        self.branches = {} # Mapping If-nodes to a list of its branches. !!Only contains transformable if-nodes!!
        self.patterns = {} # Mapping branches to a pattern
        self.subjects = {} # Mapping the If-node to its selected subject !!Only contains transformable if-nodes!!
        for pattern in Analyzer.Patterns:
            pattern.Patterns = Analyzer.Patterns
        
    def visit_If(self, node):
        self.branches[node] = get_branches(node)
        print(f"\n\nANALYZER: IF-NODE({node.test.lineno})")
        for branch in self.branches[node]:
                print(f"ANALYZER: BRANCH({branch.body[0].lineno-1})")

                # Skipping trivial 'else:' branches.
                if branch.test is None:
                    print(f"ANALYZER: TEST IS NONE. SKIPPING")
                    continue

                # Determine the main pattern of the branch
                branch_pattern = self.recognise_Branch(branch)
                if branch_pattern is None: # If no pattern recognises the branch, then delete the whole if node from the dict and return.
                    del self.branches[node]
                    return
                
                self.patterns[branch] = branch_pattern

                

        # An if-node can be transformed, if all of its branches are recognised patterns, and these patterns can all recognise the same subject.
        # Intersecting the possible subjects for each branch
        potential_subjects = self.patterns[self.branches[node][0]].potential_subjects().copy()
        # Skipping "else:" branch
        for branch in [b for b in self.branches[node] if b.test is not None]:
            print(f"ANALYZER: POTENTIAL SUBJECTS FOR BRANCH({branch.body[0].lineno-1}): {[ast.unparse(x) for x in self.patterns[branch].potential_subjects()]}")
            potential_subjects = potential_subjects.intersection(self.patterns[branch].potential_subjects())
 
        if len(potential_subjects) == 0:
            print(f"ANALYZER: NO COMMON SUBJECT FOR IF-NODE AT: ({node.test.lineno})")
            del self.branches[node]
            return
        elif len(potential_subjects) > 1:
            print(f"ANALYZER: MORE THAN ONE COMMON SUBJECT FOR IF-NODE AT: ({node.test.lineno})")
        self.subjects[node] = potential_subjects.pop()
        print(f"ANALYZER: IF-NODE AT ({node.test.lineno}) HAS POTENTIAL SUBJECT: ({ast.unparse(self.subjects[node])})")

        for branch in self.branches[node]:
            if branch.flat is not None:
                for subBranch in branch.flat:
                    flag = False
                    for pot_subject in self.patterns[subBranch].potential_subjects():
                        if pot_subject == self.subjects[node]:
                            flag = True
                            break
                    if not flag:
                        branch.flat = None
                        break

def main():
    Analyzer.Patterns = tuple(load_patterns())
    
    with open("test.py", "r") as src:
        tree = ast.parse(src.read())


    analyzer = Analyzer()    
    analyzer.visit(tree)
    with open("transformed.py", "w") as out:
        for ifNode, subjectNode in analyzer.subjects.items():
            _cases = []
            out.write("#" + "-"*10 + str(ifNode.lineno) + "-"*10 + f"[{type(subjectNode).__name__}]" +"\n")
            for branch in analyzer.branches[ifNode]:
                if branch.flat is not None:
                    for subBranch in branch.flat:
                        print(f"FLATTENED SUBBRANCH: {ast.unparse(subBranch.test)}")
                        if subBranch.test is not None:
                            pattern = analyzer.patterns[subBranch]
                            transformed_branch = ast.match_case(pattern = pattern.transform(subjectNode), guard = pattern.guard(subjectNode), body = subBranch.body)
                        else:
                            transformed_branch = ast.match_case(pattern = ast.MatchAs(), guard = None, body = subBranch.body)
                       
                        _cases.append(transformed_branch)
                elif branch.test is not None:
                    pattern = analyzer.patterns[branch]
                    transformed_branch = ast.match_case(pattern = pattern.transform(subjectNode), guard = pattern.guard(subjectNode), body = branch.body)
                    _cases.append(transformed_branch)
                else:
                    transformed_branch = ast.match_case(pattern = ast.MatchAs(), guard = None, body = branch.body)
                    _cases.append(transformed_branch)

                
            transformed_node = ast.Match(subject = subjectNode, cases = _cases)
            out.write(ast.unparse(transformed_node) + "\n")



if __name__ == "__main__":
    main()


    
