# It's my thesis
Its about transforming Python source code and stuff.  
It also got accepted as a submission at the ICSME 2022 in the SCAM Engineering Track for some reason. <sub><sup>(🤓)</sup></sub>   
Both the submitted (English) paper and the original (Hungarian) thesis can be found in the repo.

# What it does
Transforms suitable conditional branches into the newer, more trendy form of structural pattern matching.  
For example:  
```python
if isinstance(obj, Cat):
    if obj.color == 'black' or obj.color == 'gray':
        turn_around()
    elif obj.color == 'orange' and obj.weight == 'a lot':
        give_lasagne()
    else:
        ignore_cat()
```

<p align="center">
🠋🠋🠋🠋
</p>

```python
match obj:
    case Cat(color='black' | 'gray'):
        turn_around()
    case Cat(color='orange', weight='a lot'):
        give_lasagne()
    case Cat():
        ignore_cat()

```
# Usage
Pretty straight forward, just run the module with python. the only required argument is the absolute path of the file / project you want to transform.  
Use the ``-h`` flag for more info.
