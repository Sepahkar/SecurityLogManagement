
# list variable is something like ['1,2,3']
# we must convert it into [1,2,3]
def ver1(variable):
    if len(variable) > 0:
        # ['1,2,3'] --> '1,2,3'
        variable = variable[0]
        variable = variable.split(',')
    return variable

    # list variable is something like ['1,2,3']
    # we must convert it into [1,2,3]


def ver2(variable, is_int=True):
    if variable:
        # '1,2,3' --> ['1','2','3']
        variable = variable.split(',')
        # if array elements must be integer we cast it to int
        if is_int:
            int_variable = []
            for v in variable:
                int_variable.append(int(v))
            variable = int_variable
    return variable
