import ast
# TODO maybe not like this
def custom_hash(self):
    return hash(ast.dump(self))

def custom_eq(self, other):
    return hash(self) == hash(other)

ast.AST.__hash__ = custom_hash
ast.AST.__eq__ = custom_eq

from analyzer.utils import get_branches, load_patterns, flatten


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
        if Analyzer.Patterns is None:
            Analyzer.Patterns = tuple(load_patterns())
            for pattern in Analyzer.Patterns:
                pattern.Patterns = Analyzer.Patterns
        
    def visit_If(self, node):
        self.branches[node] = get_branches(node)
        print(f"\n\nANALYZER: IF-NODE({node.test.lineno})")
        
        # Looping through the If-nodes branches
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
                # Checking nested If-nodes
                subBranches = flatten(branch)
                if subBranches is not None: # Have to determine which version to transform: flattened, or base
                        # TODO: config 
                        # Strict: Only choose flat version if no branch is "ugly"
                        # Normal: Require at least one branch that isnt "ugly"
                        # Loose: Always choose flat
                        isUgly = False
                        for subBranch in subBranches:
                            pattern = self.recognise_Branch(subBranch) # Guaranteed to be GuardPattern
                            self.patterns[subBranch] = pattern
                            # Flattened branches tests always look like: BoolOp(And(), [mainTest, (nestedTest)*])
                            # Have to check if the patterns guard == nestedTest (if nestedTest is not None)
                            # Guard looks like: BoolOp(And(), [values])
                            guard = pattern.guard(self.subjects[node])
                            if guard is not None:
                                guardList = guard.values
                                temp = subBranch.test.values.copy()
                                temp.remove(subBranch.mainTest)
                                if temp == guardList: # Found ugly branch
                                    isUgly = True
                                    break
                        if not isUgly:
                            branch.flat = subBranches

                            


def main():
    pass



if __name__ == "__main__":
    main()


    
