

def v1(username: str="m.sepahkar@eit") -> dict:
    """*Using the HR API v1*

    :param username: Username
    :type username: str
    :return: simple user information
    :rtype: dict
    """

    return {
        "UserName": "m.sepahkar@eit",
        "FirstName": "محمد",
        "LastName": "سپه کار",
        "FullName": "محمد سپه کار",
        "FirstNameEnglish": "Mohammad",
        "LastNameEnglish": "sepahkar",
        "BirthDate": "1999-08-05",
        "ContractDate": "2018-02-20",
        "ContractEndDate": "2023-05-22",
        "About": None,
        "Gender": True,
        "NumberOfChildren": 0,
        "NationalCode": "1111111111",
        "FatherName": "عبود",
        "IdentityNumber": "11111",
        "IdentityRegisterDate": "1982-04-22",
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
    }
    

def v1(user_national_code: str="1111111111") -> dict:
    return v1()
