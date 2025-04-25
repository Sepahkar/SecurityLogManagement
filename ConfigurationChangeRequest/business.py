from . import models as m
import jdatetime
from . import validator
from django.core.exceptions import ValidationError
from datetime import datetime
from Utility.APIManager.Portal.register_document import v2 as register_document
from Utility.APIManager.Portal.send_document import ver2 as send_document
from Utility.APIManager.Portal.update_document_state_code import v1 as update_document_state_code
from Utility.APIManager.Portal.terminate_flow import v1 as terminate_flow
from Utility.APIManager.Portal.finish_flow import v1 as finish_flow
from Config import settings

APP_CODE = settings.APPCODE

def get_user_information(request_id:int, status_code:str)->str:
    user_info = None
    operation_info = None
    team_info = None
    role_info = None
    request_instance = m.ConfigurationChangeRequest.objects.get(id=request_id)
    if status_code == 'TESTER':
        user_info = request_instance.tester_nationalcode
        team_info = request_instance.tester_team_code.team_name
        role_info = request_instance.tester_role_id.role_title
        operation_info = "انجام تست"
    elif status_code == 'MANAGE':
        user_info = request_instance.manager_nationalcode
        operation_info = "بررسی و اعلام نظر"
    elif status_code == 'COMITE':
        user_info = request_instance.committee_user_nationalcode
        operation_info = "اعلام نظر کمیته"
    elif status_code == 'DRAFTD':
        user_info = request_instance.requestor_nationalcode
        team_info = request_instance.requestor_team_code
        role_info = request_instance.requestor_role_id.role_title
        operation_info = "تکمیل اطلاعات فرم"
    elif status_code == 'EXECUT':
        user_info = request_instance.executor_nationalcode
        team_info = request_instance.executor_team_code.team_name
        role_info = request_instance.executor_role_id.role_title
        operation_info = "اجرای تغییرات"

    # در صورتی که برای فردی ارسال شده باشد، مشخصات وی بازگشت داده می شود
    if user_info and operation_info:
        salutation = "آقای" if user_info.gender or user_info.gender is None else "خانم"
        role_info = role_info if role_info is not None else ""
        if team_info:
            return f"{salutation} {user_info.first_name} {user_info.last_name} {role_info} تیم {team_info} جهت {operation_info}"
        else:
            return f"{salutation} {user_info.first_name} {user_info.last_name} {role_info} جهت {operation_info}"
    else:
        return "-1"
# این تابع بررسی می کند که با توجه به وضعیت فعلی سیستم فرم برای این کاربر باید به چه صورتی نمایش داده شود؟
def check_form_status(user_nationalcode: str, request_id: int) -> str:
    # بررسی اعتبار request_id
    if request_id is None:
        return 'INSERT'
    
    try:
        # دریافت درخواست بر اساس request_id
        request_instance = m.ConfigurationChangeRequest.objects.get(id=request_id)
    except m.ConfigurationChangeRequest.DoesNotExist:
        return 'INSERT'
    
    # بررسی وضعیت و تطابق با کاربر جاری
    if (
        (request_instance.status_code == 'DRAFTD' and user_nationalcode == request_instance.requestor_nationalcode.national_code) or
        (request_instance.status_code == 'MANAGE' and user_nationalcode == request_instance.manager_nationalcode.national_code) or
        (request_instance.status_code == 'COMITE' and user_nationalcode == request_instance.committee_user_nationalcode.national_code) or
        (request_instance.status_code == 'EXECUT' and user_nationalcode == request_instance.executor_nationalcode.national_code) or
        (request_instance.status_code == 'TESTER' and user_nationalcode == request_instance.tester_nationalcode.national_code)
    ):
        return 'UPDATE'
    
    # بررسی وضعیت فقط خواندنی
    if user_nationalcode in [
        request_instance.requestor_nationalcode.national_code,
        request_instance.manager_nationalcode.national_code,
        request_instance.committee_user_nationalcode.national_code,
        request_instance.executor_nationalcode.national_code,
        request_instance.tester_nationalcode.national_code
    ]:
        return 'READONLY'
    
    # در غیر این صورت وضعیت نامعتبر
    return 'INVALID'

# این تابع با توجه به مرحله فعلی، به مرحله بعدی می رود
def next_step(request_id: int,user_nationalcode:int ,action: str)->str:
    # دریافت درخواست بر اساس request_id
    request_instance = m.ConfigurationChangeRequest.objects.get(id=request_id)
    
    # ابتدا باید کنترل کنیم که آیا کاربر جاری مجاز به انجام عملیات بر روی فرم هست یا خیر؟
    form_status = check_form_status(user_nationalcode, request_id)
    
    # اگر کاربر جزو کاربران مجاز این درخواست نباشد
    if form_status == 'INVALID':
        return {'success':False,'message':"شما مجوز دسترسی به این درخواست را ندارید"}
    
    # اگر کاربر مجاز باشد ولی در این مرحله امکان انجام عملیات نداشته باشد
    if form_status == 'READONLY':
        return {'success':False,'message':'شما در این مرحله امکان انجام عملیات را ندارید'}
    
    # وضعیت فعلی درخواست
    current_status = request_instance.status_code
    
    # حالا مرحله بعدی را مشخص می کنیم
    # تعیین وضعیت جدید بر اساس action
    if action == "CON":
        if current_status == 'EXECUT' and not request_instance.test_required:
            new_status = 'FINISH'
        elif current_status == 'MANAGE' and not request_instance.need_committee:
            new_status = 'EXECUT'
        else:
            new_status = get_next_status(current_status)
    elif action == "RET":
        new_status = get_previous_status(current_status)
    elif action == "REJ":
        new_status = 'FAILED'
    else:
        return {'success':False, 'message':'نوع عملیات درخواستی معتبر نمی باشد'}

    # با توجه به وضعیت فعلی اطلاعات کاربر مربوطه را به دست می آوریم
    if new_status not in ('FAILED','FINISH' ):
        user_info = get_user_information(request_id, new_status)
        if user_info == '-1':
            return {'success':False,'message':'امکان تعیین کاربر بعدی جهت ارسال وجود ندارد'}

    # به‌روزرسانی وضعیت درخواست
    request_instance.status_code = new_status
    request_instance.save()
    
    
    # به‌روزرسانی فیلدهای opinion و date بر اساس نقش و action
    current_date = jdatetime.datetime.now()
    current_time = current_date.strftime('%H:%M')
    
    if current_status == 'MANAGE':
        request_instance.manager_opinion = (action == 'CON')
        request_instance.manager_opinion_date = current_date.strftime('%Y/%m/%d')
        request_instance.manager_opinion_time = current_time
    elif current_status == 'COMITE':
        request_instance.committee_opinion = (action == 'CON')
        request_instance.committee_opinion_date = current_date.strftime('%Y/%m/%d')
        request_instance.committee_opinion_time = current_time
    elif current_status == 'EXECUT':
        request_instance.executor_report = (action == 'CON')
        request_instance.executor_report_date = current_date.strftime('%Y/%m/%d')
        request_instance.executor_report_time = current_time
    elif current_status == 'TESTER':
        request_instance.tester_report = (action == 'CON')
        request_instance.tester_report_date = current_date.strftime('%Y/%m/%d')
        request_instance.tester_report_time = current_time
    
    request_instance.save()
    
    # فراخوانی توابع مربوطه بر اساس وضعیت جدید
    if current_status == 'DRAFTD':
        doc_response = register_document(
            app_doc_id=request_instance.id,
            priority=get_priority_title(request_instance.priority.id),
            doc_state='پیش نویس',
            document_title=request_instance.change_title,
            app_code=APP_CODE,
            owner_nationalcode=request_instance.requestor_nationalcode
        )
        request_instance.doc_id = doc_response['data']['id']
        request_instance.save()
    if new_status in ['MANAGE', 'EXECUT', 'COMITE', 'TESTER']:
        send_document(
            doc_id=request_instance.doc_id,
            sender_national_code=user_nationalcode,
            inbox_owners_national_code=get_inbox_owners_national_code(new_status, request_instance)
        )
    elif new_status == 'FINISH':
        finish_flow(request_instance.doc_id, APP_CODE)
    elif new_status == 'FAILED':
        terminate_flow(request_instance.doc_id, APP_CODE)
    
    # به‌روزرسانی وضعیت سند
    # erfan
    update_document_state_code(request_instance.doc_id, APP_CODE, new_status)

    # حالت هایی که فرآیند پایان می یابد
    if new_status == 'FAILED':
        message = 'با توجه به رد مدرک، فرآیند متوقف گردید'
    elif new_status == 'FINISH':
        message = 'فرآیند با موفقیت خاتمه پیدا کرد'
    else:
        message = f'فرم با موفقیت برای {user_info} ارسال شد'
    return {'success':True,'message':message, 'request_id':request_id}
def get_next_status(current_status):
    # تابعی برای دریافت وضعیت بعدی بر اساس وضعیت فعلی
    status_order = ['DRAFTD', 'MANAGE', 'COMITE', 'EXECUT', 'TESTER', 'FINISH']
    return status_order[status_order.index(current_status) + 1]

def get_previous_status(current_status):
    # تابعی برای دریافت وضعیت قبلی بر اساس وضعیت فعلی
    status_order = ['DRAFTD', 'MANAGE', 'COMITE', 'EXECUT', 'TESTER', 'FINISH']
    return status_order[status_order.index(current_status) - 1]

def get_priority_title(priority_id):
    # تابعی برای دریافت عنوان اولویت بر اساس شناسه اولویت
    priority_instance = m.ConstValue.objects.get(id=priority_id)
    return priority_instance.Caption

def get_inbox_owners_national_code(status:str, request_instance: m.ConfigurationChangeRequest)->str:
    # تابعی برای دریافت کد ملی دریافت‌کنندگان بر اساس وضعیت
    if status == 'MANAGE':
        return request_instance.manager_nationalcode.national_code
    elif status == 'EXECUT':
        return request_instance.executor_nationalcode.national_code
    elif status == 'COMITE':
        return request_instance.committee_user_nationalcode.national_code
    elif status == 'TESTER':
        return request_instance.tester_nationalcode.national_code

# این تابع کد تیم و سمت را از متغییر ورودی جدا کرده و بازگشت می دهد
def get_team_role(team_role:str, value:str):
    if '-' in value:
        if team_role == 'T':
            return value.split('-')[0]
        elif team_role == 'R':
            return value.split('-')[1]
    else:
        return None

    return None

# این تابع درصورتی که کد درخواستی وجود داشته باشد، اطلاعات آن را به روز می کند و اگر وجود نداشته باشد آن را ایجاد می کند
def save_form(form_data) -> int:
    # بررسی وجود شناسه درخواست
    request_id = form_data.get('request_id')
    
    
    # کلیدهای خارجی را باید به معادل آن تبدیل کنیم چون برای مقداردهی به نمونه مربوطه احتیاج دارد و مقدار کلید را قبول نمی کند
    executor_nationalcode = form_data.get('executor_user_nationalcode')
    if executor_nationalcode:
        executor_nationalcode = m.User.objects.get(national_code=executor_nationalcode)

    tester_nationalcode = form_data.get('tester_user_nationalcode')
    if tester_nationalcode:
        tester_nationalcode = m.User.objects.get(national_code=tester_nationalcode)

    requestor_nationalcode = form_data.get('requestor_user_nationalcode')
    if requestor_nationalcode:
        requestor_nationalcode = m.User.objects.get(national_code=requestor_nationalcode)

    executor_role = None
    executor_role_id = form_data.get('executor_user_role')
    if executor_role_id:
        try:
            executor_role = m.Role.objects.get(role_id=executor_role_id)
        except m.Role.DoesNotExist:
            executor_role = None

    tester_role = None
    tester_role_id = form_data.get('tester_user_role')
    if tester_role_id:
        try:
            tester_role = m.Role.objects.get(role_id=tester_role_id)
        except m.Role.DoesNotExist:
            tester_role = None

    requestor_role = None
    requestor_role_id = form_data.get('requestor_user_role')
    if requestor_role_id:
        try:
            requestor_role = m.Role.objects.get(role_id=requestor_role_id)
        except m.Role.DoesNotExist:
            requestor_role = None

    executor_team_code = form_data.get('executor_user_team')
    if executor_team_code:
        executor_team = m.Team.objects.get(team_code=executor_team_code)

    tester_team_code = form_data.get('tester_user_team')
    if tester_team_code:
        tester_team = m.Team.objects.get(team_code=tester_team_code)

    requestor_team_code = form_data.get('requestor_user_team')
    if requestor_team_code:
        requestor_team = m.Team.objects.get(team_code=requestor_team_code)


    committee_user_nationalcode = form_data.get('committee_user_nationalcode')
    if committee_user_nationalcode:
        committee_user_nationalcode = m.User.objects.get(national_code=committee_user_nationalcode)

    manager_nationalcode = form_data.get('manager_nationalcode')
    if manager_nationalcode:
        manager_nationalcode = m.User.objects.get(national_code=manager_nationalcode)
    

    if request_id:
        # به‌روزرسانی اطلاعات درخواست موجود
        request = m.ConfigurationChangeRequest.objects.filter(id=request_id).first()
        if request:
            # نقش های درگیر
            request.executor_nationalcode = executor_nationalcode
            request.tester_nationalcode = tester_nationalcode
            request.requestor_nationalcode = requestor_nationalcode

            request.executor_team_code = executor_team
            request.tester_team_code = tester_team
            request.requestor_team_code = requestor_team
            
            request.executor_role_id = executor_role
            request.tester_role_id = tester_role
            request.requestor_role_id = requestor_role
            
            request.committee_user_nationalcode = committee_user_nationalcode

            committee_id = form_data.get('committee')
            if committee_id:
                request.committee_id = committee_id

            request.need_committee = form_data.get('need_committee')

            request.manager_nationalcode = manager_nationalcode

            request.test_required = form_data.get('need_test')
            
            # ویژگی های تغییر
            request.change_level_id = form_data.get('change_level')
            request.classification_id = form_data.get('classification')
            request.priority_id = form_data.get('priority')
            request.risk_level_id = form_data.get('risk_level')

            # اطلاعات تغییر
            request.change_title = form_data.get('change_title')
            request.change_description = form_data.get('change_description')
            request.change_type_id = form_data.get('change_type')

            # محل تغییر
            request.change_location_data_center_id = form_data.get('change_location_data_center')
            request.change_location_database_id = form_data.get('change_location_database')
            request.change_location_systems_id = form_data.get('change_location_systems')
            request.change_location_other_id = form_data.get('change_location_other')
            request.change_location_other_description_id = form_data.get('change_location_other_description')

            # حوزه تغییر
            request.change_domain_id = form_data.get('change_domain')

            # زمانبندی تغییرات
            request.changing_date = form_data.get('change_date')
            request.changing_time = form_data.get('change_time')
            request.changing_date_actual = form_data.get('changing_date_actual')
            request.changing_duration = form_data.get('changing_duration')
            request.changing_duration_actual = form_data.get('changing_duration_actual')
            request.downtime_duration = form_data.get('downtime_duration')
            request.downtime_duration_worstcase = form_data.get('downtime_duration_worstcase')
            request.downtime_duration_actual = form_data.get('downtime_duration_actual')

            # اثر گذاری تغییر
            request.stop_critical_service = form_data.get('stop_critical_service')
            request.critical_service_title = form_data.get('critical_service_title')
            request.stop_sensitive_service = form_data.get('stop_sensitive_service')
            request.stop_service_title = form_data.get('stop_service_title')
            request.not_stop_any_service = form_data.get('not_stop_any_service')

            # طرح بازگشت
            request.has_role_back_plan = form_data.get('has_role_back_plan')
            request.role_back_plan_description = form_data.get('role_back_plan_description')

            # الزامات تغییر
            request.reason_regulatory = form_data.get('reason_regulatory')
            request.reason_technical = form_data.get('reason_technical')
            request.reason_security = form_data.get('reason_security')
            request.reason_business = form_data.get('reason_business')
            request.reason_other = form_data.get('reason_other')
            request.reason_other_description = form_data.get('reason_other_description')

            # اطلاعات تکمیلی سایر مراحل
            # نظر مدیر
            request.manager_opinion = form_data.get('manager_opinion')
            request.manager_opinion_date = form_data.get('manager_opinion_date')
            request.manager_reject_description = form_data.get('manager_reject_description')
            
            # نظر کمیته
            request.committee_opinion = form_data.get('committee_opinion')
            request.committee_opinion_date = form_data.get('committee_opinion_date')
            request.committee_reject_description = form_data.get('committee_reject_description')

            # گزارش اجرا
            request.executor_report = form_data.get('executor_report')
            request.executor_report_date = form_data.get('executor_report_date')
            request.execution_description = form_data.get('execution_description')
            
            # گزارش تست
            request.test_date = form_data.get('test_date')
            request.tester_report = form_data.get('tester_report')
            request.tester_report_date = form_data.get('tester_report_date')
            request.test_report_description = form_data.get('test_report_description')

            request.save()
    else:
        # ایجاد درخواست جدید
        request = m.ConfigurationChangeRequest.objects.create(
            # نقش های درگیر

            executor_nationalcode = executor_nationalcode
            ,tester_nationalcode = tester_nationalcode
            ,requestor_nationalcode = requestor_nationalcode

            ,executor_team_code = executor_team
            ,tester_team_code = tester_team
            ,requestor_team_code = requestor_team
            
            ,executor_role_id = executor_role
            ,tester_role_id = tester_role
            ,requestor_role_id = requestor_role
            
            ,committee_user_nationalcode = committee_user_nationalcode
            ,committee_id = form_data.get('committee')
            ,need_committee = form_data.get('need_committee')

            ,manager_nationalcode = manager_nationalcode
            ,test_required = form_data.get('need_test')
            
            # ویژگی های تغییر
            ,change_level_id = form_data.get('change_level')
            ,classification_id = form_data.get('classification')
            ,priority_id = form_data.get('priority')
            ,risk_level_id = form_data.get('risk_level')

            # اطلاعات تغییر
            ,change_title = form_data.get('change_title')
            ,change_description = form_data.get('change_description')
            ,change_type_id = form_data.get('change_type')

            # محل تغییر
            ,change_location_data_center = form_data.get('change_location_data_center')
            ,change_location_database = form_data.get('change_location_database')
            ,change_location_systems = form_data.get('change_location_systems')
            ,change_location_other = form_data.get('change_location_other')
            ,change_location_other_description = form_data.get('change_location_other_description')

            # حوزه تغییر
            ,change_domain_id = form_data.get('change_domain')

            # زمانبندی تغییرات
            ,changing_date = form_data.get('change_date')
            ,changing_time = form_data.get('change_time')
            ,changing_duration = form_data.get('changing_duration')
            ,downtime_duration = form_data.get('downtime_duration')
            ,downtime_duration_worstcase = form_data.get('downtime_duration_worstcase')

            # اثر گذاری تغییر
            ,stop_critical_service = form_data.get('stop_critical_service')
            ,critical_service_title = form_data.get('critical_service_title')
            ,stop_sensitive_service = form_data.get('stop_sensitive_service')
            ,stop_service_title = form_data.get('stop_service_title')
            ,not_stop_any_service = form_data.get('not_stop_any_service')

            # طرح بازگشت
            ,has_role_back_plan = form_data.get('has_role_back_plan')
            ,role_back_plan_description = form_data.get('role_back_plan_description')

            # الزامات تغییر
            ,reason_regulatory = form_data.get('reason_regulatory')
            ,reason_technical = form_data.get('reason_technical')
            ,reason_security = form_data.get('reason_security')
            ,reason_business = form_data.get('reason_business')
            ,reason_other = form_data.get('reason_other')
            ,reason_other_description = form_data.get('reason_other_description')
        )

    # حذف رکوردهای موجود و درج رکوردهای جدید
    # تیم‌ها
    # مواردی که هم اکنون در دیتابیس وجود دارد را استخراج می کنیم
    existing_teams = m.RequestTeam.objects.filter(request=request)
    for team_code in form_data.get('teams', []):
        if team_code not in existing_teams:
            # اگر موردی در لیست باشد که در دیتابیس وجود نداشته باشد آن را اضافه می کنیم
            m.RequestTeam.objects.create(request=request, team_code_id=team_code)
    # مواردی که در لیست نیستند ولی در دیتابیس هستند را حذف می کنیم
    existing_teams.exclude(team_code_id__in=form_data.get('teams', [])).delete()

    # شرکت‌ها
    # مواردی که هم اکنون در دیتابیس وجود دارد را استخراج می کنیم
    existing_corps = m.RequestCorp.objects.filter(request=request)
    for corp_code in form_data.get('corps', []):
        if corp_code not in existing_corps:
            # اگر موردی در لیست باشد که در دیتابیس وجود نداشته باشد آن را اضافه می کنیم
            m.RequestCorp.objects.create(request=request, corp_code_id=corp_code)
    # مواردی که در لیست نیستند ولی در دیتابیس هستند را حذف می کنیم
    existing_corps.exclude(corp_code_id__in=form_data.get('corps', [])).delete()

    # اطلاعات تکمیلی
    # مواردی که هم اکنون در دیتابیس وجود دارد را استخراج می کنیم
    existing_extra_info = m.RequestExtraInformation.objects.filter(request=request)
    for extra_info_id in form_data.get('extra_information', []):
        if extra_info_id not in existing_extra_info:
            # اگر موردی در لیست باشد که در دیتابیس وجود نداشته باشد آن را اضافه می کنیم
            m.RequestExtraInformation.objects.create(request=request, extra_info_id=extra_info_id)
    # مواردی که در لیست نیستند ولی در دیتابیس هستند را حذف می کنیم
    existing_extra_info.exclude(extra_info_id__in=form_data.get('extra_information', [])).delete()

    return request.id

# این تابع صحت سنجی فرم را انجام می دهد در صورتی که خطا داشته باشد مقدار بازگشتی برابر با پیام های خطا خواهد بود
def form_validation(form_data):
    errors = []

    # اعتبارسنجی فیلدهای الزامی
    required_fields = {
        'requestor_user_nationalcode': "کد ملی درخواست دهنده الزامی است.",
        'requestor_user_role': "سمت درخواست‌دهنده الزامی است.",
        'requestor_user_team': "تیم درخواست‌دهنده الزامی است.",
        'executor_user_nationalcode': "کد ملی مجری الزامی است.",
        'executor_user_role': "سمت مجری الزامی است.",
        'executor_user_team': "تیم مجری الزامی است.",
        'tester_user_nationalcode': "کد ملی تستر الزامی است.",
        'tester_user_role': "سمت تستر الزامی است.",
        'tester_user_team': "تیم تستر الزامی است.",
        'change_title': "عنوان تغییر الزامی است.",
        'change_description': "توضیحات تغییر الزامی است.",
        'change_type': "نوع تغییر الزامی است.",
    }

    # اگر تست نیازی ندارد، نباید شناسه آن وجود داشته باشد
    if form_data.get('need_test') == 0:
        form_data.pop('tester_user_nationalcode', None)
    else:
        required_fields['tester_user_nationalcode'] = 'انتخاب تستر الزامی است.' 
        
    # اگر نیاز به کمیته ندارد، باید شناسه مربوطه حذف شود
    if form_data.get('need_committee') == 0:
        form_data.pop('committee', None)
    else:
        required_fields['committee'] = 'انتخاب کمیته الزامی است.' 
    
    # بررسی فیلدهای الزامی
    for field, error_message in required_fields.items():
        if not form_data.get(field):
            errors.append(error_message)

    # فیلدهای تاریخ
    date_fields = [
        ('change_date','تاریخ تغییرات'),
        ('change_date_actual','تاریخ واقعی انجام تغییرات'),
        ('test_date', 'تاریخ انجام تست'),
        ('tester_report_date','تاریخ گزارش تست'),
        ('manager_opinion_date','تاریخ اظهار نظر مدیر مستقیم'),
        ('committee_opinion_date','تاریخ اظهار نظر کمیته'),
    ]
    

    for field, description in date_fields:
        date = form_data.get(field)
        if date:
            try:
                # بررسی اینکه آیا ورودی از نوع رشته است
                if isinstance(date, str):
                    # تبدیل به تاریخ شمسی
                    date = jdatetime.datetime.strptime(date, '%Y/%m/%d')
                else:
                    errors.append(f"فرمت تاریخ برای '{description}' نامعتبر است.")
            except ValueError:
                errors.append(f"'{description}' باید در فرمت 'YYYY-MM-DD' باشد.")

    time_fields = [
        ('change_time','ساعت تغییرات'),
        ('change_time_actual','ساعت واقعی انجام تغییرات'),
        ('test_time', 'ساعت انجام تست'),
        ('tester_report_time','ساعت گزارش تست'),
        ('manager_opinion_time','ساعت اظهار نظر مدیر مستقیم'),
        ('committee_opinion_time','ساعت اظهار نظر کمیته'),
    ]
    
    for field, description in time_fields:
        time = form_data.get(field)
        if time:
            try:
                # بررسی اینکه آیا ورودی از نوع رشته است
                if isinstance(time, str):
                    # بررسی اینکه آیا فرمت زمان صحیح است
                    hours, minutes = map(int, time.split(':'))
                    if 0 <= hours <= 24 and 0 <= minutes <= 59:
                        pass
                    else:
                        errors.append(f"فرمت ساعت برای '{description}' نامعتبر است. ساعت باید بین 00:00 تا 23:59 باشد.")
                else:
                    errors.append(f"فرمت ساعت برای '{description}' نامعتبر است.")
            except ValueError:
                errors.append(f"'{description}' باید در فرمت 'HH:MM' باشد.")



    # کد ملی درخواست کننده
    if form_data.get('requestor_user_nationalcode') and not m.User.objects.filter(national_code=form_data['requestor_user_nationalcode']).exists():
        errors.append("کد ملی درخواست کننده نامعتبر است.")

    # تیم درخواست‌دهنده
    if form_data.get('requestor_user_team') and not m.Team.objects.filter(team_code=form_data['requestor_user_team']).exists():
        errors.append("تیم درخواست‌دهنده نامعتبر است.")

    # کد ملی مجری
    if form_data.get('executor_user_nationalcode') and not m.User.objects.filter(national_code=form_data['executor_user_nationalcode']).exists():
        errors.append("کد ملی مجری نامعتبر است.")

    # تیم مجری
    if form_data.get('executor_user_team') and not m.Team.objects.filter(team_code=form_data['executor_user_team']).exists():
        errors.append("تیم مجری نامعتبر است.")

    # کد ملی تستر
    if form_data.get('tester_user_nationalcode') and not m.User.objects.filter(national_code=form_data['tester_user_nationalcode']).exists():
        errors.append("کد ملی تستر نامعتبر است.")

    # تیم تستر
    if form_data.get('tester_user_team') and not m.Team.objects.filter(team_code=form_data['tester_user_team']).exists():
        errors.append("تیم تستر نامعتبر است.")

    # کد ملی مدیر
    if not form_data.get('manager_nationalcode'):
        manager_nationalcode = m.UserTeamRole.objects.filter(team_code=form_data['requestor_user_team'], role_id=form_data['requestor_user_role']).values('manager_national_code').first()
        if manager_nationalcode:
            form_data['manager_nationalcode'] = manager_nationalcode['manager_national_code']
        # حالتی است که مدیر کاربر پیدا نشده است
        else:
            errors.append("امکان تشخیص دادن مدیر کاربر درخواست دهنده وجود ندارد")
    elif not m.User.objects.filter(national_code=form_data['manager_nationalcode']).exists():
        errors.append("کد ملی مدیر نامعتبر است.")


    # شناسه کمیته
    if form_data.get('committee') and not m.Committee.objects.filter(id=form_data['committee']).exists():
        errors.append("شناسه کمیته نامعتبر است.")

    # کد ملی کاربر کمیته
    if form_data.get('committee_user_nationalcode') and not m.User.objects.filter(national_code=form_data['committee_user_nationalcode']).exists():
        errors.append("کد ملی کاربر کمیته نامعتبر است.")

    if not form_data.get('committee_user_nationalcode'):
        committee_user_nationalcode = m.Committee.objects.filter(id=form_data['committee']).values('administrator_nationalCode').first()
        if committee_user_nationalcode:
            form_data['committee_user_nationalcode'] = committee_user_nationalcode['administrator_nationalCode']
        # حالتی است که مدیر کاربر پیدا نشده است
        else:
            errors.append("امکان تشخیص دادن کاربر کمیته وجود ندارد")
    elif not m.User.objects.filter(national_code=form_data['committee_user_nationalcode']).exists():
        errors.append("کد ملی کاربر کمیته نامعتبر است.")


    # گستردگی تغییرات
    if form_data.get('change_level') and not m.ConstValue.objects.filter(id=form_data['change_level']).exists():
        errors.append("گستردگی تغییرات نامعتبر است.")

    # طبقه‌بندی
    if form_data.get('classification') and not m.ConstValue.objects.filter(id=form_data['classification']).exists():
        errors.append("طبقه‌بندی نامعتبر است.")

    # اولویت
    if form_data.get('priority') and not m.ConstValue.objects.filter(id=form_data['priority']).exists():
        errors.append("اولویت نامعتبر است.")

    # سطح ریسک
    if form_data.get('risk_level') and not m.ConstValue.objects.filter(id=form_data['risk_level']).exists():
        errors.append("سطح ریسک نامعتبر است.")

    # دامنه تغییر
    if form_data.get('change_domain') and not m.ConstValue.objects.filter(id=form_data['change_domain']).exists():
        errors.append("دامنه تغییر نامعتبر است.")


    # نوع تغییر
    if form_data.get('change_type') and not m.ChangeType.objects.filter(id=form_data['change_type']).exists():
        errors.append("نوع تغییر نامعتبر است.")


    # اعتبارسنجی محل تغییر: سایر
    try:
        validator.Validator.validate_change_location_other(
            form_data.get('change_location_other'),
            form_data.get('change_location_other_description')
        )
    except ValidationError as e:
        errors.append(str(e))

    # اعتبارسنجی توقف خدمات بحرانی و حساس
    try:
        validator.Validator.validate_critical_service(
            form_data.get('stop_critical_service'),
            form_data.get('critical_service_title')
        )
    except ValidationError as e:
        errors.append(str(e))

    try:
        validator.Validator.validate_sensitive_service(
            form_data.get('stop_sensitive_service'),
            form_data.get('stop_service_title')
        )
    except ValidationError as e:
        errors.append(str(e))

    # اعتبارسنجی سایر الزامات
    try:
        validator.Validator.validate_reason_other(
            form_data.get('reason_other'),
            form_data.get('reason_other_description')
        )
    except ValidationError as e:
        errors.append(str(e))

    # اعتبارسنجی نظر مدیر
    try:
        validator.Validator.validate_manager_opinion(
            form_data.get('manager_opinion'),
            form_data.get('manager_reject_description')
        )
    except ValidationError as e:
        errors.append(str(e))

    # اعتبارسنجی فیلدهای کمیته
    try:
        validator.Validator.validate_committee_fields(
            form_data.get('need_committee'),
            form_data.get('committee_user_nationalcode'),
            form_data.get('committee_opinion_date'),
            form_data.get('committee_opinion'),
            form_data.get('committee_reject_description')
        )
    except ValidationError as e:
        errors.append(str(e))

    # اعتبارسنجی تاریخ تست و گزارش تست
    try:
        validator.Validator.validate_test_date(
            form_data.get('test_date'),
            form_data.get('changing_date_actual')
        )
    except ValidationError as e:
        errors.append(str(e))

    try:
        validator.Validator.validate_tester_report_date(
            form_data.get('tester_report_date'),
            form_data.get('test_date')
        )
    except ValidationError as e:
        errors.append(str(e))

    # اعتبارسنجی کلیدهای خارجی برای تیم‌ها
    for team_code in form_data.get('teams', []):
        if not m.Team.objects.filter(team_code=team_code).exists():
            errors.append(f"کد تیم '{team_code}' نامعتبر است.")

    # اعتبارسنجی کلیدهای خارجی برای شرکت‌ها
    for corp_code in form_data.get('corps', []):
        if not m.Corp.objects.filter(corp_code=corp_code).exists():
            errors.append(f"کد شرکت '{corp_code}' نامعتبر است.")

    # اعتبارسنجی مقادیر اطلاعات تکمیلی
    for extra_info_id in form_data.get('extra_information', []):
        if not m.ConstValue.objects.filter(id=extra_info_id).exists():
            errors.append(f"مقدار اطلاعات تکمیلی با شناسه '{extra_info_id}' نامعتبر است.")

    return errors

def get_dynamic_checkbox(type:str, request):
    # دریافت چک باکس‌های داینامیک برای 
    values = m.ConstValue.objects.filter(Code__startswith=type+'_', IsActive=True)
    
    extra_information = []
    for value in values:
        if (request.POST.get(value.Code) == value.Code):  # ذخیره وضعیت چک باکس
            extra_information.append(value.id)
    
    return extra_information

def get_selected_items(team_corp: str, request):
    # تعیین مدل بر اساس نوع (تیم یا شرکت)
    if team_corp == 't':
        items = m.Team.objects.all()
    elif team_corp == 'c':
        items = m.Corp.objects.all()
    else:
        return []

    selected_items = []
    for item in items:
        if request.POST.get(item.team_code if team_corp == 't' else item.corp_code):
            selected_items.append(item.team_code if team_corp == 't' else item.corp_code)

    return selected_items

def load_form_data(request_id:int, user_nationalcode:str):
    form_data = {}
    # مشخص می کنیم که وضعیت فعلی فرم چیست؟
    status_code = check_form_status(request_id, user_nationalcode) 
    form_data['status'] = status_code    
    
    # اگر کاربر مربوطه مجاز به مشاهده اطلاعات نباشد
    if status_code == 'INVALID':
        form_data['message'] = 'شما مجاز به مشاهده این فرم نیستید'
        return form_data
    
    # اگر در حالت به روزرسانی و یا مشاهده باشیم باید اطلاعات درخواست را دریافت کنیم
    if status_code in ['READONLY','UPDATE']:
        # اگر شناسه درخواست معتبر باشد، اطلاعات شناسه درخواست هم ارسال می شود
        request_data = m.ConfigurationChangeRequest.objects.filter(id=request_id).first()
        if request_data:
            form_data['request_data'] = request_data  # اضافه کردن اطلاعات درخواست به data

    # اگر در حالت ویرایش و یا درج باشیم بایستی اطلاعات تکمیلی را هم اضافه کنیم
    if status_code in ['UPDATE','INSERT']:

        
        # فیلتر کردن رکوردهای مربوط به طبقه بندی
        classification_values = m.ConstValue.objects.filter(Code__startswith='Classification_', IsActive=True)
        classification_default = 'Classification_Normal'
        
        # فیلتر کردن رکوردهای مربوط به دامنه تغییرات
        change_level_values = m.ConstValue.objects.filter(Code__startswith='ChangeLevel_', IsActive=True)
        change_level_default = 'ChangeLevel_Minor'
        
        # فیلتر کردن رکوردهای مربوط به اولویت تغییر
        priority_values = m.ConstValue.objects.filter(Code__startswith='Priority_', IsActive=True)
        priority_default = 'Priority_Standard'
        
        # فیلتر کردن رکوردهای مربوط به سطح ریسک تغییر
        risk_level_values = m.ConstValue.objects.filter(Code__startswith='RiskLevel_', IsActive=True)
        risk_level_default = 'RiskLevel_Low'
        
        # فیلتر کردن رکوردهای مربوط به تغییرات مرکز داده
        data_center_values = m.ConstValue.objects.filter(Code__startswith='DataCenter_', IsActive=True)
        
        # فیلتر کردن رکوردهای مربوط به سیستم ها و سرویس ها
        systems_services_values = m.ConstValue.objects.filter(Code__startswith='SystemsServices_', IsActive=True)
        
        # فیلتر کردن رکوردهای مربوط به محدوده تغییر
        domain_values = m.ConstValue.objects.filter(Code__startswith='Domain_', IsActive=True)
        
        # فیلتر کردن رکوردهای مربوط به نوع پیوست
        attachment_type_values = m.ConstValue.objects.filter(Code__startswith='AttachmentType_', IsActive=True)
        
        # فیلتر کردن رکوردهای مربوط به وضعیت
        status_values = m.ConstValue.objects.filter(Code__startswith='Status_', IsActive=True)

        committee = m.Committee.objects.filter(is_active=True)

        corps = m.Corp.objects.all()
        teams = m.Team.objects.all()
        
        # نوع تغییر را از جدول مربوطه می گیریم
        change_type = m.ChangeType.objects.all()
        
        # شرکت های مربوط به انواع تغییر
        change_type_request_corp = m.RequestCorp_ChangeType.objects.all()
        # تیم های مربوط به انواع تغییر
        change_type_request_team = m.RequestTeam_ChangeType.objects.all()
        
        change_type_data_center_list = m.RequestExtraInformation_ChangeType.objects.filter(extra_info__Code__startswith='DataCenter_')
        change_type_database_list = m.RequestExtraInformation_ChangeType.objects.filter(extra_info__Code__startswith='Database_')
        change_type_systems_list = m.RequestExtraInformation_ChangeType.objects.filter(extra_info__Code__startswith='SystemsServices_')
        
        
        # این قسمت از کد باید با توجه به مکانیزم جدید احراز هویت جایگزین شود
        # erfan
        current_user = {'fullname': 'محمد سپه کار', "username":"m.sepahkar", "national_code": "1280419180", "gender": "M","is_active":True,
                        'team_roles':[{"role_title":"برنامه نویس","role_id":132,"team_name":"خودرو", "team_code":"MIS", 
                                    "manager_national_code":"0063967782", "Level_id":4, "level_title":"", "is_suprior":True,
                                    "start_date":"", "end_date":""},
                                    {"role_title":"پشتیبان","role_id":121,"team_name":"عمر", "team_code":"EVA", "manager_national_code":"0029893003"}]}
        
        all_users = [{'fullname': 'مجید خاکور',"username":"m.khakvar@eit", "national_code": "0017901030", "gender": "M",
                    'team_roles':[{"role_title":"مدیر عامل","role_id":98,"team_name":"مدیریت عامل", "team_code":"CTO", "manager_national_code":""}]}, 
                    {'fullname': 'مریم سلطانی',"username":"m.soltani@eit", "national_code": "6309920952", "gender": "F",
                        'team_roles':[{"role_title":"پشتیبان","role_id":53,"team_name":"عمر", "team_code":"LIF", "manager_national_code":"0029893003"}]},
                        {'fullname': 'امید مشعشعی',"username":"o.moshashai@eit", "national_code": "0010748148", "gender": "M",
                        'team_roles':[{"role_title":"مدیر ادمین","role_id":63,"team_name":"ادمین", "team_code":"ADM", "manager_national_code":"0029893003"},
                                    {"role_title":"مدیر نسخه","role_id":53,"team_name":"نسخه", "team_code":"VER", "manager_national_code":"0029893003"},
                                    {"role_title":"معاون عملیات","role_id":53,"team_name":"معاونت عملیات", "team_code":"OAS", "manager_national_code":"0029893003"}]},
                        {'fullname': 'مینا ضیائی',"username":"m.ziyaei@eit", "national_code": "0063425750", "gender": "F",
                        'team_roles':[{"role_title":"تستر","role_id":53,"team_name":"عمر", "team_code":"LIF", "manager_national_code":"0029893003"}]},
                        {'fullname': 'سعید فیضی',"username":"s.feizi@eit", "national_code": "3979843076", "gender": "M",
                        'team_roles':[{"role_title":"برنامه نویس","role_id":63,"team_name":"خودرو", "team_code":"WEB", "manager_national_code":"0029893003"},
                                    {"role_title":"برنامه نویس","role_id":63,"team_name":"عمر", "team_code":"LIF", "manager_national_code":"0029893003"}]}]
        
        request_date = request_date = jdatetime.datetime.now().strftime('%Y/%m/%d')
        breadcrumbs = [{'name':'اطلاعات درخواست','order':1, 'default':True},
                    {'name':'اطلاعات اجرا','order':2, 'default':False}]
    
        form_data.update({
            'classification_values': classification_values,
            'classification_default': classification_default,
            'change_level_values': change_level_values,
            'change_level_default': change_level_default,
            'priority_values': priority_values,
            'priority_default': priority_default,
            'risk_level_values': risk_level_values,
            'risk_level_default': risk_level_default,
            'data_center_values': data_center_values,
            'systems_services_values': systems_services_values,
            'domain_values': domain_values,
            'attachment_type_values': attachment_type_values,
            'status_values': status_values,
            'committee': committee,
            'corps': corps,
            'teams': teams,
            'request_number':'-',
            'request_date': request_date,
            'breadcrumbs':breadcrumbs,
            'current_user': current_user,
            'all_users': all_users,
            'change_type': change_type,
            'change_type_data_center_list':change_type_data_center_list,
            'change_type_systems_list':change_type_systems_list,
            'change_type_request_corp':change_type_request_corp,
            'change_type_database_list':change_type_database_list,
            'change_type_request_team':change_type_request_team
        })
        

    return form_data