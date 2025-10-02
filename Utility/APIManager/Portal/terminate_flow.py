import requests
from Utility import configs
from shared_lib import core as slcore
from ConfigurationChangeRequest.models import ConfigurationChangeRequest

def v1(doc_id: int, app_code: str) -> dict:
    # 1. Call Portal API to hide DocumentFlows
    url = "http://127.0.0.1:8001/Cartable/api/v1/hide-document-flows/"
    # url = f"http://{configs.servers['MAIN_SERVER']}:{configs.Port.PORTAL}/Cartable/api/v1/hide-document-flows/"
    payload = {"app_doc_id": doc_id}
    headers = {
        "Service-Authorization": slcore.generate_token("e.rezaee"),
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    portal_result = response.json()

    # 2. Update local ConfigurationChangeRequest status to FAILED
    ConfigurationChangeRequest.objects.filter(doc_id=doc_id).update(status_code='FAILED')

    return {
        "msg": "success",
        "portal_result": portal_result
    }
