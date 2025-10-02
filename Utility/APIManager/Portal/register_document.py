def v1(
    app_doc_id: int,
    priority: str,
    doc_state: str,
    document_title: str,
    app_code: str,
    owner: str,
) -> dict:

    return {
        "msg": "success",
        "data": {
            "id": 51449,  # <-- you need this (as document id )
            "AppDocId": 55842,
            "Priority": priority,
            "DocState": doc_state,
            "DocumentTitle": document_title,
            "AppCode": app_code,
            "DocumentOwner": owner,
        },
    }


def v2(
    app_doc_id: int,
    priority: str,
    doc_state: str,
    document_title: str,
    app_code: str,
    owner_nationalcode: str
) -> dict:
    """using NationalCode"""

    return {
        "msg": "success",
        "data": {
            "id": 51449,  # <-- you need this (as document id )
            "AppDocId": 55842,
            "Priority": priority,
            "DocState": doc_state,
            "DocumentTitle": document_title,
            "AppCode": app_code,
            "DocumentOwnerNationalCode": owner_nationalcode
        },
    }
