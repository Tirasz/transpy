import ast
def custom_hash(self):
    return hash(ast.dump(self))

def custom_eq(self, other):
    return hash(self) == hash(other)

ast.AST.__hash__ = custom_hash
ast.AST.__eq__ = custom_eq

import pkgutil
import importlib
import inspect
import sys
import plugins
from plugins.Base import get_branches
vprint = print if ("-v" in sys.argv[1:]) else lambda *a, **k: None

def load_plugins():
    """Returns a list of objects that implement the Base plugin interface."""
    Plugins = []
    # Loading python modules from plugins folder
    Modules = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules(plugins.__path__, plugins.__name__ + ".")
    }

    for plugin_name in Modules.keys():
        # Checking every class in the module
        for name, cls in inspect.getmembers(Modules[plugin_name], inspect.isclass):
            if issubclass(cls, plugins.Base.TransformerBase):
                Plugins.append(cls())
                print(f"PLUGIN: {name} succesfully loaded!")
    return Plugins

class Analyzer(ast.NodeVisitor):
    def __init__(self, transformers):
        self.transformers = transformers
        self.branches = {}
        # Mapping an If-node to a list of branches
        self.results = {}
        # Mapping a branch to plugin capable of transforming it. (except the else: branch, where the transformed branch is mapped)
        self.subject = {}
        # Mapping an If-node to a subject

    def visit_If(self, node):
        self.branches[node] = get_branches(node)
        temp_results = {}

        for branch in self.branches[node]:
            if branch.test is not None:
                temp_results[branch] = []
            else:
                self.results[branch] = ast.match_case(pattern = ast.MatchAs(), body = branch.body, guard = None)

        for plugin in self.transformers: 
            for branch in temp_results.keys(): 
                subjects = plugin.visit(branch)
                temp_results[branch].append((plugin, subjects))
        # temp_results is a dictionary mapping the (not trivial) branches of the current If-node to a list of tuples: (plugin, set(subjects))


        # First, for every branch, union all of their possible subjects
        curr_subjects = {}
        for branch in temp_results.keys():
            curr_subjects[branch] = set()
            for pl_sb in temp_results[branch]:
                curr_subjects[branch] = curr_subjects[branch].union(pl_sb[1])
            #print(f"BRANCH({branch.test.lineno}): {curr_subjects[branch]}")
        # curr_subject is a dictionary, mapping branches of the current if-node to a set of possible subjects


        # Second, intersect the possible subjects over all the branches
        possible_subjects = curr_subjects[list(curr_subjects)[0]]
        for branch in curr_subjects.keys():
            possible_subjects = possible_subjects.intersection(curr_subjects[branch])

        #print(f"POSSIBLE SUBJECTS: {possible_subjects}")

        # If we get an empty set, it means that there isnt a single subject that could be used for transforming all the branches.
        if(len(possible_subjects) == 0):
            print(f"If-node ({node.lineno} IS NOT TRANSFORMABLE!)")
            del self.branches[node]
            return

        # If we get a set with multiple elements, that means that all branches can be transformed by using any of the possible subjects.
        if(len(possible_subjects) > 1):
            chosen = set()
            chosen.add(possible_subjects.pop())
            possible_subjects = chosen
            print(f"If-node ({node.lineno}) HAS MULTIPLE POSSIBLE SUBJECTS. CHOOSING RANDOM ({possible_subjects}) FOR NOW.")
        
        self.subject[node] = list(possible_subjects)[0]

        # After we have chosen a subject, iterate over all the plugins, and remove the ones that cannot transform the branch using the chosen subject
        for branch in temp_results.keys():
            temp_results[branch] = [pl_sb for pl_sb in temp_results[branch] if not pl_sb[1].isdisjoint(possible_subjects)]
            #print(f"REMAINING: {temp_results[branch]}")

            # This shouldnt be possible
            if len(temp_results[branch]) == 0:
                raise Exception("NO POSSIBLE PLUGIN REMAINING! THIS SHOLDNT HAPPEN!!")

            if len(temp_results[branch]) > 1:
                print(f"BRANCH ({branch.test.lineno} HAS MULTIPLE POSSIBLE PLUGINS. CHOOSING RANDOM FOR NOW.)")

            self.results[branch] = temp_results[branch][0][0]
        
        # self.branches contains the branches for an If-node
        # self.results contains the chosen transforming plugin for each branch of the If-node
        # self.subject contain the chosen subject for the If-node
        
       
        



def main():
    with open("test.py", "r") as src:
        tree = ast.parse(src.read())    

    analyzer = Analyzer(load_plugins())    
    analyzer.visit(tree)

    
    with open("transformed.py", "w") as out:
        for node in analyzer.branches.keys():
            subject = analyzer.subject[node]
            cases = []
            out.write("#" + "-"*10 + str(node.lineno) + "-"*10 + f"[{type(subject).__name__}]" +"\n")

            for branch in analyzer.branches[node]:
                #print(f"TRANSFORMING BRANCH: ({branch.test.lineno}) WITH SUBJECT: {subject_id}")
                if branch.test is not None:
                    plugin = analyzer.results[branch]
                    transformed_branch = plugin.transform(branch, subject)
                else:
                    transformed_branch = analyzer.results[branch]

                cases.append(transformed_branch)

            transformed_node = ast.Match(subject = subject, cases = cases)
            
            out.write(ast.unparse(transformed_node) + "\n")
        

if __name__ == "__main__":

    main()
    vprint("Done")

    
