import ast


class SingletonPattern:
    IsComplex = True
    def __init__(self):
        self._potential_subjects = set()
        self.const_node = None
        self.node = None
        self.inverted = False
        self._guard = []

    def visit(self, node):
        self.node = node
        match node:
            case ast.Compare(left = subject_node, ops = [ast.Is()], comparators = [ast.Constant()] ):
                self.const_node = node.comparators[0]
                self._potential_subjects.add(subject_node)
            case _:
                return False
        if self.inverted and self.const_node.value == None:
            self._guard.append(self.node)
        return True

    def transform(self, subject):
        for subject_node in self._potential_subjects:
            break

        if not subject == subject_node:
            raise ValueError(f"Cannot transform SingletonPattern! Given subject: {subject}, Expected: {subject_node}")

        if len(self._guard):
            return ast.MatchAs()
        elif self.inverted:
            self.const_node = ast.Constant(kind = None, value = (not self.const_node.value))

        return ast.MatchSingleton(self.const_node.value)

    def process(self, parentPattern):
        for subjectNode in self._potential_subjects:
            break

        if len(self._guard): # if its a (is not None) check
            for pattern in parentPattern.terms:  
                if subjectNode in pattern.potential_subjects(): # and there are other patterns, that recognise the same subject
                    parentPattern.terms.remove(self) # remove this check
                    return

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
        if self._guard:
            return self._guard
        return None