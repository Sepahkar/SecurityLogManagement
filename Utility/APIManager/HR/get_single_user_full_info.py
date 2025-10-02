def v1(username: str="m.sepahkar@eit") -> dict:
    """*Using HR API v1*

    :param username: Username, *no matter it has @eit or not,
                     FixUsername will be fix it.*
    :type username: str
    :return: User's Full information
    :rtype: dict
    """
    return {
        "UserName": "m.sepahkar@eit",
        "FirstName": "محمد",
        "LastName": "سپه کار",
        "FullName": "محمد سپه کار",
        "FirstNameEnglish": "Mohammad",
        "LastNameEnglish": "sepahkar",
        "BirthDate": "1924-08-12",
        "ContractDate": "2018-02-20",
        "ContractEndDate": "2023-05-22",
        "About": None,
        "Gender": True,
        "NumberOfChildren": 0,
        "NationalCode": "1111111111",
        "FatherName": "عبود",
        "IdentityNumber": "11111",
        "IdentityRegisterDate": "2005-04-22",
        "InsuranceNumber": "11111111",
        "CVFile": None,
        "BirthCity_id": 50,
        "Religion_id": 81,
        "DegreeType_id": 56,
        "LivingAddress_id": None,
        "MarriageStatus_id": 60,
        "MilitaryStatus_id": 40,
        "UserStatus_id": 94,
        "ContractType_id": 92,
        "Degree_TypeTitle": "دکترا",
        "found_in_educational_history": True,
        "Marriage_StatusTitle": "متاهل",
        "Military_StatusTitle": "انجام شده",
        "UserStatusTitle": "شاغل",
        "ContractTypeTitle": "مشاوره",
        "BirthCityTitle": "اصفهان",
        "IdentityCityTitle": "اصفهان",
        "ReligionTitle": "اسلام",
        "PhotoURL": "static/HR/images/personnel/m.sepahkar.jpg",
        "StaticPhotoURL": "http://192.168.20.81:14000/media/HR/PersonalPhoto/m.sepahkar.jpg",
        "all_phone_number": [
            {
                "id": 108,
                "TelNumber": 11111,
                "Title": "تلفن همراه",
                "IsDefault": False,
                "Person_id": "m.sepahkar@eit",
                "Province_id": None,
                "TelType_id": 65,
                "TelTypeTitle": "تلفن همراه"
            },
            {
                "id": 374,
                "TelNumber": 2222,
                "Title": "تلفن محل سکونت",
                "IsDefault": False,
                "Person_id": "m.sepahkar@eit",
                "Province_id": 8,
                "TelType_id": 66,
                "ProvinceTitle": "تهران",
                "TelTypeTitle": "منزل"
            }
        ],
        "all_team_role": [
            {
                "id": 3449,
                "Superior": False,
                "StartDate": "1396/12/01",
                "EndDate": None,
                "LevelId_id": None,
                "ManagerUserName_id": "m.khakvar@eit",
                "RoleId": 121,
                "TeamCode": "EVA",
                "UserName": "m.sepahkar@eit",
                "RoleTitle": "مديرتيم ارزيابي",
                "TeamName": "ارزيابي",
                "all_employee": []
            },
            {
                "id": 3642,
                "Superior": False,
                "StartDate": "1400/08/08",
                "EndDate": None,
                "LevelId_id": None,
                "ManagerUserName_id": "m.khakvar@eit",
                "RoleId": 132,
                "TeamCode": "MIS",
                "UserName": "m.sepahkar@eit",
                "RoleTitle": "مدير سامانه هاي ستادي",
                "TeamName": "مديريت سامانه هاي ستادي",
                "all_employee": [
                    
                    {
                        "UserName": "E.Rezaee@eit",
                        "FirstName": "عرفان",
                        "LastName": "رضائي",
                        "FullName": "عرفان رضائي",
                        "FirstNameEnglish": "Erfan",
                        "LastNameEnglish": "Rezaee",
                        "BirthDate": "2006-04-12",
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
                        "UserStatus_id": 95,
                        "ContractType_id": 91,
                        "LivingAddressText": "تهران ",
                        "Degree_TypeTitle": "دیپلم",
                        "found_in_educational_history": False,
                        "Marriage_StatusTitle": "مجرد",
                        "Military_StatusTitle": "معافیت کفالت",
                        "UserStatusTitle": "ترک کار",
                        "ContractTypeTitle": "پاره وقت",
                        "BirthCityTitle": "تهران",
                        "IdentityCityTitle": "تهران",
                        "ReligionTitle": "اسلام",
                        "PhotoURL": "static/HR/images/personnel/E.Rezaee.jpg",
                        "StaticPhotoURL": "http://192.168.20.81:14000/media/HR/PersonalPhoto/E.Rezaee.jpg",
                        "all_phone_number": [
                            {
                                "id": 646,
                                "TelNumber": 1111111,
                                "Title": "منزل",
                                "IsDefault": False,
                                "Person_id": "E.Rezaee@eit",
                                "Province_id": None,
                                "TelType_id": 66,
                                "TelTypeTitle": "منزل"
                            },
                            {
                                "id": 647,
                                "TelNumber": 111111111,
                                "Title": "تلفن همراه",
                                "IsDefault": False,
                                "Person_id": "E.Rezaee@eit",
                                "Province_id": None,
                                "TelType_id": 65,
                                "TelTypeTitle": "تلفن همراه"
                            },
                            {
                                "id": 2258,
                                "TelNumber": 111111,
                                "Title": "ضروری",
                                "IsDefault": False,
                                "Person_id": "E.Rezaee@eit",
                                "Province_id": None,
                                "TelType_id": 65,
                                "TelTypeTitle": "تلفن همراه"
                            }
                        ],
                        "all_team_role": [
                            {
                                "id": 3719,
                                "Superior": False,
                                "StartDate": "1401/06/06",
                                "EndDate": None,
                                "LevelId_id": None,
                                "ManagerUserName_id": "m.sepahkar@eit",
                                "RoleId": 135,
                                "TeamCode": "MIS",
                                "UserName": "E.Rezaee@eit",
                                "RoleTitle": "مستندساز ",
                                "TeamName": "مديريت سامانه هاي ستادي",
                                "all_employee": []
                            },
                            {
                                "id": 3866,
                                "Superior": False,
                                "StartDate": "1402/01/01",
                                "EndDate": None,
                                "LevelId_id": 5,
                                "ManagerUserName_id": "m.sepahkar@eit",
                                "RoleId": 63,
                                "TeamCode": "MIS",
                                "UserName": "E.Rezaee@eit",
                                "LevelTitle": "Junior+",
                                "RoleTitle": "برنامه نويس",
                                "TeamName": "مديريت سامانه هاي ستادي",
                                "all_employee": []
                            }
                        ],
                        "corresponding_degree_info": {}
                    },
                    
                    
                    
                ]
            }
        ],
        "corresponding_degree_info": [
            {
                "id": 384,
                "StartDate": None,
                "EndDate": None,
                "StartYear": 1352,
                "EndYear": 1400,
                "IsStudent": False,
                "GPA": "19.99",
                "Degree_Type_id": 56,
                "EducationTendency_id": 1,
                "Person_id": "m.sepahkar@eit",
                "University_id": None,
                "DegreeTitle": "دکترا",
                "TendencyTitle": "نرم افزار",
                "PersonFullName": "محمد سپه کار"
            }
        ]
    }


def v2(user_national_code: str="1111111111") -> dict:
    return v1()