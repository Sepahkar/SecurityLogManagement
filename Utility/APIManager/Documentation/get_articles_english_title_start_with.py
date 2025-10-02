import requests

from Utility import configs


def v1(start_with: str):
    """

    :param start_with:
    :return:
    """
    url = configs.GET_ARTICLES_ENGLISH_TITLE_START_WITH("MAIN_SERVER",
                                                        pattern=start_with)

    req = requests.get(url)
    if req.status_code == 200:
        return req.json()
    return []
