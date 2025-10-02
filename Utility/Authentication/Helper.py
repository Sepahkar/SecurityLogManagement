import json
import requests
import datetime
import jwt
import os
from dotenv import load_dotenv
from pathlib import Path
import pytz
from urllib.parse import parse_qsl,urlencode,urlparse,urlunparse
from django.http.response import HttpResponse
from django.core.cache import cache
import traceback
from django.contrib.auth.models import User
import socket
from shared_lib import core as slcore

load_dotenv(os.path.join(Path(__file__).resolve().parent,".env"))


def V1_get_user_from_iis(request):
    AUTH_USER = request.META.get('AUTH_USER')
    LOGON_USER = request.META.get('LOGON_USER')
    REMOTE_USER = request.META.get('REMOTE_USER')
    if AUTH_USER != '' and AUTH_USER == LOGON_USER and AUTH_USER == REMOTE_USER:
        user = str(AUTH_USER).replace("EIT\\", "")
        user = user + "@eit" if "@eit" not in user else user
        user = user.lower()
        return user


def V1_init_all_data(request, user, user_ip):
    username = user
    # host = request.scheme + "://" + str(request.get_host()).split(":")[0]
    host = os.getenv('ACCESSCONTROL_ADDRESS_IP_PORT')
    url = f'{host}AccessControl/api/get-all-apps-info/?return-dict=1'
    try:
        res = requests.get(url, headers={"Service-Authorization":slcore.generate_token("e.rezaee")})
        all_apps_info = res.json().get("data")
        if all_apps_info:
            user_data = {
                "username": username,
                "user_ip": user_ip,
            }
            # call api from app HR
            if 'HR' in all_apps_info:
                hr_full_url = all_apps_info.get('HR').get('FullUrl')
                # urls
                user_url = f'{hr_full_url}api/get-user/{username}/'
                user_team_role_url = f'{hr_full_url}api/get-user-team-role/{username}/'
                # end
                # requests
                user_res = requests.get(user_url, headers={"Service-Authorization":slcore.generate_token("e.rezaee")})
                user_team_role_res = requests.get(user_team_role_url, headers={"Service-Authorization":slcore.generate_token("e.rezaee")})
                # end
                # init data from response
                user_info = user_res.json().get('data')
                user_team_role_info = user_team_role_res.json().get('data')
                # end

                for k,v in user_info.items():
                    user_data.update({f'user_{k}':v})
                user_data.update({
                    'team_role_info':user_team_role_info,
                })

            if "AccessControl" in all_apps_info:
                access_control_full_url = all_apps_info.get('AccessControl').get('FullUrl')
                # urls
                user_access_urls_url = f'{access_control_full_url}api/get-user-all-urls/{username}/'
                # end
                # requests
                user_access_urls_res = requests.get(user_access_urls_url, headers={"Service-Authorization":slcore.generate_token("e.rezaee")})
                # end
                # init data from response
                user_access_urls = user_access_urls_res.json().get('data')
                user_data.update({
                    'user_access_urls': [item.get('URL') for item in user_access_urls.get('rows')],
                })
        return user_data
    except:
        return None


def V1_jwt_enc(payload):
    encoded = jwt.encode(payload=payload, key=os.getenv('JWT_AUTHENTICATE_SECRET_KEY'), algorithm="HS256")
    return str(encoded)


def V1_jwt_dec(encrypted):
    try:
        if type(encrypted) is str:
            encrypted = str(encrypted).encode("utf-8")
        data = jwt.decode(encrypted, os.getenv('JWT_AUTHENTICATE_SECRET_KEY'), algorithms=["HS256"])
        return data
    except:
        return None


def V1_is_valid_info(data_enc, user_ip):
    user_ip_token = data_enc.get('user_ip')
    if user_ip and user_ip_token and user_ip == user_ip_token:
        return True
    return False


def V1_is_not_expired(exp_datetime):
    if exp_datetime is not None:
        now = V1_datetime_to_int(datetime.datetime.now(tz=pytz.timezone('Asia/Tehran')))
        ret = False
        if exp_datetime >= now:
            ret = True
        return ret
    return False


def V1_is_valid_token(request,token):
    data_enc = V1_jwt_dec(token)
    need_new_token = True
    show_403 = True
    if data_enc:
        if "username" in data_enc and "exp" in data_enc and "user_ip" in data_enc:
            if V1_is_valid_info(data_enc, V1_get_client_ip(request)):
                if V1_is_not_expired(data_enc.get('exp',None)):
                    need_new_token = False
                    show_403 = False
                else:
                    need_new_token = True
                    show_403 = False
    return show_403,need_new_token


def V1_get_username_is_valid_token(token, user_ip):
    data_enc = V1_jwt_dec(token)
    username = None
    if data_enc:
        if "username" in data_enc and "exp" in data_enc and "user_ip" in data_enc:
            if V1_is_valid_info(data_enc, user_ip):
                if V1_is_not_expired(data_enc.get('exp',None)):
                    username = data_enc.get('username')
    return username


def V1_datetime_to_int(datetime):
    return int(round(datetime.timestamp() * 1000))


def V1_generate_token(request, user, user_ip):
    data = V1_init_all_data(request,user,user_ip)
    data.update({
        "exp": V1_datetime_to_int(datetime.datetime.now(tz=pytz.timezone('Asia/Tehran')) + datetime.timedelta(hours=24))
    })
    token = V1_jwt_enc(data)
    return token


def V1_generate_first_token(request):
    username = V1_get_user_from_iis(request)
    if username:
        data = {
            "username": username,
            "user_ip": V1_get_client_ip(request),
            "exp": V1_datetime_to_int(datetime.datetime.now(tz=pytz.timezone('Asia/Tehran')) + datetime.timedelta(minutes=1))
        }
        first_token = V1_jwt_enc(data)
        return first_token


def V1_get_username_ip_from_first_token(first_token):
    enc_data = V1_jwt_dec(first_token)
    user = None
    user_ip = None
    if "username" in enc_data and "user_ip" in enc_data and "exp" in enc_data:
        if V1_is_not_expired(enc_data.get('exp')):
            user = str(enc_data.get('username')).replace("EIT\\", "")
            user = user + "@eit" if "@eit" not in user else user
            user = user.lower()
            user_ip = enc_data.get('user_ip')
    return user, user_ip


def V1_check_token(request):
    #need_new_token = True
    new_token = ''
    show_403 = True
    token = request.GET.get("token",None)
    if token is None and V1_get_user_from_iis(request):
        new_token = V1_generate_token(request)
        show_403 = False
    if token is not None:
        show_403,need_new_token = V1_is_valid_token(request,token)
        if need_new_token and show_403 is False:
            new_token = V1_generate_token(request)
        elif need_new_token is False and show_403 is False:
            new_token = token
    return new_token,show_403


def V1_check_access_current_url(request,token):
    ret = False
    JWT = token
    URL = request.scheme + "://" + request.get_host() + request.get_full_path()
    # host = request.scheme + "://" + str(request.get_host()).split(":")[0]
    host = os.getenv('ACCESSCONTROL_ADDRESS_IP_PORT')
    apps_url = f'{host}AccessControl/api/get-all-apps-info/?return-dict=1'
    try:
        res = requests.get(apps_url, headers={"Service-Authorization":slcore.generate_token("e.rezaee")})
        all_apps_info = res.json().get("data")
        if all_apps_info:
            if 'AccessControl' in all_apps_info:
                ac_full_url = all_apps_info.get('AccessControl').get('FullUrl')
                ac_check_url = ac_full_url + "api/CheckPermittedURL/"
                response = requests.post(ac_check_url,data=json.dumps({'URL':URL,'JWT':JWT,'REQUESTED_IP':V1_get_client_ip(request)}),headers={'content-Type':'application/json', "Service-Authorization":slcore.generate_token("e.rezaee")})
                if response.json().get('data').get('state') == "ok":
                    if response.json().get('data').get('access') is True:
                        ret = True
    except:
        ret = False
    return ret


def V1_get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def V1_update_url_params(url='', params={}, list_remove=[]):
    if url:
        url_parse = urlparse(url)
        query = url_parse.query
        url_dict = dict(parse_qsl(query))
        for item in list_remove:
            if item in url_dict:
                del url_dict[item]
        url_dict.update(params)
        url_new_query = urlencode(url_dict)
        url_parse = url_parse._replace(query=url_new_query)
        new_url = urlunparse(url_parse)
        return new_url
    return url


def V1_get_url_params(url=''):
    if url:
        url_parse = urlparse(url)
        query = url_parse.query
        url_dict = dict(parse_qsl(query))
        return url_dict
    return {}


def V1_show_html_page(page_name):
    html_path = os.path.join(Path(__file__).resolve().parent, f'templates/{page_name}.html')
    with open(html_path, 'r',encoding="utf8") as f:
        html = f.read()
    return HttpResponse(html)


def V1_get_data_from_token(token,key):
    data_enc = V1_jwt_dec(token)
    if data_enc and key:
        if all(k in data_enc for k in [key,"exp"]):
            if V1_is_not_expired(data_enc.get('exp',None)):
                return data_enc.get(key)


def V1_find_token_from_request(request):
    token = None
    if request.GET.get('token',None):
        token = request.GET.get('token')
    if token is None and request.POST.get('token', None):
        token = request.POST.get('token')

    if token is None and hasattr(request,"body"):
        try:
            body_data = json.loads(str(request.body, encoding='utf-8'))
            token = body_data.get('token')
        except:
            print("error at get token in request.body")

    if token is None and hasattr(request, "data"):
        token = request.data.get('token')

    return token


def V1_get_current_host(request):
    host = request.scheme + "://" + str(request.get_host()).split(":")[0]
    return host


def V1_get_host_from_access_control():
    host = os.getenv('ACCESSCONTROL_ADDRESS_IP_PORT')
    host = host.split("://")[0] + "://" + host.split("://")[1].split(":")[0]
    return host


def V1_get_api_fetch_data(url,return_key=None):
    if url in cache:
        data = json.loads(cache.get(url))
        if return_key:
            return data.get(return_key)
        return data
    else:
        try:
            response = requests.get(url, headers={"Service-Authorization":slcore.generate_token("e.rezaee")})
            data = response.json().get('data')
            cache.set(url,json.dumps(data))
            if return_key:
                return data.get(return_key)
            return data
        except:
            traceback.print_exc()


def get_request_handler(_type="get"):
    ret = requests.get
    if _type == "post":
        ret = requests.post
    elif _type == "put":
        ret = requests.put
    elif _type == "delete":
        ret = requests.delete
    elif _type == "patch":
        ret = requests.patch
    elif _type == "head":
        ret = requests.head
    elif _type == "options":
        ret = requests.options

    return ret


def V1_call_api(url, return_key=None, method_type="get", data={}, use_cache=True):
    if use_cache and url in cache:
        data = json.loads(cache.get(url))
        if return_key:
            return data.get(return_key)
        return data
    else:
        try:
            request_handler = get_request_handler(method_type)
            response = request_handler(url=url, data=json.dumps(data), headers={'Content-Type':'application/json', "Service-Authorization":slcore.generate_token("e.rezaee")})
            data = response.json().get('data')
            cache.set(url, json.dumps(data))
            if return_key:
                return data.get(return_key)
            return data
        except:
            print("error at call_api method")


def get_current_server_ip():
    socket.gethostbyname(socket.gethostname())
    ip = socket.gethostbyname(socket.getfqdn())
    return ip


def V1_get_host():
    return f"http://{get_current_server_ip()}"


def V1_get_port(app_name):
    key = "all_app_info"
    try:
        if key in cache:
            data = json.loads(cache.get(key))
        else:
            url = f"{V1_get_host()}:13000/AccessControl/api/get-all-apps-info/?return-dict=1"
            data = V1_call_api(url)
            cache.set(key,json.dumps(data))
    except:
        data = {}
        traceback.print_exc()
    return data.get(app_name,{}).get('APPPORT',0)


def V1_get_host_from_server():
    host = os.getenv('HOST_ON_SERVER')
    return host


def V1_get_port_from_server(app_name):
    key = "all_app_info_from_server"
    try:
        if key in cache:
            data = json.loads(cache.get(key))
        else:
            url = f"{V1_get_host_from_server()}:13000/AccessControl/api/get-all-apps-info/?return-dict=1"
            data = V1_call_api(url)
            cache.set(key,json.dumps(data))
    except:
        data = {}
        traceback.print_exc()
    return data.get(app_name,{}).get('APPPORT',0)


def V1_get_access_control_ip_port():
    host = os.getenv('ACCESSCONTROL_ADDRESS_IP_PORT')
    return host


def V1_get_or_create_auth_user(username):
    username = str(username).lower()
    if "@eit" not in username:
        username += "@eit"
    user = User.objects.filter(username=username).first()
    if user:
        return user
    user = User.objects.create(
        username=username,
        is_active=True,
        is_staff=True,
        password=0,
        email=str(username).replace('@eit','@iraneit.com')
    )
    return user


def V1_get_all_user_team_roles():
    url = f"{V1_get_host_from_server()}:{V1_get_port_from_server('HR')}/HR/api/get-user-team-roles/"
    data = V1_call_api(url=url)
    return data


def V1_get_all_levels():
    return {
        '1':'Senior +',
        '2':'Senior',
        '3':'Middle +',
        '4':'Middle',
        '5':'Junior +',
        '6':'Junior',
    }


def V1_get_all_roles():
    url = f"{V1_get_host_from_server()}:{V1_get_port_from_server('HR')}/HR/api/get-all-roles/?return_dict=1"
    data = V1_get_api_fetch_data(url)
    return data


def V1_get_all_teams():
    url = f"{V1_get_host_from_server()}:{V1_get_port_from_server('HR')}/HR/api/get-all-teams/?return_dict=1"
    data = V1_get_api_fetch_data(url)
    return data


def V1_get_all_users(show_as_list=False):
    url = f"{V1_get_host_from_server()}:{V1_get_port_from_server('HR')}/HR/api/all-users/?return_dict=1"
    data = V1_get_api_fetch_data(url)
    if show_as_list:
        data = [value for key,value in data.items()]
    return data
