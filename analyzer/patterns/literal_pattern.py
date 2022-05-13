import ast


class LiteralPattern:
    IsComplex = False
    
    def __init__(self):
        self._potential_subjects = set()
        self.const_node = None
        self.node = None
        self.singleton = False

    def visit(self, node):
        self.node = node
        match node:
            case ast.Compare(left = subject_node, ops = [ast.Eq()], comparators = [ast.Constant()] | [ast.UnaryOp(ast.USub(), ast.Constant())]
                            ):
                self.const_node = node.comparators[0]
                self._potential_subjects.add(subject_node)
            case ast.Compare(left = ast.Constant() | ast.UnaryOp(ast.USub(), ast.Constant()), ops = [ast.Eq()], comparators = [subject_node]):
                self.const_node = node.left
                self._potential_subjects.add(subject_node)
            case ast.Compare(left = subject_node, ops = [ast.Is()], comparators = [ast.Constant()] ):
                self.const_node = node.comparators[0]
                self._potential_subjects.add(subject_node)
                self.singleton = True
            case _:
                return False
        return True

    def transform(self, subject):
        for subject_node in self._potential_subjects:
            break
        if not subject == subject_node:
            raise ValueError(f"Cannot transform LiteralPattern! Given subject: {subject}, Expected: {subject_node}")
        if self.singleton:
            return ast.MatchSingleton(self.const_node.value)
    
        return ast.MatchValue(self.const_node)

    def potential_subjects(self):
        return self._potential_subjects

    def guard(self, subject):
        return None