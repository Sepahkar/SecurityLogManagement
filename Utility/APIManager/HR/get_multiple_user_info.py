def v1(users: list=["m.sepahkar", "e.rezaee"]) -> list[dict]:
    """*Using the HR API v1*

    :param users: Usernames
    :type users: list
    :return: Users data
    :rtype: list[dict]
    """
    return [
    {
        "UserName": "m.sepahkar@eit",
        "FirstName": "محمد",
        "LastName": "سپه کار",
        "FullName": "محمد سپه کار",
        "FirstNameEnglish": "Mohammad",
        "LastNameEnglish": "sepahkar",
        "BirthDate": "2010-04-13",
        "ContractDate": "2018-02-20",
        "ContractEndDate": "2023-05-22",
        "About": None,
        "Gender": True,
        "NumberOfChildren": 0,
        "NationalCode": "1111111111",
        "FatherName": "عبود",
        "IdentityNumber": "11111",
        "IdentityRegisterDate": "2011-04-22",
        "InsuranceNumber": "11111111",
        "CVFile": None,
        "BirthCity_id": 50,
        "Religion_id": 81,
        "DegreeType_id": 56,
        "LivingAddress_id": None,
        "MarriageStatus_id": 60,
        "MilitaryStatus_id": 40,
        "ContractType_id": 92,
        "UserStatus_id": 94,
        "Degree_TypeTitle": "دکترا",
        "Marriage_StatusTitle": "متاهل",
        "Military_StatusTitle": "انجام شده",
        "UserStatusTitle": "شاغل",
        "ContractTypeTitle": "مشاوره",
        "BirthCityTitle": "اصفهان",
        "IdentityCityTitle": "اصفهان",
        "ReligionTitle": "اسلام",
        "PhotoURL": "static/HR/images/personnel/m.sepahkar.jpg",
        "StaticPhotoURL": "http://192.168.20.81:14000/media/HR/PersonalPhoto/m.sepahkar.jpg"
    },
    {
        "UserName": "E.Rezaee@eit",
        "FirstName": "عرفان",
        "LastName": "رضائي",
        "FullName": "عرفان رضائي",
        "FirstNameEnglish": "Erfan",
        "LastNameEnglish": "Rezaee",
        "BirthDate": "2006-08-15",
        "ContractDate": "2022-08-23",
        "ContractEndDate": "2023-05-22",
        "About": "    ",
        "Gender": True,
        "NumberOfChildren": 0,
        "NationalCode": "2222222222",
        "FatherName": "رستم",
        "IdentityNumber": "2222222222",
        "IdentityRegisterDate": None,
        "InsuranceNumber": None,
        "CVFile": "/media/E.Rezaee.pdf",
        "BirthCity_id": 103,
        "Religion_id": 81,
        "DegreeType_id": 52,
        "LivingAddress_id": 323,
        "MarriageStatus_id": 59,
        "MilitaryStatus_id": 77,
        "ContractType_id": 91,
        "UserStatus_id": 95,
        "LivingAddressText": "تهران",
        "Degree_TypeTitle": "دیپلم",
        "Marriage_StatusTitle": "مجرد",
        "Military_StatusTitle": "معافیت کفالت",
        "UserStatusTitle": "ترک کار",
        "ContractTypeTitle": "پاره وقت",
        "BirthCityTitle": "تهران",
        "IdentityCityTitle": "تهران",
        "ReligionTitle": "اسلام",
        "PhotoURL": "static/HR/images/personnel/E.Rezaee.jpg",
        "StaticPhotoURL": "http://192.168.20.81:14000/media/HR/PersonalPhoto/E.Rezaee.jpg"
    }
]

def v2(users_national_code: list=["2222222222", "1111111111"]) -> list[dict]:
    return v1()