def ver1(
    doc_id: int,
    sender: str = "e.rezaee@eit",
    inbox_owners: list[str] = ["m.sepahkar@eit", "a.ahmadi@eit"],
) -> dict:

    # for each inbox owner (aka receiver) we have a username key in return dict
    return {
        "m.sepahkar@eit": {
            "msg": "success",
            "data": {
                "id": 67083,
                "ReceiveDate": "2025-01-29T11:54:34.845225+03:30",
                "IsRead": False,
                "SendDate": None,
                "InboxOwner": "m.sepahkar@eit",
                "SenderUser": "e.rezaee@eit",
                "DueDate": None,
                "PersonalDueDate": None,
                "IsVisible": True,
                "ReadDate": None,
                "TeamCode": None,
                "RoleId": None,
                "WorkFlowStep": None,
                "DocumentId": 51449,
                "PreviousFlow": None,
            },
        }
    }


def ver2(
    doc_id: int,
    sender_national_code: str = "1111111111",
    inbox_owners_national_code: list[str] = ["2222222222","3333333333"],
) -> dict:

    # for each inbox owner (aka receiver) we have a natioanlcode key in return dict
    return {
        "2222222222": {
            "msg": "success",
            "data": {
                "id": 67083,
                "ReceiveDate": "2025-01-29T11:54:34.845225+03:30",
                "IsRead": False,
                "SendDate": None,
                "InboxOwner": "m.sepahkar@eit",
                "SenderUser": "e.rezaee@eit",
                "InboxOwnerNationalCode": "2222222222",
                "SenderUserNationalCode": "1111111111",
                "DueDate": None,
                "PersonalDueDate": None,
                "IsVisible": True,
                "ReadDate": None,
                "TeamCode": None,
                "RoleId": None,
                "WorkFlowStep": None,
                "DocumentId": 51449,
                "PreviousFlow": None,
            },
        },
        "3333333333": {
            "msg": "success",
            "data": {
                "id": 67084,
                "ReceiveDate": "2025-01-29T11:54:34.845225+03:30",
                "IsRead": False,
                "SendDate": None,
                "InboxOwner": "j.abus@eit",
                "SenderUser": "e.rezaee@eit",
                "InboxOwnerNationalCode": "3333333333",
                "SenderUserNationalCode": "1111111111",
                "DueDate": None,
                "PersonalDueDate": None,
                "IsVisible": True,
                "ReadDate": None,
                "TeamCode": None,
                "RoleId": None,
                "WorkFlowStep": None,
                "DocumentId": 51449,
                "PreviousFlow": None,
            },
        },
    }