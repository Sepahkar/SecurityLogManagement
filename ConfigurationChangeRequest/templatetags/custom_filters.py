from django import template
import jdatetime

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



@register.filter
def startswith(value, arg):
    if value:
        return value.startswith(arg)
    return False

@register.filter
def to_int(value):
    """
    تبدیل مقدار به عدد صحیح
    اگر مقدار خالی یا None باشد، 0 برمی‌گرداند
    """
    if value is None or value == '':
        return 0
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

@register.filter
def to_jalali(value, format_string="%Y/%m/%d"):
    """
    تبدیل تاریخ میلادی به تاریخ شمسی (جلالی)
    
    Args:
        value: تاریخ میلادی (می‌تواند رشته یا datetime باشد)
        format_string: فرمت خروجی تاریخ شمسی (پیش‌فرض: %Y/%m/%d)
    
    Returns:
        str: تاریخ شمسی در فرمت مشخص شده
    """
    if not value:
        return ""
    
    try:
        # اگر مقدار رشته است، ابتدا آن را به datetime تبدیل می‌کنیم
        if isinstance(value, str):
            # فرمت‌های مختلف تاریخ میلادی را پشتیبانی می‌کنیم
            import datetime
            formats = [
                "%Y-%m-%d",
                "%Y/%m/%d", 
                "%Y-%m-%d %H:%M:%S",
                "%Y/%m/%d %H:%M:%S",
                "%d/%m/%Y",
                "%d-%m-%Y"
            ]
            
            gregorian_date = None
            for fmt in formats:
                try:
                    gregorian_date = datetime.datetime.strptime(value, fmt)
                    break
                except ValueError:
                    continue
            
            if not gregorian_date:
                return value  # اگر نتوانستیم تبدیل کنیم، مقدار اصلی را برمی‌گردانیم
        else:
            gregorian_date = value
        
        # تبدیل به تاریخ شمسی
        jalali_date = jdatetime.datetime.fromgregorian(datetime=gregorian_date)
        
        # فرمت کردن تاریخ شمسی
        return jalali_date.strftime(format_string)
        
    except (ValueError, TypeError, AttributeError):
        # در صورت بروز خطا، مقدار اصلی را برمی‌گردانیم
        return str(value)