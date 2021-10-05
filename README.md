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
## Dealing with '[and]'
Since we are still talking about literal cases, (with a subject, and only literals to compare to)  
I think 'and'-s are already used kind of like 'Guards'. What i mean is:  
- If we are checking for equality, then it doesn't make much sense to also check for another one, like ```if x == 4 and x == 5```
    - Therefore the only reason to use 'and' in a case like this is to "Guard" against something, for e.g.: ```if isinstance(x, int) and x == 5``` or ```if x == 5 and (bool_expression)```
    - This means, after identifying the actual literal cases to match against, i should be able to just take the "remaining expressions" and put it in the case Guard. 
    - For eg:
    ```python
        if (x == 1 or x == 2 or x == 3) and (bool_expr):
            ...
    ```
    The literal cases are ```1 | 2 | 3``` and the Guard will be the "remaining": ```(bool_expr)```
- If we are comparing to a literal, then the whole thing is already getting put into the Guard. 
    - So something like ``` if x > 0 and x < 100``` can be turned into ``` case x if x > 0 and x < 100```.

Now, I'm going to be honest, I have absolutely no idea how to even begin implementing this.  
I also have no idea how to deal with cases like ```if something or something and something or something and (something and something or something)....``` 
