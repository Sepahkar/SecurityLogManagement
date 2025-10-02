import requests

from Utility import configs


def v1(article_id, content) -> int:
    """mainly usage for *docgen app*

    :return: status_code
    """

    payload = {
        "id"     : article_id,
        "Content": content
    }

    url = configs.UPDATE_ARTICLE_CONTENT("MAIN_SERVER")

    req = requests.put(url, data=payload)
    return req.status_code
