""" This module is used for **Creating a Document Instance**

"""
import json

import requests

from Utility import configs

from shared_lib import core as slcore
def _normalize(value):
    """
    Ensures value is JSON serializable.
    Converts Django model instances to string representation.
    """
    # Django model instance
    if hasattr(value, "_meta"):
        # Prefer Code attribute if exists (ConstValue case)
        if hasattr(value, "Code"):
            return value.Code
        return str(value)

    return value

def v1(app_doc_id: int, priority: str, doc_state: str, document_title: str, app_code: str, owner: str) -> dict:
    """*Using Portal API v1*

    :param app_doc_id: App Doc Id
    :type app_doc_id: int
    :param priority: Priority, *Like Normal, Urgent*
    :type priority: str
    :param doc_state: Document State, *Like Not send yet, Not read yet, Read, Finished*
    :type doc_state: str
    :param document_title: Document Title
    :type document_title: str
    :param app_code: App Code
    :type app_code: str
    :return: Dictionary that contains Document Id if it created properly, Otherwise it contains validations error message
    :rtype: dict
    """
    # todo app_doc_id need more docs
    # todo app_code need more docs

    url = 'http://192.168.20.81:23000/Cartable/api/create-document2/'
    # url = configs.PUT_DOCUMENT("MAIN_SERVER")

    json_data = {
        "AppDocId": app_doc_id,
        "Priority": priority,
        "DocState": doc_state,
        "DocumentTitle": document_title,
        "AppCode": app_code,
        "DocumentOwner": owner,
    }
    r = requests.put(url, json_data, headers={"Service-Authorization":slcore.generate_token("bpms")})
    if r.status_code == 200:
        return r.json()
    return r.json()


def ver2(    app_doc_id: int,
    priority,
    doc_state,
    document_title: str,
    app_code: str,
    owner_nationalcode: str,
) -> dict:
    """
    Using Portal API v2
    Ensures safe JSON serialization before sending.
    """

    url = "http://eit-app:23000/Cartable/api/v2/documents/"

    # Normalize potentially unsafe values
    priority = _normalize(priority)
    doc_state = _normalize(doc_state)

    json_data = {
        "AppDocId": app_doc_id,
        "Priority": priority,
        "DocState": doc_state,
        "DocumentTitle": document_title,
        "AppCode": app_code,
        "DocumentOwnerNationalCode": owner_nationalcode,
    }

    headers = {
        "Service-Authorization": slcore.generate_token("bpms"),
        "Content-Type": "application/json",
    }

    try:
        response = requests.put(url, json=json_data, headers=headers)
    except Exception as e:
        return {
            "success": False,
            "error": f"Request failed before reaching portal: {str(e)}",
        }

    try:
        portal_response = response.json()  # <--- Must call .json() first
        # portal returns {"msg":"success", "data":{...}}
        document_id = portal_response.get("data", {}).get("id", -1)
        return {"success": True, "doc_id": document_id, "portal_response": portal_response}

    except Exception:
        return {
            "success": False,
            "status_code": response.status_code,
            "raw_response": response.text,
        }


# def v2():
# todo add response doc
# response = {
#     "document_id": None,
#     "message": "messageclass",
#     "error_code": "875",
# }
# pass

# def ver2(app_doc_id: int, priority: str, doc_state: str, document_title: str, app_code: str, owner_nationalcode: str) -> dict:
    
#     url = 'http://192.168.20.81:23000/Cartable/api/create-document2/'
#     # url = configs.PUT_DOCUMENT("MAIN_SERVER")
#     owner_Username = "m.sepahkar"
#     json_data = {
#         "AppDocId": app_doc_id,
#         "Priority": priority,
#         "DocState": doc_state,
#         "DocumentTitle": document_title,
#         "AppCode": app_code,
#         "DocumentOwner": owner_Username,
#     }
#     r = requests.put(url, json_data, headers={"Service-Authorization":slcore.generate_token("bpms")})
#     doc_id = r.doc_id
#     if r.status_code == 200:
#         return {'success':True, 'doc_id': doc_id, 'message':'با موفقیت ثبت شد'}
#     return {'success':False, 'doc_id': doc_id, 'message':'با موفقیت ثبت شد'}
