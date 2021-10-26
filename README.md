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
For example, lets say i find an ```ast.Compare(left, ops, ast.Lt()) ``` in the list of values.  
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

# Literal case
  * **If-node**: In the python AST, it represents an ```if``` statement. It has the attributes: test, body, orelse.  
      * The test holds a single node, the body and the orelse each hold a list of nodes.  
      * Since the ```elif``` clauses dont have special representation in the AST, they **appear as extra If-nodes** within the orelse section of the previous one.  
      * To work with this more comfortably, I thought it would be a good idea, to **separate every If-node into a list of branches**.  

  * **Branch**: A branch represents an ```if / elif``` statement. It has the attributes: test, body. 
      * Final ```else``` statements dont have a test attribute.
      * When processing an **If-node**, the first thing I do, is make a list of **branches**, to represent the **If-node**.  

  * **Compare-node**: Represents a comparison of two or more values in the AST. It has the attributes: left, ops, comparators.  
      * The left attribute represents the first value in the comparison.
      * The ops attribute is the list of **operators**
      * The comparators is the list of values after the first element in the comparison.

  * **operators**: Represents comparator tokens in the AST, such as ```==```, ```>```, ```>=```, etc..

  * **BoolOp-node**: Represents a boolean operation in the AST. It has the attributes: op, values.
      * The op attribute represents either the ```and``` or the ```or``` tokens.
      * The values attribute is a list of nodes, containing the values involved in the boolean operations.
      * Consecutive operations with the same operator are collapsed into one **BoolOp-node** with multiple values.

  * **Constant-node**: Represents a constant literal in the AST. Its only attribute is value.
      * The value attribute can represent simple types such as ```number```, ```string```, or ```None```, but also immutable container types if all of their elements are constant.
      * Negative numbers are represented with the **Constant-node** being inside an **UnaryOp** node.

  * **Subject**: A **Compare-node** has a subject, if either its left, or its comparators attribute is a singe **Name-node**. 
      * For every **Branch** there is a set of **subjects** derived from its test attribute -- Can be an empty set
      * The **subject** of an **If-node** is the intersection of all of its **branches** subjects.
      * At least one **subject** is necessary for transforming an **If-node** into a match statement.

  * **Literal**: 
      * A **Compare-node** is **Literal**, if it has a **Subject**, and it compares that subject to a **Constant-node** with the **Equality** operator.
      * A **Branch** is literal if its test is:  
        -- A single, **Literal Compare-node**.  
        -- A **BoolOp-node** with the ```or``` operator, where every node inside its values atrribute is a **Literal Compare-node**.  
        -- A **BoolOp-node** with the ```and``` operator, where at least one node inside its values attribute is either a **Literal Compare-node**, or a **Literal BoolOp-node**
         
         -- Nothing --> its an ```else``` statement. 
  * **Semi-literal**:
      * A **Compare-node** is **Semi-literal**, if it has a **Subject**, and it compares that subject to a **Constant-node** with **ANY** operator.
      * A **Branch** is semi-literal if its test is:  
        -- A single, **Semi-literal Compare-node**.  
        -- A **BoolOp-node** with **ANY** operator, where at least one node inside its values atrribute is a **Semi-literal Compare-node**.  

        -- Nothing --> its an ```else``` statement.   
        
In order for an **If-node** to be considered **Literal** it has to fulfill some conditions:  
    -- Every branch has to be **Semi-literal**, with at least one being **Literal**.  
    -- All branches must share at least one **Subject**.  
    
I think its clear, that **Semi-literal** cases cannot be transformed into a match case without it being ugly. 
In spite of that, I didn't want to throw away every **If-node** that had like 5 **Literal** branches, that could be perfectly transformed, and one **Semi-literal** one,  
so I thought the best way to combine these two was the definition above.
Maybe this is a bad idea, maybe its not, I dont know.
Sidenote: I came up with the name **LiteralCase** from:  
https://www.python.org/dev/peps/pep-0634/#literal-patterns
    
# Second task
Detect and transform cases like:
```python

if isinstance(x, int):
    ...
elif isinstance(x, str):
    ...
elif isinstance(x, AnyClass):
    ...

```  
Into something like this: 

```python

match number:
    case int():
        ...
    case str():
        ...
    case AnyClass():
        ...

```  

Later, this could be improved by using the actual Class Patterns:  
(https://www.python.org/dev/peps/pep-0634/#class-patterns)  
```python

if isinstance(x, int):
    ...
elif isinstance(x, str):
    ...
elif isinstance(x, AnyClass) and ( x.something == "something" or x.something == 42) and (x.other_thing == "idk"):
    ...
elif isinstance(x, OtherClass):
    if x.attribute == 42 and x.other_attribute == "something":
        ...
    elif (x.attribute == 12 or x.attribute == 24) and (x.other_attribute == "this" or x.other_attribute == "that") and (any_bool_expression()):
        ...

```
-->  
```python

match x:
    case int():
        ...
    case str():
        ...
    case AnyClass(something = "something" | 42, other_thing = "idk"):
        ...
    case OtherClass(attribute = 42, other_attribute = "something"):
        ...
    case OtherClass(attribute = 12 | 24, other_attribute = "this" | "that") if any_bool_expression():
        ...

```  
Now, this looks cool, but also scary.