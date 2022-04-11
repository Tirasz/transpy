
# Comment before If (Literal)
if asd == 2: # Comment on If-s line (Literal)
    # Comment inside If (Literal)
    print(asd)
# Comment before If (OR pattern)
elif asd == 4 or asd == 5 or asd == 6: # Comment on If-s line (OR pattern)
    print(asd)
    # Comment inside If (OR pattern)
# Comment before If (ClassPattern)
elif isinstance(asd, SomeClass) and ((asd.prop1 == 3 or asd.prop1 is None) and asd.prop2 == 2):
    # Comment inside If (ClassPattern)
    print(asd)
# Comment before If (SingletonPattern)
elif asd is None: # Comment on If-s line (SingletonPattern)
    print(asd)
# Comment before If (GuardPattern)
elif isinstance(asd, SomeClass) and some_function():
    # Comment inside If (GuardPattern)
    print(asd)
    # Comment end If (GuardPattern)
    # Comment end If (GuardPattern)
    # Comment end If (GuardPattern)
# Comment after whole If-node




"""Multiline comment
    number one
"""

if isinstance(obj, Cat):
    # Its a black or gray cat (scary)
    if obj.color == 'black' or obj.color == 'gray':
        turn_around() # Just gtfo
    # Its a fat orange cat
    # So it has to be garfield right?
    elif obj.color == 'orange' and obj.weight == 'a lot':
        give_lasagne() # Its garfield! (cute)
    else: # Boring cat, dont care + l + ratio
        ignore_cat()
elif isinstance(obj, Dog):
    """
    Multiline comment
    number three
    inside if
    """
    if obj.color == 'black' or obj.color == 'gray':
        give_pets()
    elif obj.color == 'orange' and obj.weight == 'a lot':
        give_treats()
    else:
        ignore_cat()

"""Multiline comment
    number two
"""


if number == None:
    """
    Multiline comment 
    """
    some_function(number)
elif number == 2 or number == 3 or number == 3:
    some_function(number)
elif (number == 4 or number == 5 or number == 6) and anything(1) and anything("Something"): 
    """
    Multiline comment 
    """
    some_function(number)
elif anything(2) and anything() and number == 7:
    """asdasdasd"""
    some_function(number)
elif asd == 8 and (number == 9 or number == 10):
    some_function(asd)

