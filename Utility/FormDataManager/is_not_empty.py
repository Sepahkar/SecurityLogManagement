def ver1(variable):
    if variable is None or variable == '' or \
            ((type(variable) == int or type(variable) == float) and variable == 0):
        return False
    return True
