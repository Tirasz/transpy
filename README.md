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
### How I plan to do it:
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
        3. And their *body* should be a list of nodes found either in:
            1. The *If* node's *body* section (elif ...:)
            2. The *If* node's *orelse* section (else ...:)
        4. Set the *Match* node's cases to be equal to a list of the *match_cases*
4. Merge the transformed code with the source code, replacing the old structures with the transformed ones. 
    1. Maybe this way I can minimize the collateral damage that ast.unparse can potentially cause.


# Second task
More complex cases:
```python

if number == 0 or number == 1 or ...:
    ...
elif not number == 1:
    ...
elif number > 5:
    ...
elif number is not None:
    ...
else:
   ...

```  

Basically I need a way to handle keywords: '[not], [or], [and], [is not]', and comparators other than ['=='], like '[>], [<], etc.'
'or' & 'and' are both 'BoolOp'-s. 'BoolOp'-s have an operator ('and' & 'or'), and a list of values. Consecutive operations with the same operators are collapsed into one 'BoolOp'.
e.g: x or y or z --> BoolOp(Or, x,y,z)

