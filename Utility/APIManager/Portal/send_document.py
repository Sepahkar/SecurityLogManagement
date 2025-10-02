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

    # url = 'http://192.168.20.81:23000/Cartable/api/create-document-flow2/'
    url = configs.PUT_DOCUMENT_FLOW("MAIN_SERVER")
    receive_status = {}
    for receiver in inbox_owners:
        json_data = {
            "DocumentId": doc_id,
            "InboxOwner": receiver,
            "SenderUser": sender
        }
        r = requests.put(url, json=json_data, headers={"Service-Authorization":slcore.generate_token("e.rezaee"), "Content-Type":"application/json"})
        receive_status[receiver] = r.json()
    return receive_status

# todo response payload must be implemented


def ver2():
    ...