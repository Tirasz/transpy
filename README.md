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
