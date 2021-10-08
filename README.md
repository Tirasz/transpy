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
More complex (literal) cases:
```python

if number == 0 or number == 1 or ...:
    ...
elif not number == 1:
    ...
elif number == 7 or number > 5:
    ...
elif number is not None:
    ...
else:
   ...

```  

Basically I need a way to handle keywords: '[not], [or], [and], [is not]', and comparators other than ['=='], like '[>], [<], etc.'


## OR-patterns
In a match statemenet, we can combine multiple patterns in one case, so that if at least one pattern matches, the whole pattern matches.  
The alternative patterns can bind variables, as long as they all bind the same set of variables (excluding _ ).  
Using OR-patterns, it is possible to transform something like this:  
```python 
if number == 1 or number == 2 or number == 4:
    ...
elif number == 5 or number == 6 or number == 8:
    ...
```
Into:
```python
match number:
    case 1 | 2 | 4:
        ...
    case 5 | 6 | 8:
        ...
```
## Guards
In a match statement, we can add a 'Guard' for every case. The case branch is only taken, if the 'Guard' evaluates to True.  
The 'Guard' is only evaluated after a succesful match.  
It's very important ~~and a bit confusing~~ , that there is no back-tracking in pattern matching.  
So if there is a match, but the guard fails, the case is skipped, and no other potential matches are tested in the case.  
(https://ncik-roberts.github.io/posts/pep622.html)  
Using Guards, it is possible to transform something like this:  
```python 
if number == 0:
    ...
elif number < 0:
    ...
elif number >= 1:
    ...
```
Into:
```python 
match number:
    case 0:
        ...
    case x if x < 0:
        ...
    case x if x >= 1:
        ....
```
## Dealing with [and] & [or]
### BoolOp-s
In the python AST, the operation 'and' & 'or' are represented with ```ast.BoolOp(op, values)```  
Where the 'op' can be ```ast.And``` or ```ast.Or```, and the values are the values involved.  
Consecutive operations with the same operator are collapsed:  
```if a or b or c ``` gets turned into ```ast.BoolOp(ast.Or,[a,b,c])```  


Like most languages, python has the operator precedence (from weakest to strongest):
```python 
1. or
2. and
3. not x
4. is not; not in;
```
In AST terms, the weakest always goes on the top of the tree, while the strongest are pushed down, since they are getting evaluated first.
For example: 
```python 
if a or b or c and d
=
if a or b or (c and d)
``` 
Looks something like this in the AST:
```python 
BoolOp(OR, [a, b, BoolOp(AND, c, d)])
```
### The root is ```BoolOp(OR, values)```  

In most cases, the root of an If-node's test will be a ``` ast.BoolOp(OR, [values]) ``` node.  
This makes analyzing it pretty easy, since all i have to do, is check the list of values.  
If the values are all ``` ast.Compare(left, ops, ast.Eq())``` nodes, then that means they are checking for equality, which means that I just need to make sure they are all comparing the same subject to a literal.  
If that's the case, then i can just use the OR-patterns in the match case, like mentioned above.

Sadly in any other case, the best I can do is to put the whole test into the Guard.  
For example, lets say i find an ```ast.Compare(left, ops, ast.Lt()) ``` in the list if values.  
```python 
if a == 1 or a == 2 or a < 0:
   ...
```
Then i cant turn it into a match case like:
```python
match a:
    case 1 | 2 | _ if a < 0
```
Because how Guards work. If a = 1, it wont match since a is not less than 0, and it wont even check the remaining cases.
Something like
```python
match a:
    case _ | 1 | 2 if a < 0
```
Won't work either, because of the same reason.
So the only way i can turn it into a match case is:
```python
match a:
    case x if (x == 1 or x == 2 or x < 0:)
```
This works, but is also ugly. (Maybe make this kind of transformation optional?)  
Same thing happens if i find a ``` BoolOp(AND, values) ``` in the list of values.
```python
if a == 0 or a == 1 and some_bool_func(a) or a == 5:
=
if a == 0 or (a == 1 and some_bool_func(a)) or a == 5:
```
Intuitively, i would transform it into:
```python 
match a:
    case 0 | 5 | 1 if some_bool_func(a)
```
Which after looking at it for more than 2 seconds is obviously wrong.  
So the only way in this case is also the ugly way:  
```python
match a:
    case x if (x == 0 or x == 1 and some_bool_func(x) or x == 5)
```

### The root is ```BoolOp(AND, values)```
The root of the If node's test is a ``` BoolOp(AND, values) ``` node only if:  
- The test contains no ```or``` operators
- Or if it contains them, they are parenthesized, and are separated with ```and```-s.
  
This pretty much means that the test is in CNF. (i think?)  
In this case, if i'm able to detect a node in the list of values, that contains valid literal cases ONLY, then i could transform them like so:  
e.g.: 
```python 
if (x == 1 or x == 2 or x == 3) and boolexp(x) 
```
Can be turned into:
```python
match x:
    case 1 | 2 | 3 if boolexp(x)
```
Basically, the valid cases get put into the case with the OR-pattern, and the rest goes into the case's Guard.
In any other case, its the ugly way again:  
```python
if (x <= 100 or x > 1000) and boolexp(x)
```
Has to be turned into:
```python
match x:
    case _ if (x <= 100 or x > 1000) and boolexp(x)
```


