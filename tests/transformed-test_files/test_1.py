match obj.prop:
    case 2 | 4 | 5 | 6:
        pass
    case 3 | 5:
        pass

match something[0]:
    case 2 | 4:
        pass
    case 6 | 69 if something():
        pass

match number:
    case None:
        pass
    case 2 | 3 | 3:
        pass
    case 4 | 5 | 6 if anything(1) and anything('Something'):
        pass
    case 7 if anything(2) and anything():
        pass
    case 9 | 10 if asd == 8:
        pass

match asd:
    case 3 | 4 if (number == 1 or number == 2) and anything():
        pass
    case 6 if number == 5 and anything():
        pass

if something():
    print("asd")
elif something_else():
    print(2323)
elif number == 1 or number == 2:
    print("asd")


match something:
    case True | False:
        pass
    case True | False:
        pass

if something is not None or something is True:
    pass
elif something is not False:
    pass

if something is not True:
    pass
elif something is False:
    pass
