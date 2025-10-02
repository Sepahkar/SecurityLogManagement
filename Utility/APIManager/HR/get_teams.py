"""This module is used for **getting teams' information**
"""
import requests
from shared_lib import core as slcore

def v1(active_in_service: bool = True, active_in_evaluation: bool = True) -> list[dict]:
    """Return a static json for testing purposes

        .. warning::

            Use it in test purposes, it doesn't call API

    :param active_in_service:
    :type active_in_service: bool
    :param active_in_evaluation:
    :type active_in_evaluation: bool
    :return: Teams’ data
    :rtype: list[dict]
    """
    if active_in_service and active_in_evaluation:
        return [{
            "TeamCode": "CAR",
            "TeamName": "خودرو",
            "ActiveInService": 1,
            "ActiveInEvaluation": 1,
            "TeamLogo": "static/EIT/images/TeamIcon/CAR.png",

        }, {
            "TeamCode": "COM",
            "TeamName": "مشتركات ",
            "ActiveInService": 1,
            "ActiveInEvaluation": 1,
            "TeamLogo": "static/EIT/images/TeamIcon/COM.png",

        }, {
            "TeamCode": "ENG",
            "TeamName": "مهندسي و خاص",
            "ActiveInService": 1,
            "ActiveInEvaluation": 1,
            "TeamLogo": "static/EIT/images/TeamIcon/ENG.png",

        }, {
            "TeamCode": "FIN",
            "TeamName": "مالي",
            "ActiveInService": 1,
            "ActiveInEvaluation": 1,
            "TeamLogo": "static/EIT/images/TeamIcon/FIN.png",

        }, {
            "TeamCode": "LIF",
            "TeamName": "عمر",
            "ActiveInService": 1,
            "ActiveInEvaluation": 1,
            "TeamLogo": "static/EIT/images/TeamIcon/CAR.png",

        }, {
            "TeamCode": "MED",
            "TeamName": "درمان",
            "ActiveInService": 1,
            "ActiveInEvaluation": 1,
            "TeamLogo": "static/EIT/images/TeamIcon/MED.png",

        }, {
            "TeamCode": "PMA",
            "TeamName": "مديريت پروژه",
            "ActiveInService": 1,
            "ActiveInEvaluation": 1,
            "TeamLogo": "static/EIT/images/TeamIcon/PMA.png",

        }, {
            "TeamCode": "RES",
            "TeamName": "مسئوليت",
            "ActiveInService": 1,
            "ActiveInEvaluation": 1,
            "TeamLogo": "static/EIT/images/TeamIcon/RES.png",

        }, {
            "TeamCode": "RIN",
            "TeamName": "اتکايي",
            "ActiveInService": 1,
            "ActiveInEvaluation": 1,
            "TeamLogo": "static/EIT/images/TeamIcon/RIN.png",

        },
            {
                "TeamCode": "TOL",
                "TeamName": "Tools",
                "ActiveInService": 1,
                "ActiveInEvaluation": 1,
                "TeamLogo": "static/EIT/images/TeamIcon/CAR.png",

            }, {
                "TeamCode": "WEB",
                "TeamName": "وب",
                "ActiveInService": 1,
                "ActiveInEvaluation": 1,
                "TeamLogo": "static/EIT/images/TeamIcon/WEB.png",

            }]
    if not active_in_service and not active_in_evaluation:
        return [{
            "TeamCode": "ACM",
            "TeamName": " امور مشتريان",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/ACM.png",

        }, {
            "TeamCode": "CCO",
            "TeamName": "معاونت توسعه و ارتباط با مشتريان",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/CCO.png",

        }, {
            "TeamCode": "DOA",
            "TeamName": "معاونت عمليات",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/DOA.png",

        }, {
            "TeamCode": "DOC",
            "TeamName": "مستندسازي",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/DOC.png",

        }, {
            "TeamCode": "EVA",
            "TeamName": "ارزيابي",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/EVA.png",

        }, {
            "TeamCode": "FIA",
            "TeamName": "معاونت اداري ومالي",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/FIA.png",

        }, {
            "TeamCode": "ITT",
            "TeamName": "IT",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/ITT.png",

        }, {
            "TeamCode": "KAR",
            "TeamName": "کارانگر",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/ITT.png",

        }, {
            "TeamCode": "MAN",
            "TeamName": "مديريت",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/CAR.png",

        }, {
            "TeamCode": "MIS",
            "TeamName": "مديريت سامانه هاي ستادي",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/MIS.png",

        }, {
            "TeamCode": "OFF",
            "TeamName": "اداري",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/OFF.png",

        }, {
            "TeamCode": "PDE",
            "TeamName": "معاونت پروژه",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/PDE.png",

        }, {
            "TeamCode": "PMO",
            "TeamName": "PMO",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/PMO.png",

        }, {
            "TeamCode": "POD",
            "TeamName": "معاونت محصول",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/POD.png",

        }, {
            "TeamCode": "PRO",
            "TeamName": "آزمايشگاه نرم افزار",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/PRO.png",

        }, {
            "TeamCode": "RAD",
            "TeamName": "تحقيق و توسعه",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/RAD.png",

        }, {
            "TeamCode": "SEL",
            "TeamName": "فروش و امور قراردادها",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/SEL.png",

        }, {
            "TeamCode": "SUP",
            "TeamName": "مديريت پشتيباني",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/SUP.png",

        }, {
            "TeamCode": "TEA",
            "TeamName": "معاونت فني",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/TEA.png",

        }, {
            "TeamCode": "TES",
            "TeamName": "مديريت تست",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/TES.png",

        }, {
            "TeamCode": "VER",
            "TeamName": "نسخه",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/VER.png",

        }, {
            "TeamCode": "PRE",
            "TeamName": "ارتباطات و برندينگ",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/PRE.png",

        }, {
            "TeamCode": "EDU",
            "TeamName": "جذب و آموزش",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/EDU.png",

        }, {
            "TeamCode": "CRM",
            "TeamName": " تحقيقات و برنامه ريزي ",
            "ActiveInService": 0,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/CRM.png",

        }, ]
    if active_in_service and not active_in_evaluation:
        return [{
            "TeamCode": "ADM",
            "TeamName": "Admin",
            "ActiveInService": 1,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/ADM.png",

        }, {
            "TeamCode": "BIN",
            "TeamName": "BI",
            "ActiveInService": 1,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/BIN.png",

        }, {
            "TeamCode": "FIR",
            "TeamName": "آتش‌سوزي",
            "ActiveInService": 1,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/FIR.png",

        }, {
            "TeamCode": "GEN",
            "TeamName": "کليات",
            "ActiveInService": 1,
            "ActiveInEvaluation": 0,
            "TeamLogo": "static/EIT/images/TeamIcon/GEN.png",

        }, ]

    return None


def v2(active_in_service: bool = True, active_in_evaluation: bool = True) -> list[dict]:
    """*Using HR API v1*

    :param active_in_service: Is active in book service ?
    :type active_in_service: bool
    :param active_in_evaluation: Is active in evaluation ?
    :type active_in_evaluation: bool
    :return: Teams' data
    :rtype: list[dict]
    """
    url = 'http://192.168.20.81:14000/HR/api/v1/teams/'

    # TEST server
    # url = 'http://192.168.20.52:14000/HR/api/v1/teams/'

    # use this payload as parameters for API call
    payload = {
        "ActiveInService": active_in_service,
        "active_in_evaluation": active_in_evaluation,
    }
    all_filtered_teams = requests.get(url, params=payload, headers={"Service-Authorization":slcore.generate_token("e.rezaee")})
    return all_filtered_teams.json()
