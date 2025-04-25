from django import template

register = template.Library()

@register.filter
def split(value, arg):
    parts = value.split(arg)
    if len(parts) == 0:
        return value  # اگر هیچ قسمتی وجود نداشت، مقدار اصلی را برمی‌گرداند
    return parts[0]  # به طور پیش‌فرض اولین قسمت را برمی‌گرداند

@register.filter
def split_and_return(value, arg):
    arg_parts = arg.split(',')
    separator = arg_parts[0]
    return_type = arg_parts[1]

    parts = value.split(separator)
    if return_type == 'first':
        return parts[0] if len(parts) > 0 else value
    elif return_type == 'last':
        return parts[-1] if len(parts) > 0 else value
    return value  # اگر return_type نامعتبر باشد، مقدار اصلی را برمی‌گرداند

@register.filter
def replace_none_with_zero(value):
    return value if value is not None else 0
