# transpy
Transforming "old" Python code to 3.10+

# First task
Detect and transform the most basic case:
```python

if number == 0:
    ...
elif number == 1:
    ...
elif number == 2:
    ...
elif ...
else:
   ...

```  
Into something like this: ~~Wish it had syntax highlighting~~

```python

match number:
    case 0:
        ...
    case 1:
        ...
    case 2:
        ...
    case ...
    case x:
        ...

```  
## How I plan to do it:
1. Analyze the source:
    1. Using ast.NodeVisitor visit every *If* node. 
    2. Since *elif* clauses appear as extra *If* nodes within the *orelse* section of the previous node, I will need to somehow check the "depth" of the main *If* node. 
    3. In this case, I will also have to make sure, that the *test* sections look something like this: *Name* *Eq* *Constant* where the id of the *Name* node should be equal in all the *test* nodes.
2. Separate the transformable code from the source
    1. Since ast.unparse might not produce code that is equal to the source, it seems like a good idea to only unparse things that are necessary.
3. Transform the source:
    1. Using ast.NodeTransformer, transform the If-elif structures into match statements
        1. Turn the main *If* node into a *Match* node with the *Subject* being the *Name* node that is equal in all *elif* nodes.
        2. Turn every *test* node into a *match_case* where their *pattern* is either
            1. *MatchValue(value = Constant())* (elif ...: )
            2. *MatchAs()* (else: )
        3. And their *body* should be equal to their corresponding *If* node's body
        4. Set the *Match* node's cases to be equal to a list of the previous *match_case*'s
4. Merge the transformed code with the source code, replacing the old structures with the transformed ones. 
    1. Maybe this way I can minimize the collateral damage that ast.unparse can potentially cause.

## How to try:
0. Make sure you are using a Python 3.10+ interpeter.
1. Dump all the files in the repo into a folder.
2. Make a test.py, fill it with test cases.
3. Run 'python analyzer.py'
4. Check newly made 'to_transform.py' file to see if it recognized the correct cases.
5. Run 'python transformer.py'
6. Check newly made 'transformed.py' file to see if it correctly transformed the structures.
    
