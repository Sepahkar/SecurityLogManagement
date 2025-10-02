import requests

from Utility import Helper
from Utility import configs


def v1(title, article_type_id, creator, content, english_title=None, summary=None):
    """mainly usage for docgen app"""

    creator = Helper.FixUsername(creator, need_eit=True).username
    payload = {
        "Title"          : title,
        "EnglishTitle"   : english_title,
        "Summary"        : summary,
        "ArticleType"    : article_type_id,
        "CreatorUserName": creator,
        "Content"        : content
    }

    url = configs.INSERT_ARTICLE("MAIN_SERVER")

    req = requests.post(url, data=payload)
    return req.json()
