import ast


class LiteralPattern:
    def __init__(self):
        self._potential_subjects = set()
        self.const_node = None

    def visit(self, node):
        match node:
            case ast.Compare(left = subject_node, ops = [ast.Eq()], comparators = [ast.Constant()] | [ast.UnaryOp(ast.USub(), ast.Constant())]):
                self.const_node = node.comparators[0]
                self._potential_subjects.add(subject_node)
            case ast.Compare(left = ast.Constant() | ast.UnaryOp(ast.USub(), ast.Constant()), ops = [ast.Eq()], comparators = [subject_node]):
                self.const_node = node.left
                self._potential_subjects.add(subject_node)
            case _:
                return False
        return True

    def transform(self, subject):
        subject_node = self.potential_subjects.pop()
        if not subject == subject_node:
            raise ValueError(f"Cannot transform LiteralPattern! Given subject: {subject}, Expected: {subject_node}")
    
        return ast.MatchValue(self.const_node)

    def potential_subjects(self):
        return self._potential_subjects