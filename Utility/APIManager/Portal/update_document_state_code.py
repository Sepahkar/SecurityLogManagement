import requests
from Utility import configs
from shared_lib import core as slcore

def v1(doc_id: int, app_code: str, new_state: str) -> dict:
    """
    Update the state code of a document in Portal by AppDocId.
    """
    url = f"http://{configs.servers['MAIN_SERVER']}:{configs.Port.PORTAL}/Cartable/api/v1/update-document-state/"
    payload = {
        "app_doc_id": doc_id,
        "app_code": app_code,
        "new_state": new_state
    }
    headers = {
        "Service-Authorization": slcore.generate_token("e.rezaee"),
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
