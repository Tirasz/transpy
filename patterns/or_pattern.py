import ast

class OrPattern():
    def __init__(self):
        self.terms = []
        self.potential_subjects = set()
        

    def visit(self, node):
        match node:
            case ast.BoolOp(op = ast.Or(), values = [*values]):
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