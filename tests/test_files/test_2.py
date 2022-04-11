if isinstance(obj, Class):
    pass

if (isinstance(obj, Class) and (obj.prop == 2 or obj.prop == 4)) or obj == 2:
    pass

if isinstance(obj, Class) and (obj.prop == 2 or obj.prop == 3) and (obj.prop2 == 5 or obj.prop2 == -5):
    pass

if obj.prop == 2 or obj.prop == 4:
    something()
elif isinstance(obj, SomeClass) and (obj.prop == 2 or obj.prop == 3) and something:
    something()


if isinstance(obj, Class) and (obj.attr == 2 or obj.attr == 3) and (isinstance(obj.pos, OtherClass) and (obj.pos.x == 2 or obj.pos.x == 3) and (obj.pos.y == 4 or obj.pos.y == 5)):
    pass

if isinstance(obj, Class) and (obj.attr == 2 or obj.attr == 3) and isinstance(obj.pos, OtherClass) and ( (obj.pos.x == 2 or obj.pos.x == 3) and (obj.pos.y == 4 or obj.pos.y == 5)):
    pass


if isinstance(obj, Class) and (obj.attr == -5 or obj.attr == "asd") and something():
    pass

if isinstance(obj, SomeClass) and (obj.x == 3 or obj.x == 5):
    pass
elif isinstance(obj, SomeClass) and (obj.x == 10 or obj.x == 100):
    pass


if isinstance(obj, (Cl1, Cl2, Cl3)):
    something()
elif isinstance(obj, (Cl3, Cl4, Cl5)) and (obj.val == 2 or obj.val == 4):
    something()


if isinstance(obj, some_module.SomeClass): 
    pass
elif isinstance(obj, OtherClass):
    pass
elif isinstance(obj, tuple_of_classes):
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
