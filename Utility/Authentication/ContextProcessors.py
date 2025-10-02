import traceback

from .Utils import V1_find_token_from_request,V1_jwt_dec,V1_is_not_expired

def tokeninfo(request):
    context_extras = {}
    token = V1_find_token_from_request(request)
    if token:
        data_enc = V1_jwt_dec(token)
        if data_enc and V1_is_not_expired(data_enc.get('exp', None)):
            for key,value in data_enc.items():
                try:
                    new_key = "cnt_"+key
                    context_extras.update({
                        new_key:value
                    })
                except:
                    traceback.print_exc()

    return context_extras

