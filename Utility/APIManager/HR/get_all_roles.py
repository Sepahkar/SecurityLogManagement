"""
Using for returning all roles
"""
import requests
from shared_lib import core as slcore


def v1() -> list[dict]:
    """Returns all Roles. *Using the HR API v1*.
    returns a list of dictionary that contains:

    {
        "RoleId": 45,
        "RoleName": "ادمين ديتابيس",
        "HasLevel": true,
        "HasSuperior": false
    }

    :param: Nothing
    :return: All Roles.
    :rtype: list of dict
    """
    # the HR API v1 is not published yet so use
    # the one that is running on erfan's server

    # main server
    url = 'http://192.168.20.81:14000/HR/api/v1/roles/'

    # TEST server
    # url = 'http://192.168.20.52:14000/HR/api/v1/roles/'

    all_roles = requests.get(url, headers={"Service-Authorization":slcore.generate_token("e.rezaee")})
    if all_roles.status_code == 200:
        return all_roles.json()
    return [{"message": "error"}]


