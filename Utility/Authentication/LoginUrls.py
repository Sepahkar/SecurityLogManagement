from django.urls import path,include,re_path
from Utility.Authentication.AutoLogin import *

urlpatterns = [
    path('', init_login),
    path('createuser/', create_user),
]