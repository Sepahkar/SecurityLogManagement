"""This module used for **converting Farsi format number to English**
"""


def v1(number: str) -> str:
    intab = '۱۲۳۴۵۶۷۸۹۰١٢٣٤٥٦٧٨٩٠'
    outtab = '12345678901234567890'
    translation_table = str.maketrans(intab, outtab)
    output_text = number.translate(translation_table)
    return output_text
