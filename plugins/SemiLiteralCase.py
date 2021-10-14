import ast
from plugins.Base import get_branches, MIN_BRANCHES, SubjectTransformer
from plugins.LiteralCase import analyze_test as lit_analyze
from plugins.LiteralCase import transform_test as lit_transform
from plugins.LiteralCase import get_subject



def analyze_test(test):
    # Only entering this function, if the branch isn't literal
    potential_subjects = []
    # The root node of the test of a branch can be:
    match test:
        # A list of expressions inside a BoolOp with OR
        case ast.BoolOp(ast.Or(), [*values]):          
            # Guaranteed, that not every expression is literal
            # Branch is acceptable, if at least one expression is semi-literal, against the same subject
            for node in values:
                subj = get_subject(node, (ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.NotEq, ast.Eq))
                if subj:
                    potential_subjects.append(subj)

        # A list of expressions inside a BoolOp with AND
        case ast.BoolOp(ast.And(), [*values]):          
            # Guaranteed, that there isnt a BoolOp(OR) in the list that is literal
            # Neither is there a single expression in the list that is literal
            # Branch is acceptable, if there is a BoolOp(OR) that is semi-literal or at least one expression, that is semi-literal
            for node in values:
                match node:
                    case ast.BoolOp(ast.Or(), [*exprs]):
                        for node in exprs:
                            subj = get_subject(node, (ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.NotEq, ast.Eq))
                            if subj:
                                potential_subjects.append(subj)
                    case _:
                        subject = get_subject(node,  (ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Eq, ast.NotEq))
                        if subject:
                            potential_subjects.append(subject)

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
 
        
def transform_test(test):
    # Since it is guaranteed, that the test is not literal, we can never return an ast.MatchValue -- nothing for the value
    # All we can return is an ast.MatchAs(), with the guard being the actual test --> the ugly way
    return (ast.MatchAs(), test)



class SemiLiteralCase:
    def __init__(self):
        self.subjects = {}
        self.literal_branches = {}

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
                curr_subject = analyze_test(branch.test)
                self.literal_branches[node.lineno].remove(branch.test.lineno)

            # Only accept If-nodes, that, if they have both literal, and semi-literal branches, they share subjects 
            if potential_subjects == None:
                potential_subjects = curr_subject
            elif curr_subject != set([""]):
                potential_subjects = potential_subjects.intersection(curr_subject)
            

        #print(f"IF NODE [{node.lineno}] subjects: {potential_subjects}")
        
        self.subjects[node] = potential_subjects
        #print(f"LITERAL BRANCHES: {self.literal_branches[node.lineno]} ")
        return (len(potential_subjects) > 0 and len(self.literal_branches[node.lineno]) != len(branches) and len(self.literal_branches[node.lineno]) > 0)

    def transform(self, node):
        branches = get_branches(node)
        if(len(self.subjects[node]) > 1):
            print(f"Node at line number {node.lineno} has multiple potential subjects: {self.subjects[node]}")
            print(f"Chosen at random for now.")
            # TODO
        
        subject_id = self.subjects[node].pop()
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
                curr_pattern = transform_test(branch.test)
            #print(curr_pattern)
            cases.append(ast.match_case(pattern = curr_pattern[0], body = branch.body, guard = curr_pattern[1]))

        return ast.Match(subject = subject, cases = cases)
        