import ast

class GuardPattern():
    IsComplex = False
    def __init__(self):
        self.terms = []
        self._guard = []
        self._potential_subjects = set()
        self.node = None

    def visit(self, node):
        self.node = node
        # T1 AND T2 [AND Tn]
        # Where at least one term is a recognised pattern
        # In case of more than one recognised pattern, the GuardPattern is only valid, if no two terms share the same subject.
        # (Iiii think, but im sure there are some dumbass edge cases)
        if not ( isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And) ):
            return False
            
        for value in node.values:
            for pattern in GuardPattern.Patterns:
                curr_pattern = pattern()
                if curr_pattern.visit(value):
                    self.terms.append(curr_pattern)
                    print(f"PATTERN: ({ast.unparse(value)}) RECOGNISED BY: {type(curr_pattern).__name__}")
                    break
            
            self._guard.append(value)

        if len(self.terms) == 0:
            return False
        # At least one term is recognised

        #Checking for complex patterns
        for pattern in self.terms:
            if pattern.IsComplex:
                pattern.process(self)
                print(f"PATTERN: RETURNED FROM COMPLEX CALL.")
                break
        
        print(f"\tREMAINING TERMS:\n\t{[str(term) for term in self.terms]}")
        print(f"\tREMAINING GUARD:\n\t{[ast.unparse(t) for t in self._guard]}")
        self._potential_subjects = self.terms[0].potential_subjects().copy()
        # Unioning every terms potential subjects.
        for term in self.terms:
            self._potential_subjects = self._potential_subjects.union(term.potential_subjects())
        # If no two recognised terms share the same subject, the guard pattern is valid.
        return len(self._potential_subjects) == len(self.terms)



    def transform(self, subject):
        # Guaranteed, that only one term has the given subject
        for pattern in self.terms:
            if subject in pattern.potential_subjects():
                return pattern.transform(subject)


    def potential_subjects(self):
        return self._potential_subjects

    def guard(self, subject):
        # self._guard contains all the terms by default
        # this returns the terms that are not recognised, and the ones that dont have the given subject
        print(f"PATTERN: GUARD: {[ast.unparse(t) for t in self._guard]}")
        if len(self._guard) == 0:
            return None
        res = []
        for term in self._guard:
            recognised = False
            for pattern in GuardPattern.Patterns:
                curr_pattern = pattern()
                if (curr_pattern.visit(term)) and (subject in curr_pattern.potential_subjects()):
                    recognised = True
                    break
            if not recognised:
                res.append(term)
        if len(res):
            return ast.BoolOp(op = ast.And(), values = res)
        return None