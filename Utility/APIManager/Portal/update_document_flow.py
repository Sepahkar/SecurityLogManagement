"""**Updating DocumentFlow** instances' field
"""
import requests

from Utility import configs
from shared_lib import core as slcore

def v1(doc_flow_id: int, doc_flow_fields: dict) -> int:
    """ *Using Portal API v1*

    :param doc_flow_id: DocumentFlow Id
    :type doc_flow_id: int
    :param doc_flow_fields: A dictionary of DocumentFlow fields that you want to update
    :type doc_flow_fields: dict
    :return: Updated DocumentFlow data
    :rtype: dict
    """
    url = configs.PUT_DOCUMENT_FLOW("MAIN_SERVER")
    doc_flow_fields['id'] = doc_flow_id
    r = requests.put(url, doc_flow_fields, headers={"Service-Authorization":slcore.generate_token("e.rezaee")})
    return r.json()
