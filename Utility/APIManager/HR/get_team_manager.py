"""This module is used for **getting the team manager information**"""
import requests

from Utility import configs
from shared_lib import core as slcore

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
    return 'm.sepahkar@eit'




def v2(teamcode: str, ManagerType) -> str:
    url = configs.TEAMS("MAIN_SERVER") + teamcode
    r = requests.get(url, headers={"Service-Authorization":slcore.generate_token("e.rezaee")})
    if r.status_code == 200:
        
        # its safe to use zero index,  because the teamcode is unique 
        # and always the list length is 1
        return r.json()[0][ManagerType]
    return None

