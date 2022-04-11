match obj:
    case SomeClass(x=3 | 5):
        pass
    case SomeClass(x=10 | 100):
        pass

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

match a:
    case 2 | 6:
        match b:
            case Cat(color='black' | 'gray'):
                turn_around()
            case Cat(color='orange', weight='a lot'):
                give_lasagne()
        match b:
            case Dog(color='black' | 'gray'):
                turn_around()
            case Dog(color='orange', weight='a lot'):
                give_lasagne()

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

match obj2:
    case Cat(color='black' | 'gray'):
        something(1)
        turn_around()
    case Cat(color='orange', weight='a lot'):
        something(1)
        give_lasagne()
    case Cat():
        something(1)
        ignore_cat()
    case Dog(color='black' | 'gray'):
        give_pets()
        something(2)
    case Dog(color='orange', weight='a lot'):
        give_treats()
        something(2)
    case Dog():
        ignore_cat()
        something(2)


match obj3:
    case Cat():
        match asd.color:
            case 'black' | 'gray':
                turn_around()
            case 'orange' if asd.weight == 'a lot':
                give_lasagne()
            case _:
                ignore_cat()
    case Dog():
        match asd.color:
            case 'black' | 'gray':
                give_pets()
            case 'orange' if asd.weight == 'a lot':
                give_treats()
            case _:
                ignore_cat()


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
    case Cat(color='black' | 'gray'):
        one_line()
        turn_around()
    case Cat(color='orange', weight='a lot'):
        one_line()
        give_lasagne()
    case Cat():
        one_line()
        ignore_cat()
    case 'Dog' | 'Cat':
        give_lasagne()
    case 'Human':
        turn_around()
    case _:
        pass

match obj4:
    case Cat(color='black' | 'gray'):
        two_lines()
        turn_around()
        two_lines()
    case Cat(color='orange', weight='a lot'):
        two_lines()
        give_lasagne()
        two_lines()
    case Cat():
        two_lines()
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

match obj:
    case Cl1(val=4 | 6) | Cl3(val=4 | 6):
        something()


def foo():
    match obj:
        case SomeClass() if something() and something_else():
            return obj.copy()
            return obj
        case OtherClass():
            return 2
