"""docstring"""
# todo docstring
import requests
from Utility import Helper
from shared_lib import core as slcore

def v1(username: str) -> dict:
    """*Using HR API v1*

    :param username: Username, *no matter it has @eit or not,
                     FixUsername will be fix it.*
    :type username: str
    :return: User's Full information
    :rtype: dict
    """

    # handling @eit in the end of usernames
    username = Helper.FixUsername(username, need_eit=True).username

    url = 'http://192.168.20.81:14000/HR/api/v1/users/full-info/'+ username

    # TEST server
    # url = 'http://192.168.20.52:14000/HR/api/v1/users/full-info/' + username

    user_full_info = requests.get(url, headers={"Service-Authorization":slcore.generate_token("e.rezaee")})
    if user_full_info.status_code == 200:
        # user_full_info.json() returns a list with only one dict,
        # we need to return a dict so, here we used .pop() method
        return user_full_info.json().pop()
    return {}
