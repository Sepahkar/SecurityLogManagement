"""This module is using for **begin the process of sending document
to others' cartable**

"""
import requests

from Utility import configs
from shared_lib import core as slcore

def ver1(doc_id: int, sender: str, inbox_owners: list[str]) -> dict:
    """ *Using Portal API v1*

    :param doc_id: Document Id
    :type doc_id: int
    :param sender: From *It must be Username(with @eit format)*
    :type sender: str
    :param inbox_owners: To *It must be Username(with @eit format)*
    :type inbox_owners: list[str]
    :return: Dictionary that contains DocumentFlow data if it created properly, Otherwise it contains validations error messages
    :rtype: dict
    """

    url = 'http://192.168.20.81:23000/Cartable/api/create-document-flow2/'
    # url = configs.PUT_DOCUMENT_FLOW("MAIN_SERVER")
    receive_status = {}
    for receiver in inbox_owners:
        json_data = {
            "DocumentId": doc_id,
            "InboxOwner": receiver,
            "SenderUser": sender
        }
        r = requests.put(url, json=json_data, headers={"Service-Authorization":slcore.generate_token("bpms"), "Content-Type":"application/json"})
        receive_status[receiver] = r.json()
    return receive_status

# todo response payload must be implemented


# def ver2(doc_id: int, sender_nationalcode: str, inbox_owners_nationalcode: list[str], flow_step:str, new_doc_state:str, exit_from_cartable:bool) -> dict:
#     """
#     این تابع یک سند را ارسال می کند

#     Args:
#         doc_id (int): شناسه مدرک در پورتال
#         sender (str): فرد ارسال کننده
#         inbox_owners (list[dict]): لیستی از افرادی که باید برای آنها ارسال شود
#                                 [{'national_code':'1234567890', 'role_id':25, 'team_code':'CAR'}, ...]
#         flow_step (str): مشخص می شود که این ارسال برای چه مرحله ای است
#         new_doc_state (str):وضعیت فرم را به روزرسانی می کنیم 
#         exit_from_cartable (bool): در صورتی که این مقدار صحیح باشد، رکورد قبلی که مربوط به این فرد بوده است را پیدا می کنیم و از کارتابل وی خارج می کنیم

#     Returns:
#         dict: مقدار بازگشتی شبیه به این است
#         {'success':True, 'message':''}
#     """
    
#     return {'success':True, 'message':''}

def ver2(
    doc_id: int,
    sender_nationalcode: str,
    inbox_owners_nationalcode: list,
    flow_step: str,
    new_doc_state: str,
    exit_from_cartable: bool,
) -> dict:

    url = "http://eit-app:23000/Cartable/api/v3/document-flows/"

    headers = {
        "Service-Authorization": slcore.generate_token("bpms"),
        "Content-Type": "application/json",
    }

    results = {}
    overall_success = True

    for receiver in inbox_owners_nationalcode:

        # support dict or string
        if isinstance(receiver, dict):
            receiver_key = receiver.get("national_code")  # hashable
            inbox_owner = receiver_key
        else:
            receiver_key = receiver
            inbox_owner = receiver

        payload = {
            "DocumentId": doc_id,
            "InboxOwnerNationalCode": inbox_owner,
            "SenderUserNationalCode": sender_nationalcode,
            "FlowStep": flow_step,
            "NewDocState": new_doc_state,
            "ExitFromCartable": exit_from_cartable,
        }

        response = requests.put(url, json=payload, headers=headers)

        try:
            response_data = response.json()
        except Exception:
            response_data = {
                "msg": "invalid response",
                "status_code": response.status_code,
                "raw": response.text,
            }

        if response.status_code != 200:
            overall_success = False

        results[receiver_key] = response_data

    return {
        "success": overall_success,
        "results": results,
    }
