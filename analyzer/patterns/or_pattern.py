import ast

class OrPattern():
    IsComplex = False
    def __init__(self):
        self.terms = []
        self._potential_subjects = set()
        self.node = None

    def visit(self, node):
        self.node = node
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
        
        if len(self._potential_subjects) == 0:
            return False
        
        # If any pattern has a guard inside an or pattern, the or pattern cannot be transformed
        # (I think so at least lol)
        for term in self.terms:
            for subj in self._potential_subjects:
                if term.guard(subj):
                    return False

        return True


    def transform(self, subject):
        _patterns = []
        for term in self.terms:
            _patterns.append(term.transform(subject))
        return ast.MatchOr(patterns = _patterns)

    
    def potential_subjects(self):
        return self._potential_subjects

    def guard(self, subject):
        return None