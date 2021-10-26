import ast
from plugins.Base import get_branches
MIN_BRANCHES = 3

def lit_analyze(test):
    potential_subjects = []
    # The root node of the test of a branch can be:
    match test:
        # A list of expressions inside a BoolOp with OR
        case ast.BoolOp(ast.Or(), [*values]):          
            # Need to check if every expression is an equality check with the same subject against a constant
            subject = get_subject(values)
            if subject:
                potential_subjects.append(subject)

        # A list of expressions inside a BoolOp with AND
        case ast.BoolOp(ast.And(), [*values]):          
            # Need to check if there is a BoolOp(OR) in the list of expressions, that is literal,
            # or at least single expression that is literal
            for node in values:
                match node:
                    case ast.BoolOp(ast.Or(), [*exprs]):
                        subject = get_subject(exprs)
                        if subject:
                            potential_subjects.append(subject)
                        #return get_subject(exprs)
                    case _:
                        subject = get_subject(node)
                        if subject:
                            potential_subjects.append(subject)

        # Nothing (else: block)
        case None:  
            #print("NONE")
            potential_subjects.append("")

        # A single expression
        case expr:
            subject = get_subject(expr, (ast.Eq))
            potential_subjects.append(subject)

    return set(potential_subjects)

def lit_transform(test, subject_id):
    match test:
        case ast.BoolOp(ast.Or(), [*values]):
            #It is guaranteed, that every node in the values is literal
            patterns = []
            for i in range(len(values)):
                patterns.append(ast.MatchValue(value = get_const_node(values[i])))
            return (ast.MatchOr(patterns), None)

        case ast.BoolOp(ast.And(), [*values]):
            # values either has a BoolOp(OR) where every expression is subject == literal
            # Or at least one subject == literal

            literal_node = None
            for node in values:
                match node:
                    case ast.BoolOp(ast.Or(), [*exprs]):
                        if get_subject(exprs) == subject_id: 
                            literal_node = node
                            break 
                    case _:
                        if not literal_node and get_subject(node) == subject_id:
                            literal_node = node
            # It is guaranteed that we find a literal node because of the analyzer (hopefully :P)

            match_case = lit_transform(literal_node, subject_id)[0]
            values.remove(literal_node)
            return (match_case, ast.BoolOp(ast.And(), values))

        case None:
            return (ast.MatchAs(), None)

        case expr:
            return (ast.MatchValue(value = get_const_node(expr)), None)
            
def _get_subject(compare, ops):
    #A compare node is "literal" if its left attribute is:
    # - A Name node and its comparators atribute is:
    #       - A single Constant ->(number or string)
    #       - An UnaryOp whose operator is USub ->(negative number)
    # - A single Constant ->(number or string) and its comparators attribute is a Name node
    # - An UnaryOp whose operator is USub ->(negative number) and its comparators attribute is a Name node 
    # The tuple of accepted operators for the comparator node is the second input
    
    match compare:
        case ast.Compare(ast.Name(id=var_id, ctx = _), [comp], [ast.Constant(_)]) if isinstance(comp, ops):
            return var_id
        case ast.Compare(ast.Constant(_), [comp], [ast.Name(id=var_id, ctx = _)]) if isinstance(comp, ops):
            return var_id
        case ast.Compare(ast.Name(id=var_id, ctx = _), [comp], [ast.UnaryOp(ast.USub(), ast.Constant(_))]) if isinstance(comp, ops):
            return var_id
        case ast.Compare(ast.UnaryOp(ast.USub(), ast.Constant(_)), [comp], [ast.Name(id=var_id, ctx = _)]) if isinstance(comp, ops):
            return var_id

    return False

def get_const_node(compare):
    # It is guaranteed that the input is a compare node that is literal
    if isinstance(compare.left, ast.Name):
        return compare.comparators[0]
    elif isinstance(compare.comparators[0], ast.Name):
        return compare.left
    raise ValueError(f"Cannot get the const node out of: \n {ast.dump(compare)}")

def get_subject(expr, ops = (ast.Eq,)):
    # An expression is literal if it compares a subject to a constant with the ast.Eq operator
    # In case of a list of nodes, like in a BoolOp, the BoolOp is considered literal if all of its values are literal, and have the same subject
    # The tuple of accepted operators for the comparators is the second input
    match expr:
        case [*nodes]:
            subject = {}
            for node in nodes:
                subj = get_subject(node, ops)
                if not subj:
                    return False
                subject[subj] = 1
            subject = False if len([*subject]) != 1 else [*subject][0]
            return subject
        case node:
            return _get_subject(node, ops) #!= False

def semi_analyze(test):
    # Only entering this function, if the branch isn't literal
    potential_subjects = []
    # The root node of the test of a branch can be:
    match test:
        # A list of expressions inside a BoolOp with AND / OR
        case ast.BoolOp(_, [*values]):     
            # Guaranteed, that not every expression is literal (LITERAL OR)
            # Neither is there a single expression in the list that is literal (LITERAL AND)
            # Branch is acceptable, if there is at least one expression, that is semi-literal
            for node in values:
                subj = list(semi_analyze(node))
                if subj:
                    potential_subjects += subj
                    
        # Nothing (else: block)
        case None:  
            #print("NONE")
            potential_subjects.append("")

        # A single expression
        case expr:
            subject = get_subject(expr, (ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.NotEq))
            potential_subjects.append(subject)

    #print(f"BRANCH: {test.lineno} POTSUBJECTS: {potential_subjects}")
    return set(potential_subjects)
 
def semi_transform(test):
    # Since it is guaranteed, that the test is not literal, we can never return an ast.MatchValue -- nothing for the value
    # All we can return is an ast.MatchAs(), with the guard being the actual test --> the ugly way
    return (ast.MatchAs(), test)

class LiteralCase:
    def __init__(self):
        self.subjects = {} # A dictionary, mapping If nodes (lineno) to a set of subject ID-s (variable names) -- Used in transform(), filled in visit()
        self.literal_branches = {} # A dictionary, mapping If nodes (lineno) to a list of literal branches (lineno) inside the If node. 

    def visit(self, node):
        branches = get_branches(node)
        potential_subjects = None
        self.literal_branches[node.lineno] = [branch.test.lineno for branch in branches]

        if len(branches) < MIN_BRANCHES:
            return False 

        # Checking if all the branches are in correct form and have the same subject
        for branch in branches:
            # First check if the branch is literal
            curr_subject = lit_analyze(branch.test)
            # If not, then check if its semi-literal
            if len(curr_subject) == 0:
                curr_subject = semi_analyze(branch.test)
                self.literal_branches[node.lineno].remove(branch.test.lineno)

            # Only accept If-nodes, that, if they have both literal, and semi-literal branches, they share subjects 
            if potential_subjects == None:
                potential_subjects = curr_subject
            elif curr_subject != set([""]):
                potential_subjects = potential_subjects.intersection(curr_subject)
            

        #print(f"IF NODE [{node.lineno}] subjects: {potential_subjects}")
        
        self.subjects[node.lineno] = potential_subjects
        #print(f"LITERAL BRANCHES: {self.literal_branches[node.lineno]} ")
        return (len(potential_subjects) > 0 and len(self.literal_branches[node.lineno]) > 0)

    def transform(self, node):
        branches = get_branches(node)
        if(len(self.subjects[node.lineno]) > 1):
            print(f"Node at line number {node.lineno} has multiple potential subjects: {self.subjects[node.lineno]}")
            print(f"Chosen at random for now.")
            # TODO
        
        subject_id = self.subjects[node.lineno].pop()
        # A match node has a 'subject': Should be a Name node 
        # Since the analyzer already made sure, that the subject is the same in all branches, we can skip that here
        
        subject = ast.Name(id=subject_id, ctx=ast.Load())
        # and a list of 'cases': each case being a 'match_case' Node
        # a 'match_case' has a 
        # - 'pattern': in this case, either a MatchValue(value=Constant(x)), a MatchAs(), or a MatchOr(patterns)
        # - 'body': This should just be the main 'If' node's body
        # - 'guard': an optional attribute, contains an expression that will be evaluated if the pattern matches the subject
        cases = []
        for branch in branches:
            if branch.test.lineno in self.literal_branches[node.lineno]: #If the branch is literal
                curr_pattern = lit_transform(branch.test, subject_id)
            else:
                curr_pattern = semi_transform(branch.test)
            #print(curr_pattern)
            cases.append(ast.match_case(pattern = curr_pattern[0], body = branch.body, guard = curr_pattern[1]))

        return ast.Match(subject = subject, cases = cases)
        