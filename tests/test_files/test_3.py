if isinstance(obj, SomeClass):
    if obj.x == 3 or obj.x == 5:
        pass
    elif obj.x == 10 or obj.x == 100:
        pass

if isinstance(obj, Cat):
    if obj.color == 'black' or obj.color == 'gray':
        turn_around()
    elif obj.color == 'orange' and obj.weight == 'a lot':
        give_lasagne()
    else:
        ignore_cat()
elif isinstance(obj, Dog):
    if obj.color == 'black' or obj.color == 'gray':
        give_pets()
    elif obj.color == 'orange' and obj.weight == 'a lot':
        give_treats()
    else:
        ignore_cat()

if a == 2 or a == 6:
    if isinstance(b, Cat) and (b.color == "black" or b.color == "gray"):
        turn_around()
    elif isinstance(b, Cat) and b.color == 'orange' and b.weight == 'a lot':
        give_lasagne()
    if isinstance(b, Dog) and (b.color == "black" or b.color == "gray"):
        turn_around()
    elif isinstance(b, Dog) and b.color == 'orange' and b.weight == 'a lot':
        give_lasagne()

if isinstance(obj, Cat):
    if obj.color == 'black' or obj.color == 'gray':
        turn_around()
    elif obj.color == 'orange' and obj.weight == 'a lot':
        give_lasagne()
    else:
        ignore_cat()
elif isinstance(obj, Dog):
    if obj.color == 'black' or obj.color == 'gray':
        give_pets()
    elif obj.color == 'orange' and obj.weight == 'a lot':
        give_treats()
    else:
        ignore_cat()

if isinstance(obj2, Cat):
    something(1)
    if obj2.color == 'black' or obj2.color == 'gray':
        turn_around()
    elif obj2.color == 'orange' and obj2.weight == 'a lot':
        give_lasagne()
    else:
        ignore_cat()
elif isinstance(obj2, Dog):
    if obj2.color == 'black' or obj2.color == 'gray':
        give_pets()
    elif obj2.color == 'orange' and obj2.weight == 'a lot':
        give_treats()
    else:
        ignore_cat()
    something(2)


if isinstance(obj3, Cat):
    if asd.color == 'black' or asd.color == 'gray':
        turn_around()
    elif asd.color == 'orange' and asd.weight == 'a lot':
        give_lasagne()
    else:
        ignore_cat()
elif isinstance(obj3, Dog):
    if asd.color == 'black' or asd.color == 'gray':
        give_pets()
    elif asd.color == 'orange' and asd.weight == 'a lot':
        give_treats()
    else:
        ignore_cat()


if isinstance(obj4, Cat):
    if obj4.color == 'black' or obj4.color == 'gray':
        turn_around()
    elif obj4.color == 'orange' and obj4.weight == 'a lot':
        give_lasagne()
    else:
        ignore_cat()
else:
    if obj4 == "Dog" or obj4 == "Cat":
        give_lasagne()
    elif obj4 == 'Human':
        turn_around()
    else:
        pass


if isinstance(obj4, Cat):
    one_line()
    if obj4.color == 'black' or obj4.color == 'gray':
        turn_around()
    elif obj4.color == 'orange' and obj4.weight == 'a lot':
        give_lasagne()
    else:
        ignore_cat()
else:
    if obj4 == "Dog" or obj4 == "Cat":
        give_lasagne()
    elif obj4 == 'Human':
        turn_around()
    else:
        pass

if isinstance(obj4, Cat):
    two_lines()
    if obj4.color == 'black' or obj4.color == 'gray':
        turn_around()
    elif obj4.color == 'orange' and obj4.weight == 'a lot':
        give_lasagne()
    else:
        ignore_cat()
    two_lines()
else:
    if obj4 == "Dog" or obj4 == "Cat":
        give_lasagne()
    elif obj4 == 'Human':
        turn_around()
    else:
        pass

if isinstance(obj4, Cat):
    lot_of_lines()
    lot_of_lines()
    lot_of_lines()
    if obj4.color == 'black' or obj4.color == 'gray':
        turn_around()
    elif obj4.color == 'orange' and obj4.weight == 'a lot':
        give_lasagne()
    else:
        ignore_cat()
    lot_of_lines()
    lot_of_lines()
    lot_of_lines()
else:
    if obj4 == "Dog" or obj4 == "Cat":
        give_lasagne()
    elif obj4 == 'Human':
        turn_around()
    else:
        pass

if isinstance(obj, (Cl1, Cl3)):
    if obj.val == 4 or obj.val == 6:
        something()


def foo():
    if isinstance(obj, SomeClass) and something():
        if something_else():
            return obj.copy()
        return obj
    elif isinstance(obj, OtherClass):
        return 2