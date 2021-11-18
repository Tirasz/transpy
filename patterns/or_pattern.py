import ast

class OrPattern():
    def __init__(self):
        self.terms = []
        self._potential_subjects = set()

    def visit(self, node):
        # Or-pattern: T1 OR T2 [OR Tn]* 
        # Where all Ti terms are valid patterns, and they share one possible subject.
        if not ( isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or) ):
            return False

        for value in node.values:
            for pattern in OrPattern.Patterns:
                curr_pattern = pattern()
                if curr_pattern.visit(value):
                    self.terms.append(curr_pattern)
                    print(f"PATTERN: ({ast.unparse(value)}) RECOGNISED BY: {type(curr_pattern).__name__}")
                    break
                
        if len(node.values) != len(self.terms):
            return False
        # At this point, every term is a recognised pattern
        self._potential_subjects = self.terms[0].potential_subjects().copy()
        # Intersecting every terms potential subjects.
        for term in self.terms:
            self._potential_subjects = self._potential_subjects.intersection(term.potential_subjects())
        return len(self._potential_subjects)


    def transform(self):
        # TODO
        pass
    
    def potential_subjects(self):
        return self._potential_subjects