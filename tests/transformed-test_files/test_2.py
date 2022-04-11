match obj:
    case Class():
        pass

match obj:
    case Class(prop=2 | 4) | 2:
        pass

match obj:
    case Class(prop=2 | 3, prop2=5 | -5):
        pass

if obj.prop == 2 or obj.prop == 4:
    something()
elif isinstance(obj, SomeClass) and (obj.prop == 2 or obj.prop == 3) and something:
    something()


match obj:
    case Class(attr=2 | 3, pos=OtherClass(x=2 | 3, y=4 | 5)):
        pass

match obj:
    case Class(attr=2 | 3, pos=OtherClass(x=2 | 3, y=4 | 5)):
        pass


match obj:
    case Class(attr=-5 | 'asd') if something():
        pass

match obj:
    case SomeClass(x=3 | 5):
        pass
    case SomeClass(x=10 | 100):
        pass


match obj:
    case Cl1() | Cl2() | Cl3():
        something()
    case Cl3(val=2 | 4) | Cl4(val=2 | 4) | Cl5(val=2 | 4):
        something()


match obj:
    case some_module.SomeClass():
        pass
    case OtherClass():
        pass
    case tuple_of_classes():
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
