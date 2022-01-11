import ast


class LiteralPattern:
    IsComplex = False
    
    def __init__(self):
        self._potential_subjects = set()
        self.const_node = None
        self.node = None

    def visit(self, node):
        self.node = node
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
        for subject_node in self._potential_subjects:
            break
        if not subject == subject_node:
            raise ValueError(f"Cannot transform LiteralPattern! Given subject: {subject}, Expected: {subject_node}")
    
        return ast.MatchValue(self.const_node)

    def potential_subjects(self):
        # For an attribute node, representing "obj.prop.x" returns the set: (obj, obj.prop, obj.prop.x)
        # In some cases, they all could be considered a subject
        """
        for subject in self._potential_subjects:
            break
        currNode = subject
        while isinstance(currNode, ast.Attribute): 
            self._potential_subjects.add(currNode.value)
            currNode = currNode.value
        self._potential_subjects.add(currNode)
        """
        return self._potential_subjects

    def guard(self, subject):
        return None