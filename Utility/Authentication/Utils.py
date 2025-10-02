
from functools import wraps

from .Helper import *


def V1_PermissionControl(function):
    @wraps(function)
    def wrap(request,*args,**kwargs):
        return function(request,*args,**kwargs)
    return wrap

