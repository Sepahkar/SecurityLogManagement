import requests
from shared_lib import core as slcore
# def ver1(doc_id:int, inbox_owner_national_code:str, sender_national_code:str=None)->dict:
#         """
#         این تابع برای خارج کردن یک مدرک از کارتابل است.
#         در صورتی که شناسه کد ملی فرد ارسال کننده نیز ارسال شده باشد، فقط رکوردی از کارتابل خارج می شود
#         که فرستنده و گیرنده با پارامترها منطبق باشند
#         در صورتی که فرستنده مقدار نداشته باشد، کلیه رکوردهای موجود در کارتابل فرد دریافت کننده از کارتابل وی خارج می شود.

#         Args:
#             doc_id (int): شناسه مدرک
#             inbox_owner_national_code (str): کد ملی فردی که مدرک باید از کارتابل وی خارج شود
#             sender_national_code (str): کد ملی فردارسال کننده مدرک، در صورت نال بودن این مقدار، کلیه رکوردهایی که گیرنده با پارامتر مربوطه است، از کارتابل خارج می شود

#         Returns:
#             dict : یک دیکشنری مشابه زیر است:
#                 {'success':True, 'message':'با موفقیت از کارتابل خارج شد'}
#         """
#         return {'success':True, 'message':'با موفقیت از کارتابل خارج شد'}
def ver1(
    doc_id: int,
    inbox_owner_national_code: str,
    sender_national_code: str = None
) -> dict:
    """
    Removes document from user's cartable.

    If sender_national_code is provided:
        Only matching sender+receiver record is removed.
    If sender_national_code is None:
        All visible records for receiver are removed.
    """

    url = "http://eit-app:23000/Cartable/api/v1/exit-document-flow/"

    headers = {
        "Service-Authorization": slcore.generate_token("bpms"),
        "Content-Type": "application/json",
    }

    payload = {
        "DocumentId": doc_id,
        "InboxOwnerNationalCode": inbox_owner_national_code,
    }

    if sender_national_code:
        payload["SenderUserNationalCode"] = sender_national_code

    response = requests.put(url, json=payload, headers=headers)

    try:
        response_data = response.json()
    except Exception:
        response_data = {
            "msg": "invalid response",
            "status_code": response.status_code,
        }

    return {
        "success": response.status_code == 200,
        "response": response_data,
    }
