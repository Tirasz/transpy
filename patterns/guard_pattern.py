import ast

class GuardPattern():
    def __init__(self):
        self.terms = []
        self.guard = []
        self.potential_subjects = set()

    def visit(self, node):
        match node:
            case ast.BoolOp(op = ast.And(), values = [*values]):
                for value in values:
                    self.terms.append(value)
            case _:
                return False
        
        return True

    def transform(self):
        # TODO
        pass

    def get_potential_subjects(self):
        return self.potential_subjects