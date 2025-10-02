"""This module is used for converting Jalali To Gregorian date.

Using :py:mod:`convert_fa_number_to_en` and ``jdatetime`` python library as dependency
"""

import jdatetime
from . import convert_fa_number_to_en as f2e


def ver1(date: str) -> str:
    """
    .. note::

       You can pass ۱۴۰۱/۰۸/۱۳, ۱۴۰۱-۰۸-۱۳, 1401/08/13 or 1401-08-13 as input.
       They are all the same


    :param date: Persian date *No matter in Farsi or English number format,
     with ``/`` or ``-`` seperator*
    :type date: str
    :return: Gregorian date *in English number format*
    :rtype: str
    """
    spliter = "/"
    if str(date).__contains__("-"):
        spliter = "-"
    arr = str(date).split(spliter)
    y = int(f2e.v1(arr[0]))
    m = int(f2e.v1(arr[1]))
    d = int(f2e.v1(arr[2]))
    date = jdatetime.JalaliToGregorian(y, m, d)
    gdate = date.gyear.__str__() + "-" + date.gmonth.__str__() + "-" + date.gday.__str__()
    return gdate  # jdatetime.datetime(date.gyear,date.gmonth,date.gday).date()
