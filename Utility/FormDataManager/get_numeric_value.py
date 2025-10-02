from . import is_not_empty


def ver1(value, value_type="int"):
    if not is_not_empty.ver1(value):
        return 0
    else:
        if type(value) == str and value.strip().isnumeric():
            if value_type == "float":
                return float(value)
            else:
                return int(value)
