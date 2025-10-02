import requests

from Utility import configs


def v1(start_with: str):
    """

    :param start_with:
    :return:
    """
    url = configs.DELETE_ARTICLES("MAIN_SERVER")
    payload = {
        "start_pattern": start_with
    }
    req = requests.post(url, data=payload)
    return req.status_code
