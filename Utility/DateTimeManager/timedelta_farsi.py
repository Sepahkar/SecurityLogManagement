"""This module is used for **getting timedelta** between 2 datetime object
and return a farsi string like دو سال و سه ماه و 12 روز پیش

Using **datetime, python-dateutil** packages.

"""
from datetime import datetime
from dateutil.relativedelta import *


def v1(object_datetime: datetime, full_detail: bool = False) -> str:
    """It's not highly customizable, it just has 2 type return that will be
    specified with full_detail parameter.

    :param object_datetime: datetime
    :type object_datetime: datetime.datetime
    :param full_detail: Need to full details? full details contains year to second (if they are not zero)
    :type full_detail: bool
    :return: farsi timedelta like دو ماه و سه روز
    :rtype: str
    """
    assert isinstance(object_datetime, datetime)
    assert isinstance(full_detail, bool)

    now = datetime.now()
    datetime_diff = relativedelta(now, object_datetime)

    diff_detail = {
        'سال': datetime_diff.years,
        'ماه': datetime_diff.months,
        'روز': datetime_diff.days,
        'ساعت': datetime_diff.hours,
        'دقیقه': datetime_diff.minutes,
        'ثانیه': datetime_diff.seconds,
    }
    if full_detail:
        diff_date_persian = ''
        for key, value in diff_detail.items():
            if value:
                diff_date_persian += f'{value} {key} '
        return diff_date_persian
    else:
        for key, value in diff_detail.items():
            if value:
                return f'{value} {key}'

