from Utility.Authentication.Helper import (
    V1_find_token_from_request,
    V1_get_data_from_token,
    V1_show_html_page,
    V1_get_all_users,
)
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.middleware.csrf import get_token
import os
from pathlib import Path
from django.http import HttpResponse
from django.shortcuts import redirect
import urllib.parse


def init_login(request):
    username = None
    url = "/admin/login/"
    if "next" in request.GET:
        url = request.GET.get('next')

    if request.user.is_authenticated:
        username = str(request.user.username).lower()

    token = V1_find_token_from_request(request)
    if token:
        username = V1_get_data_from_token(token, 'username')
        username = str(username).lower() if username else username

    elif not token:
        if "next" in request.GET:
            next_url = urllib.parse.unquote(request.GET.get('next'))
            if "token=" in next_url:
                token = next_url.split("token=")[1]
                username = V1_get_data_from_token(token, 'username')
                username = str(username).lower() if username else username

    if username:
        user = User.objects.filter(username=username).first()
        if user:
            login(request, user)
    else:
        url = "/admin/login/"
        url = f"{url}?next={request.GET.get('next', '')}" if "next" in request.GET else url
    return redirect(url)


def create_user(request):
    access_this = False
    if request.user.is_authenticated:
        if request.user.is_superuser:
            access_this = True

    token = V1_find_token_from_request(request)
    if token:
        username = V1_get_data_from_token(token, 'username')
        if username:
            username = str(username).lower()
            user = User.objects.filter(username=username).first()
            if user and user.is_superuser:
                login(request, user)
                access_this = True

    if access_this:
        message = ''
        if request.method == "POST":
            selected_user = request.POST.get('selected_user')
            if selected_user:
                if User.objects.filter(username=str(selected_user).lower()).exists():
                    msg_str = 'این کاربر قبلا در سیستم ثبت شده است'
                else:
                    User.objects.create(
                        username=selected_user,
                        password=0,
                        first_name='',
                        last_name='',
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        email=selected_user.replace("@eit","@iraneit.com")
                    )
                    msg_str = 'کاربر با موفقیت اضافه شد.'
            else:
                msg_str = 'لطفا یک کابر انتخاب کنید'

            message = f'''<p class="alert" id="alert">{msg_str}</p>'''

        if "do" in request.GET and "username" in request.GET:
            msg_str = ''
            username = request.GET.get('username')
            if request.user.is_superuser:
                if username:
                    username = str(username).lower()
                    user = User.objects.filter(username=username).first()
                    if user:
                        if request.GET.get('do') == "deleteuser":
                            user.delete()
                            msg_str = 'کاربر مورد نظر با موفقیت حذف شد'
                        elif request.GET.get('do') == "setsuperuser":
                            if user.is_superuser is False:
                                user.is_superuser = True
                                user.save()
                                msg_str = 'فعال شدن ارشد با موفقیت انجام شد'
                        elif request.GET.get('do') == "unsetsuperuser":
                            if user.is_superuser is True:
                                user.is_superuser = False
                                user.save()
                                msg_str = 'غیرفعال شدن ارشد موفقیت انجام شد'
                        elif request.GET.get('do') == "deactive":
                            if user.is_active is True:
                                user.is_active = False
                                user.save()
                                msg_str = 'غیرفعال شدن کاربر با موفقیت انجام شد'
                        elif request.GET.get('do') == "active":
                            if user.is_active is False:
                                user.is_active = True
                                user.save()
                                msg_str = 'فعال شدن کاربر موفقیت انجام شد'
                    else:
                        msg_str = 'کاربری با این مشخصات وجود ندارد'
                else:
                    msg_str = 'کاربری انتخاب نشده است'
            else:
                msg_str = 'شما مجوز لازم را ندارید'
            message = f'''<p class="alert" id="alert">{msg_str}</p>''' if msg_str else ''
            request.session['custom_message'] = message
            return redirect(request.path)

        if "custom_message" in request.session and request.session["custom_message"]:
            message = request.session["custom_message"]
            request.session["custom_message"] = ''


        all_users_info = V1_get_all_users()
        all_users_info_list = [v for l,v in all_users_info.items()]
        qs_exists_users = User.objects.all()
        exists_users = []
        exists_users_list = []
        for item in qs_exists_users.values("username","is_active","is_superuser"):
            item.update({'username':str(item.get('username')).lower()})
            exists_users.append(item)
            exists_users_list.append(str(item.get('username')).lower())

        csrf_token = get_token(request)
        tag_csrf_token = f'<input name="csrfmiddlewaretoken" value={csrf_token} type="hidden" />'
        html_path = os.path.join(Path(__file__).resolve().parent, 'templates/create_user.html')
        with open(html_path, 'r', encoding="utf8") as f:
            html = f.read()
        tag_select_all_users = f""
        for item in all_users_info_list:
            if item.get('UserName') not in exists_users_list:
                tag_select_all_users += f'<option value="{item.get("UserName")}">{item.get("FullName")}</option>'
        tag_tr_exists_users = ""
        for item in exists_users:
            active_deactive = '<a href="'+request.path+'?do=deactive&username='+item.get('username')+'" class="link_button">غیر فعال کردن کاربر</a>' if item.get('is_active') else '<a href="'+request.path+'?do=active&username='+item.get('username')+'" class="link_button">فعال کردن کاربر</a>'
            superusernosuperuser = '<a href="'+request.path+'?do=unsetsuperuser&username='+item.get('username')+'" class="link_button">غیر فعال شدن ارشد</a>' if item.get('is_superuser') else '<a href="'+request.path+'?do=setsuperuser&username='+item.get('username')+'" class="link_button">ارشد شدن کاربر</a>'
            deleteuser = '<b  data-href="'+request.path+'?do=deleteuser&username='+item.get('username')+'" class="link_button" onclick="deleteUser(this)">حذف کاربر</b>'
            tag_tr_exists_users += f'''
            <tr>
                <td>{item.get("username")}</td>
                <td>{all_users_info.get(item.get("username"),{}).get('FullName','')}</td>
                <td>{"<b style='color:green;'>فعال</b>" if item.get("is_active") else "<span class='sp-deactive'>غیرفعال</span>"}</td>                
                <td>{"<b style='color:green;'>بله</b>" if item.get("is_superuser") else "<span class='sp-deactive'>خیر</span>"}</td>    
                <td>
                    <div class="parent_link_button">
                    {active_deactive}     
                    {superusernosuperuser}
                    {deleteuser}              
                    </div>                    
                </td>            
            </tr>
            '''



        html = html.replace("{{tag_select_all_users}}",tag_select_all_users)
        html = html.replace("{{tag_tr_exists_users}}",tag_tr_exists_users)
        html = html.replace("{{tag_csrf_token}}",tag_csrf_token)
        html = html.replace("{{message}}",message)
        return HttpResponse(html)

    return V1_show_html_page('not_access_admin')