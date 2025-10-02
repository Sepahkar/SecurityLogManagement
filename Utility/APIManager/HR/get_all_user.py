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
    raise Exception("DO NOT USE")
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


def v2() -> list[dict]:
    raise Exception("DO NOT USE")


def v3() -> list[dict]:
    """Return all users' **Minimal** information.
    It's 6-7 seconds quicker than older version ,
    and have less information.
    *Using the HR API v1*.

    :param: Nothing
    :return: UserName, FullName, StaticPhotoURL
    :rtype: list of dict
    """
    return [
        {
        "UserName": "m.sepahkar@eit",
        "FullName": "محمد سپه کار",
        "StaticPhotoURL": "http://192.168.20.81:14000/media/HR/PersonalPhoto/m.sepahkar.jpg"
        },
        {
        "UserName": "E.Rezaee@eit",
        "FullName": "عرفان رضائي",
        "StaticPhotoURL": "http://192.168.20.81:14000/media/HR/PersonalPhoto/E.Rezaee.jpg"
        },
]
