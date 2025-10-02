"""**Updating Document** instances' field
"""

import requests

from Utility import configs
from shared_lib import core as slcore

def v1(doc_id: int, doc_fields: dict) -> dict :
    """ *Using Portal API v1*

    :param doc_id: Document Id
    :type doc_id: int
    :param doc_fields: A dictionary of Document fields that you want to update
    :type doc_fields: dict
    :return: Updated Document data
    :rtype: dict
    """
    url = configs.PUT_DOCUMENT("MAIN_SERVER")
    doc_fields['id'] = doc_id
    r = requests.put(url, doc_fields, headers={"Service-Authorization":slcore.generate_token("e.rezaee")})
    return r.json()
