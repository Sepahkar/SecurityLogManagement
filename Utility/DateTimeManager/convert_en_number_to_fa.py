"""This module used for **converting English format number to Farsi**
"""


def v1(number: str) -> str:
    intab = '12345678901234567890'
    outtab = '۱۲۳۴۵۶۷۸۹۰١٢٣٤٥٦٧٨٩٠'
    translation_table = str.maketrans(intab, outtab)
    output_text = number.translate(translation_table)
    return output_text
