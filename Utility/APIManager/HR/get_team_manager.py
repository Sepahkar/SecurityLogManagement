def v1(team_code: str) -> str:
    """Returns the sample static data"""
    # erfan_team = {
    #     'ACC',
    #     'ACM',
    #     'ADM',
    #     'BIN',
    #     'CAR',
    #     'CCO',
    #     'COM',
    #     'CRM',
    #     'DOA',
    #     'DOC',
    #     'EDU',
    #     'ENG',
    #     'EVA',
    #     'FIA',
    #     'FIN',
    #     'FIR',
    #     'GEN',
    #     'ITT',
    #     'KAR',
    #     'LIF',
    #     'MAN',
    # }

    zahra_team = {
        'MED',
        'MIS',
        'OFF',
        'PDE',
        'PMA',
        'PMO',
        'POD',
        'PRE',
        'PRO',
        'RAD',
        'RES',
        'RIN',
        'SEL',
        'SUP',
        'TEA',
        'TES',
        'TOL',
        'VER',
        'WEB',
    }

    # if team_code in zahra_team:
    #     return 'z.alizadeh@eit'
    raise Exception("DO NOT USE THIS")
    return 'm.sepahkar@eit'




def v2(teamcode: str="MIS", ManagerType="GeneralManager") -> str:
    data = {
        "TeamCode": "MIS",
        "TeamName": "مديريت سامانه هاي ستادي",
        "ActiveInService": False,
        "ActiveInEvaluation": False,
        "IsActive": True,
        "GeneralManager": "m.sepahkar@eit",
        "SupportManager": None,
        "TestManager": None
    } 
    
    return data[ManagerType]


def v3(teamcode: str="MIS", ManagerType="GeneralManager") -> str:
    data = {
        "TeamCode": "MIS",
        "TeamName": "مديريت سامانه هاي ستادي",
        "ActiveInService": False,
        "ActiveInEvaluation": False,
        "IsActive": True,
        "GeneralManager": "m.sepahkar@eit",
        "GeneralManagerNationalCode": "1111111111",
        "SupportManager": None,
        "SupportManagerNationalCode": None,
        "TestManager": None,
        "TestManagerNationalCode": None
    } 
    
    return data[ManagerType]


