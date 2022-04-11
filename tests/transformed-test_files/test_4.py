
# Comment before If (Literal)
# PRESERVED COMMENTS: 
 # Comment before If (Literal)
 # Comment on If-s line (Literal)
 # Comment inside If (Literal)
 # Comment before If (OR pattern)
 # Comment on If-s line (OR pattern)
 # Comment inside If (OR pattern)
 # Comment before If (ClassPattern)
 # Comment inside If (ClassPattern)
 # Comment before If (SingletonPattern)
 # Comment on If-s line (SingletonPattern)
 # Comment before If (GuardPattern)
match asd:
    case 2:
        print(asd)
    case 4 | 5 | 6:
        print(asd)
    case SomeClass(prop1=3 | None, prop2=2):
        print(asd)
    case None:
        print(asd)
    case SomeClass() if some_function():
        print(asd)
    # Comment end If (GuardPattern)
    # Comment end If (GuardPattern)
    # Comment end If (GuardPattern)
# Comment after whole If-node




"""Multiline comment
    number one
"""

# PRESERVED COMMENTS: 
 # Its a black or gray cat (scary)
 # Just gtfo
 # Its a fat orange cat
 # So it has to be garfield right?
 # Its garfield! (cute)
 # Boring cat, dont care + l + ratio
match obj:
    case Cat(color='black' | 'gray'):
        turn_around()
    case Cat(color='orange', weight='a lot'):
        give_lasagne()
    case Cat():
        ignore_cat()
    case Dog(color='black' | 'gray'):
        give_pets()
    case Dog(color='orange', weight='a lot'):
        give_treats()
    case Dog():
        ignore_cat()

"""Multiline comment
    number two
"""


match number:
    case None:
        some_function(number)
    case 2 | 3 | 3:
        some_function(number)
    case 4 | 5 | 6 if anything(1) and anything('Something'):
        some_function(number)
    case 7 if anything(2) and anything():
        some_function(number)
    case 9 | 10 if asd == 8:
        some_function(asd)

