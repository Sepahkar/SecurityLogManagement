import requests
from Utility import configs
from shared_lib import core as slcore


def v1(doc_id: int, app_code: str) -> dict:
    # 1. Call Portal API to hide DocumentFlows
    url = f"http://{configs.servers['MAIN_SERVER']}:{configs.Port.PORTAL}/Cartable/api/v1/document-flows/{doc_id}/finish/failed/"

    payload = {"app_doc_id": doc_id}
    headers = {
        "Service-Authorization": slcore.generate_token("v.bagheri"),
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    portal_result = response.json()



    return {
        "msg": "success",
        "portal_result": portal_result
    }
