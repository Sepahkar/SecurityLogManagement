import json
from functools import wraps

import requests

from .Helper import *
from django.http.response import HttpResponseRedirect,HttpResponse
from django.core.exceptions import PermissionDenied
from shared_lib import core as slcore


def V1_PermissionControl(function):
    @wraps(function)
    def wrap(request,*args,**kwargs):
        if "first_token" in request.GET:
            first_token = request.GET.get('first_token')
            user, user_ip = V1_get_username_ip_from_first_token(first_token)
            if user and user_ip and user_ip == V1_get_client_ip(request):
                # host = request.scheme + "://" + str(request.get_host()).split(":")[0]
                host = os.getenv('ACCESSCONTROL_ADDRESS_IP_PORT')
                api_url = f'{host}AccessControl/api/GenerateToken/'
                try:
                    response = requests.post(api_url,data=json.dumps({'first_token':first_token}),headers={'Content-Type':'application/json', "Service-Authorization":slcore.generate_token("e.rezaee")})
                    if response.json().get('data').get('state') == "ok":
                        token = response.json().get('data').get('token')
                        url = request.scheme + "://" + request.get_host() + request.get_full_path()
                        url = V1_update_url_params(url=url,params={'token':token},list_remove=['first_token'])
                        return HttpResponseRedirect(redirect_to=url)
                except:
                    print("access control server is down")
                    return V1_show_html_page('service_not_available')

            return V1_show_html_page('403')

        token = V1_find_token_from_request(request)
        if token:
            show_403,need_new_token = V1_is_valid_token(request,token)
            if show_403 is False and need_new_token:
                # refresh current page for get new token
                url = request.scheme + "://" + request.get_host() + request.get_full_path()
                url = V1_update_url_params(url=url, list_remove=['token','first_token'])
                return HttpResponseRedirect(redirect_to=url)
            elif show_403 is False and need_new_token is False:
                access_current_url = V1_check_access_current_url(request,token)
                if access_current_url:
                    return function(request,*args,**kwargs)
                return V1_show_html_page('not_access_page')

            return V1_show_html_page('403')

        next_url = request.scheme + "://" + request.get_host() + request.get_full_path()
        # url = request.scheme + "://eit-app:5000/Auth/"
        url = os.getenv('GATEWAY_AUTH_URL')
        url = V1_update_url_params(url, params={'next':next_url},list_remove=['first_token','token'])
        return HttpResponseRedirect(redirect_to=url)
    return wrap







