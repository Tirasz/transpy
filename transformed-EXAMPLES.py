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


match obj:
    case SomeClass(x=3 | 5):
        pass
    case SomeClass(x=10 | 100):
        pass



if isinstance(obj, SomeClass) and (obj.x == 3 or obj.x == 5):
    pass
elif isinstance(obj, SomeClass) and (obj.x == 10 or obj.x == 100):
    pass

match x:
    case OtherClass(attribute=42, other_attribute='something'):
        something(1)
        pass
        something(3)
    case OtherClass(attribute=12 | 24, other_attribute='this' | 'that') if any_bool_expression():
        something(1)
        pass
        something(3)
    case OtherClass():
        something(1)
        something(2)
        something(3)



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

something()
something_else()

"""Nested If-s with Pre and Post nest"""
if isinstance(obj2, Cat):
    something(1)
    match obj2.color:
        case 'black' | 'gray':
            turn_around()
        case 'orange' if obj2.weight == 'a lot':
            give_lasagne()
        case _:
            ignore_cat()
elif isinstance(obj2, Dog):
    match obj2.color:
        case 'black' | 'gray':
            give_pets()
        case 'orange' if obj2.weight == 'a lot':
            give_treats()
        case _:
            ignore_cat()
    something(2)
    something(3)
    something(4)

something()
something_else()

""""Ugly" nested If-s"""
if isinstance(obj3, Cat):
    match asd.color:
        case 'black' | 'gray':
            turn_around()
        case 'orange' if asd.weight == 'a lot':
            give_lasagne()
        case _:
            ignore_cat()
elif isinstance(obj3, Dog):
    match asd.color:
        case 'black' | 'gray':
            give_pets()
        case 'orange' if asd.weight == 'a lot':
            give_treats()
        case _:
            ignore_cat()
        
something()
something_else()


match obj4:
    case Cat(color='black' | 'gray'):
        turn_around()
    case Cat(color='orange', weight='a lot'):
        give_lasagne()
    case Cat():
        ignore_cat()
    case 'Dog' | 'Cat':
        give_lasagne()
    case 'Human':
        turn_around()
    case _:
        pass


match obj4:
    case Cat():
        one_line()
        match obj4.color:
            case 'black' | 'gray':
                turn_around()
            case 'orange' if obj4.weight == 'a lot':
                give_lasagne()
            case _:
                ignore_cat()
    case 'Dog' | 'Cat':
        give_lasagne()
    case 'Human':
        turn_around()
    case _:
        pass

match obj4:
    case Cat():
        two_lines()
        match obj4.color:
            case 'black' | 'gray':
                turn_around()
            case 'orange' if obj4.weight == 'a lot':
                give_lasagne()
            case _:
                ignore_cat()
        two_lines()
    case 'Dog' | 'Cat':
        give_lasagne()
    case 'Human':
        turn_around()
    case _:
        pass

match obj4:
    case Cat():
        lot_of_lines()
        lot_of_lines()
        lot_of_lines()
        match obj4.color:
            case 'black' | 'gray':
                turn_around()
            case 'orange' if obj4.weight == 'a lot':
                give_lasagne()
            case _:
                ignore_cat()
        lot_of_lines()
        lot_of_lines()
        lot_of_lines()
    case 'Dog' | 'Cat':
        give_lasagne()
    case 'Human':
        turn_around()
    case _:
        pass

