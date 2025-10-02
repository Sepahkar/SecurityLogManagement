"""docstring"""
import requests
from Utility import Helper
from shared_lib import core as slcore


def v1(users: list) -> list[dict]:
    """*Using the HR API v1*

    :param users: Usernames
    :type users: list
    :return: Users data
    :rtype: list[dict]
    """
    # handling @eit in the end of usernames
    for index, user in enumerate(users):
        users[index] = Helper.FixUsername(user, need_eit=True).username

    # example: ['jassem', 'qassem'] --> 'jassem,qassem'
    usernames = ','.join([str(username) for username in users])

    url = 'http://192.168.20.81:14000/HR/api/v1/users/'+ usernames

    # TEST server
    # url = 'http://192.168.20.52:14000/HR/api/v1/users/' + usernames

    all_users_info = requests.get(url, headers={"Service-Authorization":slcore.generate_token("e.rezaee")})
    return all_users_info.json()
