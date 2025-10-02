""" This module is used for **Creating a Document Instance**

"""
import json

import requests

from Utility import configs

from shared_lib import core as slcore

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

    # url = 'http://192.168.20.81:23000/Cartable/api/create-document2/'
    url = configs.PUT_DOCUMENT("MAIN_SERVER")

    json_data = {
        "AppDocId": app_doc_id,
        "Priority": priority,
        "DocState": doc_state,
        "DocumentTitle": document_title,
        "AppCode": app_code,
        "DocumentOwner": owner,
    }
    r = requests.put(url, json_data, headers={"Service-Authorization":slcore.generate_token("e.rezaee")})
    if r.status_code == 200:
        return r.json()
    return r.json()

# def v2():
# todo add response doc
# response = {
#     "document_id": None,
#     "message": "messageclass",
#     "error_code": "875",
# }
# pass

def v2():
    ...