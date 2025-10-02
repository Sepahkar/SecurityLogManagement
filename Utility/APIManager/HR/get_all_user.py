"""**Returns all Users' information**.
*Be aware that it is not the full user data,
and it does not contain info such as Phone Number, UserTeamRole, ... .*

For get full information check out :py:mod:`get_user_full_info`

"""
import requests
from shared_lib import core as slcore


def v1() -> list[dict]:
    """
    .. warning::

        Used in test purposes, it doesn't call API

    It just returns **simple static list of dictionary**
    that contains a few user simple data.

    For see an example check out the source code.

    :return: Users' data
    :rtype: list[dict]
    """
    return [{'username' : 'B.Ghasemi',
             'fullname' : 'بهاره قاسمی',
             'firstname': 'بهاره',
             'lastname' : 'قاسمی',
             'gender'   : False,
             'photo_url': 'http://192.168.20.81:23000/media_hr/HR/PersonalPhoto/B.Ghasemi.JPG'},
            {'username' : 'E.rezaee',
             'fullname' : 'عرفان رضایی',
             'firstname': 'عرفان',
             'lastname' : 'رضایی',
             'gender'   : False,
             'photo_url': 'http://192.168.20.81:23000/media_hr/HR/PersonalPhoto/E.rezaee.JPG'},
            {'username' : 'M.mozaffari',
             'fullname' : 'محبوبه مضفری',
             'firstname': 'محبوبه',
             'lastname' : 'مضفری',
             'gender'   : True,
             'photo_url': 'http://192.168.20.81:23000/media_hr/HR/PersonalPhoto/M.mozaffari.JPG'},
            {'username' : 'M.moghaddami',
             'fullname' : 'مهسا مقدمی',
             'firstname': 'مهسا',
             'lastname' : 'مقدمی',
             'gender'   : False,
             'photo_url': 'http://192.168.20.81:23000/media_hr/HR/PersonalPhoto/M.moghaddami.JPG'},
            {'username' : 'M.morsali',
             'fullname' : 'مریم مرسلی',
             'firstname': 'مریم',
             'lastname' : 'مرسلی',
             'gender'   : True,
             'photo_url': 'http://192.168.20.81:23000/media_hr/HR/PersonalPhoto/M.morsali.JPG'},
            {'username' : 'E.taeidi',
             'fullname' : 'الهام تاییدی',
             'firstname': 'الهام',
             'lastname' : 'تاییدی',
             'gender'   : True,
             'photo_url': 'http://192.168.20.81:23000/media_hr/HR/PersonalPhoto/E.taeidi.JPG'},
            {'username' : 'B.zangeneh',
             'fullname' : 'بهنوش زنگنه',
             'firstname': 'بهنوش',
             'lastname' : 'زنگنه',
             'gender'   : False,
             'photo_url': 'http://192.168.20.81:23000/media_hr/HR/PersonalPhoto/B.zangeneh.JPG'},
            {'username' : 'M.sepahkar',
             'fullname' : 'محمد سپه کار',
             'firstname': 'محمد',
             'lastname' : 'سپه کار',
             'gender'   : True,
             'photo_url': 'http://192.168.20.81:23000/media_hr/HR/PersonalPhoto/m.sepahkar.JPG'},
            {'username' : 'Z.alizadeh',
             'fullname' : 'زهرا علیزاده',
             'firstname': 'زهرا',
             'lastname' : 'علیزاده',
             'gender'   : True,
             'photo_url': 'http://192.168.20.81:23000/media_hr/HR/PersonalPhoto/Z.alizadeh.JPG'},

            ]


# todo
# firsname, lastname,fullname,  photo_url
# new api (/HR/api/v2/) must be defined 
# filter active user must be defined


def v2() -> list[dict]:
    """Return all users' information. *Using the HR API v1*.

    :param: Nothing
    :return: All users' data. *It's not user full information*
    :rtype: list of dict
    """
    url = 'http://192.168.20.81:14000/HR/api/v1/users/'

    # TEST server
    # url = 'http://192.168.20.52:14000/HR/api/v1/users/'
    all_users = requests.get(url, headers={"Service-Authorization":slcore.generate_token("e.rezaee")})
    return all_users.json()


def v3() -> list[dict]:
    """Return all users' **Minimal** information.
    It's 6-7 seconds quicker than older version ,
    and have less information.
    *Using the HR API v1*.

    :param: Nothing
    :return: UserName, FullName, StaticPhotoURL
    :rtype: list of dict
    """
    url = 'http://192.168.20.81:14000/HR/api/v1/users-minimal-info/'

    # TEST server
    # url = 'http://192.168.20.52:14000/HR/api/v1/users-minimal-info/'
    all_users = requests.get(url, headers={"Service-Authorization":slcore.generate_token("e.rezaee")})
    return all_users.json()
