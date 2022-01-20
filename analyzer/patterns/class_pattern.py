import ast


def is_attribute_of(attr, node):
    return (isinstance(attr, ast.Attribute) and attr.value == node)

class ClassPattern:
    IsComplex = True
    def __init__(self):
        self._potential_subjects = set()
        self.className = None
        self.kwd_attribtues = []
        self.kwd_patterns = []
        self.node = None

    def visit(self, node):
        self.node = node
        match node:
            case ast.Call(args = [subject_node, class_name], func=ast.Name(id="isinstance")):
                self._potential_subjects.add(subject_node)
                self.className = class_name
            case _:
                return False
        return True

    def transform(self, subject):
        return ast.MatchClass(cls = self.className, patterns=[], kwd_attrs = self.kwd_attribtues, kwd_patterns = self.kwd_patterns)

    def potential_subjects(self):
        return self._potential_subjects

    def guard(self, subject):
        return None

    def process(self, parentPattern):
        # Gets called, when a ClassPattern is found as a subpattern
        # Since ClassPattern specifies the class and the subject, look for other patterns that recognise an attribute of the subject as their subject
        for subject_node in self._potential_subjects:
            break
        if(self.node in parentPattern._guard):
            parentPattern._guard.remove(self.node)
        
        print(f"PATTERN: LOOKING FOR ATTRIBUTES FOR: ({ast.unparse(subject_node)})")
        temp = parentPattern.terms.copy()
        for term in temp:
            for term_subject in term.potential_subjects():
                if is_attribute_of(term_subject, subject_node):
                    print(f"\tFOUND: {type(term).__name__}({ast.unparse(term_subject)})")
                    if term.IsComplex:
                        term.process(parentPattern)
                    self.kwd_attribtues.append(term_subject.attr)
                    self.kwd_patterns.append(term.transform(term_subject))
                    parentPattern.terms.remove(term)
                    if term.node in parentPattern._guard:
                        parentPattern._guard.remove(term.node)
                    break
