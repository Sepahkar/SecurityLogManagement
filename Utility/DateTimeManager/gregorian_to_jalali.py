"""This module is used for converting Gregorian To Jalali date.

Using :py:mod:`convert_en_number_to_fa` and ``jdatetime`` python library as dependency
"""
import jdatetime
from . import convert_en_number_to_fa as e2f


def v1(date: str) -> str:
    spliter = "/"
    if str(date).__contains__("-"):
        spliter = "-"

    arr = [int(x) for x in str(date).split("-")]  # "1401-08-03" --> [1401,8,3] (str--> int list)
    jdate = jdatetime.GregorianToJalali(arr[0], arr[1], arr[2])

    ja_year = e2f.v1(jdate.jyear.__str__())
    ja_month = e2f.v1(jdate.jmonth.__str__())
    ja_day = e2f.v1(jdate.jday.__str__())

    return ja_year + '-' + ja_month + '-' + ja_day
