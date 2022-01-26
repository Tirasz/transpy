number = "asdasdasd"
asd = 12
def its_a_cat(asd):
    pass
def turn_around():
    pass
def give_lasagne():
    pass
def ignore_cat():
    pass
def its_a_dog(asd):
    pass
def give_pets():
    pass
def give_treats():
    pass
class Dog():
    pass
class Cat():
    pass
obj = Cat()
obj2 = Dog()
obj3 = Cat()
obj4 = Dog()

def some_function(in_number):
    print(in_number)
def something():
    pass
def something_else():
    pass
def anything(asd = 2):
    pass
class Class:
    pass
class OtherClass:
    pass
class SomeClass:
    pass
x = SomeClass()
a = Class()
b = OtherClass()
def any_bool_expression():
    pass
def one_line():
    pass
def two_lines():
    pass
def lot_of_lines():
    pass



if obj.prop == 2 or obj.prop == 4 or (obj.prop == 5 or obj.prop == 6):
    pass

if obj.prop == 3 or obj.prop == 5:
    pass

if isinstance(obj, Class):
    pass


if isinstance(obj, Class) and (obj.prop == 2 or obj.prop == 3) and (obj.prop2 == 5 or obj.prop2 == -5):
    pass


if isinstance(obj, Class) and (obj.attr == 2 or obj.attr == 3) and (isinstance(obj.pos, OtherClass) and (obj.pos.x == 2 or obj.pos.x == 3) and (obj.pos.y == 4 or obj.pos.y == 5)):
    pass

if isinstance(obj, Class) and (obj.attr == 2 or obj.attr == 3) and isinstance(obj.pos, OtherClass) and ( (obj.pos.x == 2 or obj.pos.x == 3) and (obj.pos.y == 4 or obj.pos.y == 5)):
    pass


if isinstance(obj, Class) and (obj.attr == -5 or obj.attr == "kek") and something():
    pass


if (obj.attr == 2 or obj.attr == 3) and ( (obj.pos.x == 2 or obj.pos.x == 3) and (obj.pos.y == 4 or obj.pos.y == 5)):
    pass

if (isinstance(obj, Class) and (obj.prop == 2 or obj.prop == 4)) or obj == 2:
    pass



if obj.prop == 2 or obj.prop == 4:
    something()
elif isinstance(obj, SomeClass) and (obj.prop == 2 or obj.prop == 3) and something:
    something()



if something[0] == 2 or something[0] == 4:
    asd()
elif (something[0] == 6 or something[0] == 69) and something():
    asd()


if something[0] == 2 or something[0] == 4:
    asd()
elif obj.prop > 10 and (obj.prop == 5 or obj.prop == 10):
    asd()


# Literal
if number == None:
    some_function(number)
elif number == 2 or number == 3 or number == 3:
    some_function(number)
elif (number == 4 or number == 5 or number == 6) and anything(1) and anything("Something"):
    some_function(number)
elif anything(2) and anything() and number == 7:
    some_function(number)
elif asd == 8 and (number == 9 or number == 10):
    some_function(asd)
    


# Literal with multiple subjects
if (number == 1 or number == 2) and (asd == 3 or asd == 4) and anything(): 
    some_function(number)
    some_function(asd)
elif number == 5 and asd == 6 and anything():                               
    some_function(number)
    some_function(asd)
#elif number == 7 or asd == 5: -- Would make it impossible to transform
#elif number == 7: -- Would fix the subject to number
#elif (asd == 8 or asd == 9) and anything(): -- Would fix the subject to asd
   

if something():
    print("asd")
elif something_else():
    print(2323)
elif number == 1 or number == 2:
    print("asd")


if isinstance(obj, SomeClass):
    if obj.x == 3 or obj.x == 5:
        pass
    elif obj.x == 10 or obj.x == 100:
        pass



if isinstance(obj, SomeClass) and (obj.x == 3 or obj.x == 5):
    pass
elif isinstance(obj, SomeClass) and (obj.x == 10 or obj.x == 100):
    pass

if isinstance(x, OtherClass) and (x.attribute == 42 and x.other_attribute == "something"):
    something(1)
    pass
    something(3)
elif isinstance(x, OtherClass) and ( (x.attribute == 12 or x.attribute == 24) and (x.other_attribute == "this" or x.other_attribute == "that") and (any_bool_expression()) ):
    something(1)
    pass
    something(3)
elif isinstance(x, OtherClass):
    something(1)
    something(2)
    something(3)



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

if any_bool_expression():
    something()
    something_else()

""" Nested If-s with no Pre-and-Post nest"""
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

something()
something_else()

"""Nested If-s with Pre and Post nest"""
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
    something(3)
    something(4)

something()
something_else()

""""Ugly" nested If-s"""
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
        
something()
something_else()


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

