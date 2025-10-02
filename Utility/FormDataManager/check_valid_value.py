from . import is_not_empty, get_numeric_value


def ver1(request, variable_name, value_list, numeric_value=None, numeric_operator=None):
    """

                this function check if a variable exists in request and if it has valid value
                request must send as: request. POST or request. GET
                if variable is string and may in some value value_list is something like: ['A','B','C',...]
                otherwise if variable is numeric operator may be one of this value
                g : grater than
                ge :greater or equal to
                e : equal to
                l : less than
                le : less or equal to
                numeric_value is value that we want to compare
                for example if we want to check if this variable is grater than zero
                then we must call function with this parameter:
                numeric_value = 0 numeric_operator = 'g'
    """

    # check if variable exists
    if variable_name not in request:
        return False

    # get value of variable and check if it is not None
    value = request.get(variable_name)
    if not is_not_empty.ver1(value):
        return False

    # check if variable in list
    if len(value_list) > 0 and request.get(variable_name) not in value_list:
        return False

    if numeric_value:
        value = get_numeric_value.ver1(request.get(variable_name))
        if numeric_operator == 'g' and value <= numeric_value:
            return False
        elif numeric_operator == 'ge' and value < numeric_value:
            return False
        elif numeric_operator == 'l' and value >= numeric_value:
            return False
        elif numeric_operator == 'le' and value > numeric_value:
            return False
        elif numeric_operator == 'e' and value != numeric_value:
            return False

    return True
