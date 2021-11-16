
def to_number(value : str):
    num = 0
    if value:
        if '.' in value:
            try:
                num = float(value)
            except:
                print('Unable to convert %s}' % value)
        else:
            try:
                num = int(value)
            except:
                print('Unable to convert %s}' % value)
    return num
