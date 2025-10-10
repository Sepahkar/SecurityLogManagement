from django.shortcuts import render, redirect
from .business import ChangeType, Request, FormManager, Task
from django.http import JsonResponse
import logging
import json
import inspect

in_EIT = False

def get_current_user(request):
    if in_EIT:
        current_user = request.user.national_code
    else:
        request_id = 4
        from . import models as m
        objRequest = m.ConfigurationChangeRequest.objects.filter(id=request_id).first()
        
        if objRequest:
            requestor = objRequest.requestor_nationalcode.national_code
            rel_manger = objRequest.related_manager_nationalcode.national_code
            manager = objRequest.direct_manager_nationalcode.national_code
            commitee = objRequest.committee_user_nationalcode.national_code if objRequest.committee_user_nationalcode else None
            # استخراج همه تسک‌های مربوط به این درخواست
            tasks = m.RequestTask.objects.filter(request_id=request_id)
            Task = []

            for task in tasks:
                # پیدا کردن اولین مجری (RoleCode='E') و اولین تستر (RoleCode='T') برای هر تسک
                executor_user = task.requesttaskuser_set.filter(user_role_code='E').first()
                tester_user = task.requesttaskuser_set.filter(user_role_code='T').first()

                executor_name = executor_user.user_nationalcode.national_code if executor_user else ''
                tester_name = tester_user.user_nationalcode.national_code if tester_user else ''

                Task.append([executor_name, tester_name])
            # حالا Task[i][0] مجری و Task[i][1] تستر تسک iام است (i از 0 شروع می‌شود)
            print(Task)
            
        else:
            requestor = '1280419180'
            manager = '1379150728'
            rel_manger = '0081578091'
            commitee = '5228300880'

            task1_executor = '6309920952'
            task1_test = '0074322060'

            task2_executor = '0063425750'
            task2_test = ''

            task3_executor = '0074322060'
            task3_test = '6309920952'

            task4_executor = '0080556787'
            task4_test = '6000091631'

        # حالا بر اساس مرحله، کاربر جاری را مشخص می کنیم
        if objRequest:
            if objRequest.status_code == 'DRAFTD':
                current_user = requestor
            elif objRequest.status_code == 'DIRMAN':
                current_user = manager
            elif objRequest.status_code == 'RELMAN':
                current_user = rel_manger
            elif objRequest.status_code == 'COMITE':
                current_user = commitee
            elif objRequest.status_code == 'DOTASK':
                # اینجا نخستین تسکی که وضعیت آن TASFIN یا TASFAL نیست را پیدا می کنیم.
                first_valid_task = None
                for idx, task in enumerate(tasks):
                    if task.status_code not in ['TASFIN', 'TASFAL']:
                        first_valid_task = (idx, task)
                        break

                if first_valid_task is not None:
                    idx, task_obj = first_valid_task
                    if task_obj.status_code in ['EXESEL', 'EXERED', 'DEFINE']:
                        current_user = Task[idx][0]  # مجری
                    else:
                        current_user = Task[idx][1]  # تستر
                else:
                    current_user = ''  # اگر تسک معتبری نبود
        else:     
            current_user = requestor

    if not current_user:
        current_user = requestor

    print(current_user)
    return current_user

logging.basicConfig(
    filename='app.log',           # نام فایل لاگ
    filemode='a',                 # 'a' برای اضافه کردن، 'w' برای بازنویسی
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# def attachment_form_view(request):
#     """
#     این view فرم پیوست را نمایش می‌دهد
#     """
#     # دریافت اطلاعات کاربر جاری
#     current_user_nationalcode = current_user
    
#     # بارگذاری داده‌های فرم
#     data = b.load_form_data(-1, current_user_nationalcode)
    
#     # اضافه کردن اطلاعات خاص فرم پیوست
#     data['form_type'] = 'attachment'
#     data['page_title'] = 'فرم پیوست'
    
#     return render(request, 'ConfigurationChangeRequest/attachment-form.html', data)

def get_simple_form_data(request):
    """
    این تابع اطلاعات مربوط به فرم ساده را از شی درخواست http می گیرد

    Args:
        request (_type_): درخواست http
    """
    current_user_nationalcode = get_current_user(request)
    request_id = int(request.POST.get('request_id')) if request.POST.get('request_id') else -1

    # یک نمونه از شی فرم ایجاد می کنیم
    objFormManager = FormManager(current_user_national_code=current_user_nationalcode, request_id=request_id)


    form_data = {
        'request_id': request_id, 
        'change_title': request.POST.get('change_title',''),
        'change_type': int(request.POST.get('change_type', -1)),
        'change_description': request.POST.get('change_description',''),
        'user_team_role': request.POST.get('user_team_role',''),
        'action': request.POST.get('action','CON'),
        'user_nationalcode': current_user_nationalcode,
        'objFormManager': objFormManager,
        'requestor_user_nationalcode': request.POST.get('requestor_user_nationalcode'),  # کد ملی ایجاد کننده درخواست
    }

    # سمت و تیم کاربر در قالب یک متغییر بازگشت داده می شود.
    # CAR-73 : یعنی تیم خودرو و سمتی که شناسه آن 73 است
    utr = request.POST.get('requestor_user_team_role','')
    user_team_role = objFormManager.get_user_team_role(utr)
    if user_team_role['success']:
        form_data['requestor_team_code']=user_team_role.get('team_code','')
        form_data['requestor_role_id']=user_team_role.get('role_id',-1)
    
    return form_data

def get_full_form_data(request,objFormManager :FormManager):
    # دریافت اطلاعات فرم ساده
    form_data = get_simple_form_data(request=request)
    # objFormManager :FormManager= form_data['objFormManager']  # اصلاح: استفاده از [] به جای ()
    #*******************************صفحه اول*****************************
    #################################سطر اول#############################
    #-----------------------------قسمت اول-----------------------------

    #-----------------------------قسمت دوم-----------------------------
    # ویژگی های تغییر
    form_data['classification'] = int(request.POST.get('classification')) if request.POST.get('classification') else None  # طبقه‌بندی
    form_data['change_level'] = int(request.POST.get('change_level')) if request.POST.get('change_level') else None  # سطح تغییر
    form_data['priority'] = int(request.POST.get('priority')) if request.POST.get('priority') else None  # اولویت
    form_data['risk_level'] = int(request.POST.get('risk_level')) if request.POST.get('risk_level') else None  # سطح ریسک

    #################################سطر دوم#############################
    #-----------------------------قسمت اول-----------------------------
    # محل تغییر
    form_data['change_location_DataCenter'] = request.POST.get('change_location_DataCenter') == 'true'  # محل تغییر: مرکز داده (Boolean)
    form_data['extra_information'] = []
    # دریافت چک باکس‌های داینامیک برای DataCenter
    extra_information = objFormManager.get_dynamic_checkbox('DataCenter', request)
    form_data['extra_information'].extend(extra_information)                    
    
    form_data['change_location_Database'] = request.POST.get('change_location_Database') == 'true'  # محل تغییر: پایگاه داده (Boolean)
    extra_information = objFormManager.get_dynamic_checkbox('Database', request)
    form_data['extra_information'].extend(extra_information)                    
    
    form_data['change_location_SystemServices'] = request.POST.get('change_location_SystemServices') == 'true'  # محل تغییر: سیستم‌ها (Boolean)
    # دریافت چک باکس‌های داینامیک برای SystemsServices
    extra_information = objFormManager.get_dynamic_checkbox('SystemServices', request)
    form_data['extra_information'].extend(extra_information)                    

    form_data['change_location_other'] = request.POST.get('change_location_other') == 'true'  # محل تغییر: سایر (Boolean)
    form_data['change_location_other_description'] = request.POST.get('change_location_other_description')  # توضیحات محل تغییر

    #-----------------------------قسمت دوم-----------------------------
    # دامنه تغییرات
    form_data['need_committee'] = request.POST.get('need_committee') == '1'  # نیاز به کمیته (Boolean)
    form_data['committee'] = int(request.POST.get('committee'))  # کمیته انتخاب شده
    form_data['domain'] = request.POST.get('domain')  # دامنه تغییر

    # دریافت چک باکس‌های داینامیک برای تیم‌ها
    form_data['teams'] = objFormManager.get_selected_items('t', request)

    # دریافت چک باکس‌های داینامیک برای شرکت‌ها
    form_data['corps'] = objFormManager.get_selected_items('c', request)

    #*******************************صفحه دوم*****************************
    #################################سطر اول#############################
    #-----------------------------قسمت اول-----------------------------
    # زمانبندی تغییرات
    form_data['changing_duration_hour'] = int(request.POST.get('duration_hour')) if request.POST.get('duration_hour') else None  # ساعت مدت زمان تغییرات
    form_data['changing_duration_minute'] = int(request.POST.get('duration_minute')) if request.POST.get('duration_minute') else None  # دقیقه مدت زمان تغییرات
    form_data['downtime_duration_hour'] = int(request.POST.get('estimate_downtime_hour')) if request.POST.get('estimate_downtime_hour') else None  # ساعت مدت زمان توقف
    form_data['downtime_duration_minute'] = int(request.POST.get('estimate_downtime_minute')) if request.POST.get('estimate_downtime_minute') else None  # دقیقه مدت زمان توقف
    form_data['downtime_duration_worstcase_hour'] = int(request.POST.get('worstcase_downtime_hour')) if request.POST.get('worstcase_downtime_hour') else None  # ساعت بدترین مدت زمان توقف
    form_data['downtime_duration_worstcase_minute'] = int(request.POST.get('worstcase_downtime_minute')) if request.POST.get('worstcase_downtime_minute') else None  # دقیقه بدترین مدت زمان توقف
    form_data['change_date'] = request.POST.get('request_date')  # تاریخ تغییر
    form_data['change_time'] = request.POST.get('request_time')  # تاریخ تغییر
    # ############################تست تاریخ شمسی#####################

    
    
    
    #-----------------------------قسمت دوم-----------------------------
    # حوزه اثرگذاری تغییر
    form_data['stop_critical_service'] = request.POST.get('ImpactOnCriticalService') == 'true'  # توقف خدمات بحرانی (Boolean)
    form_data['critical_service_title'] = request.POST.get('ImpactOnCriticalServiceDescription')  # عنوان خدمات بحرانی
    form_data['stop_sensitive_service'] = request.POST.get('ImpactOnSensitiveService') == 'true'  # توقف خدمات حساس (Boolean)
    form_data['stop_service_title'] = request.POST.get('ImpactOnSensitiveServiceDescription')  # عنوان خدمات متوقف شده
    form_data['not_stop_any_service'] = request.POST.get('ImpactNotOnAnyService') == 'true'  # عدم توقف هیچ خدماتی (Boolean)

    #################################سطر دوم#############################
    #-----------------------------قسمت اول-----------------------------
    # الزام تغییرات
    form_data['reason_regulatory'] = request.POST.get('ReasonRegulatory') == 'true'  # الزام قانونی (Boolean)
    form_data['reason_technical'] = request.POST.get('ReasonTechnical') == 'true'  # الزام فنی (Boolean)
    form_data['reason_security'] = request.POST.get('ReasonSecurity') == 'true'  # الزام امنیتی (Boolean)
    form_data['reason_business'] = request.POST.get('ReasonBusiness') == 'true'  # الزام کسب و کاری (Boolean)
    form_data['reason_other'] = request.POST.get('ReasonOther') == 'true'  # سایر الزامات (Boolean)
    form_data['reason_other_description'] = request.POST.get('ReasonOtherDescription')  # توضیحات الزامات دیگر


    #-----------------------------قسمت دوم-----------------------------
    # طرح بازگشت
    form_data['has_role_back_plan'] = request.POST.get('Rollback') == '1'  # وجود برنامه بازگشت (Boolean)
    form_data['role_back_plan_description'] = request.POST.get('RollbackPlan')  # توضیحات برنامه بازگشت

    #---------------------------نظرم مدیر---------------------------------
    form_data['manager_opinion'] = int(request.POST.get('manager_opinion')) if request.POST.get('manager_opinion') else None
    form_data['manager_reject_description'] = request.POST.get('manager_reject_description')

    
    
    return form_data
    
    

def request_create(request):
    """
    برای ایجاد یک درخواست جدید از این تابع استفاده می شود
    """
    current_user_nationalcode =  get_current_user(request)
    form_manager = FormManager(current_user_nationalcode)
    
    if request.method == 'POST':
        # دریافت اطلاعات فرم
        form_data = get_simple_form_data(request=request)
        
        # اعتبارسنجی فرم
        validation_result = form_manager.form_validation(form_data)
        
        if validation_result['success']:
            # ایجاد درخواست
            request_obj = Request(current_user_national_code=current_user_nationalcode, request_id=-1)
            result = request_obj.create_request(form_data, current_user_nationalcode)
            
            if result['success']:
                return JsonResponse({
                    'success': True, 
                    'request_id': result['request_id'],
                    'message': result.get('message','درخواست تغییر با موفقیت ایجاد شد و برای بررسی مدیر ارسال گردید')
                })
            else:
                return JsonResponse({'success': False, 'message': result['message']})
        else:
            return JsonResponse({'success': False, 'message': validation_result['message']})
    
    # بارگذاری داده‌های فرم
    data = form_manager.get_form_data(-1, current_user_nationalcode)
    if data['success'] == False:
        return JsonResponse({'success': False, 'message': data['message']})
    
    return render(request, 'ConfigurationChangeRequest/request-simple.html', data)

def request_view(request, request_id):
    """
    برای مشاهده فرم درخواست از این تابع استفاده می شود

    Args:
        request (request): اطلاعات درخواست http
        request_id (int): شناسه درخواست
    """
    current_user_nationalcode =  get_current_user(request)
    data = {}

    # ابتدا یک نمونه از شی درخواست ایجاد می کنیم
    request_obj = Request(current_user_national_code=current_user_nationalcode,request_id=request_id)    
    
    # اگر چنین درخواستی وجود نداشته باشد، باید پیام خطا به کاربر بدهیم
    if request_obj.request_id is None or request_obj.request_id < 0:
        return render(request, 'ConfigurationChangeRequest/404.html', data)    
    
    # ممکن است در زمان ایجاد درخواست، با خطا مواجه شده باشد
    if request_obj.error_message:
        return JsonResponse({'success': False, 'message': request_obj.error_message})
    
    # اگر درخواست معتبر باشد، باید بررسی کنیم که کدام فرم باید برای این کاربر باز شود
    form_manager = FormManager(current_user_national_code=current_user_nationalcode, request_id=request_id)   
    result = form_manager.check_form_status(user_nationalcode=current_user_nationalcode, request_id=request_id)
    
    # وضعیت فرم را به دست می آوریم. وضعیت پیش فرض درج است
    mode = result.get('mode', 'INSERT')
    
    # نوع فرم را به دست می آوریم، نوع پیش فرض، درخواست ساده است
    form = result.get('form', 'RequestSimple')
    
    # اگر وضعیت درج باشد، آنگاه باید به صفحه اصلی هدایت شویم
    if mode == 'INSERT':
        return request_create(request=request)
    
    if mode == 'INVALID':
        return render(request, 'ConfigurationChangeRequest/403.html', data)    
    
    # اگر حالت به روزرسانی باشد
    # و داده های جدید ارسال شده باشند
    if request.method == 'POST':

        form_data = {}
        # دریافت اطلاعات فرم
        if form == "RequestSimple":
            form_data = get_simple_form_data(request=request)
        elif form == "RequestFull":
            form_data = get_full_form_data(request=request, objFormManager=form_manager)      
        elif form == "TaskSelect":
             return task_select_view(request=request, request_obj=request_obj, task_obj=request_obj.current_task)
        elif form ==  "TaskReport":
            return task_report_view(request=request, request_obj=request_obj, task_obj=request_obj.current_task)
        else:
            JsonResponse({'success': False, 'message': 'امکان تشخیص فرم مورد نظر وجود ندارد'})     
        # چون الان در حالت ویرایش هستیم، باید شناسه درخواست را هم اضافه کنیم
        form_data['request_id'] = request_id 
        
        # اعتبارسنجی فرم
        validation_result = form_manager.form_validation(form_data)
        if validation_result['success']:
            # اطلاعات جدید درخواست به روزرسانی می شود
            result = request_obj.update_request(form_data, current_user_nationalcode)
            
            if result['success']:
                # عملیات را به دست می آوریم
                action = form_data.get('action', 'CON')
                # اگر عملیات به جز ذخیره سازی باشد
                # فرم باید به مرحله بعد ارسال شود
                if action and action!='SAV':
                    result = request_obj.next_step(
                        action_code= action, user_nationalcode=current_user_nationalcode
                    )                    
                    if result['success']:
                        return JsonResponse({
                            'success': True, 
                            'request_id': request_id,
                            'message':result.get('message', 'اطلاعات با موفقیت ذخیره شد')
                        })
                    else:
                        return JsonResponse({'success': False, 'message': result['message']})        

            else:
                return JsonResponse({'success': False, 'message': result['message']})     
        else:
            return JsonResponse({'success': False, 'message': result['message']})         
        
        
    # بارگذاری داده‌های فرم
    data = request_obj.load_record_data(current_user_nationalcode)    

    # اگر فرم درخواست ساده باشد
    if form == 'RequestSimple':
        return render(request, 'ConfigurationChangeRequest/request-simple.html', data)

    # اگر فرم درخواست کامل باشد
    elif form == 'RequestFull':
        return request_full_view(request, request_id, data, False)

    # اگر فرم درخواست کامل فقط خواندنی باشد
    elif form == 'RequestFull-Readonly':
        return request_full_view(request, request_id, data, True)
    
    # اگر فرم لیست تسک ها باشد
    elif form == 'TaskList':
        return task_list_view(request, request_obj)

    # اگر فرم انتخاب تسک باشد
    elif form == 'TaskSelect':
        return task_select_view(request, request_obj, request_obj.current_task, mode)
    
    # اگر فرم گزارش تسک باشد
    elif form == 'TaskReport':
        return task_report_view(request, request_obj, request_obj.current_task, mode)
    
    # در غیر این صورت، فرم پیش‌فرض برای ایجاد درخواست بارگذاری می شود
    return request_create(request)


def request_full_view(request, request_id, data, readonly=False):
    """
    فرم درخواست کامل (مرحله دوم)
    """
    current_user_nationalcode =  get_current_user(request)
    form_manager = FormManager(current_user_nationalcode)
    request_obj: Request = None
    if request.method == 'POST':
        # دریافت اطلاعات فرم کامل
        form_data = request.POST.dict()
        form_data['request_id'] = request_id
        
        # اعتبارسنجی فرم
        validation_result = form_manager.form_validation(form_data)
        
        if validation_result['success']:
            # به‌روزرسانی درخواست
            request_obj = Request(current_user_national_code=current_user_nationalcode, request_id=request_id)
            result = request_obj.update_request(form_data)
            
            if result['success']:
                return JsonResponse({'success': True, 'message': 'درخواست با موفقیت به‌روزرسانی شد'})
            else:
                return JsonResponse({'success': False, 'message': result['message']})
        else:
            return JsonResponse({'success': False, 'message': validation_result['message']})
    
    # بارگذاری داده‌های فرم
    if not data:
        data = request_obj.load_record_data(request_id, current_user_nationalcode)
    
    # اضافه کردن لیست کاربران برای کومبو
    if 'all_users' in data:
        data['user_team_roles'] = data['all_users']
    if readonly:
        return render(request, 'ConfigurationChangeRequest/request-full-readonly.html', data)
    else:
        return render(request, 'ConfigurationChangeRequest/request-full.html', data)

def task_select_view(request, request_obj:Request, task_obj:Task, mode:str='READONLY'):
    """
    انتخاب تسک (برای مجری/تستر)
    """
    current_user_nationalcode =  get_current_user(request)
    form_manager = FormManager(current_user_nationalcode)
    
    if request.method == 'POST':
        # تسک توسط کاربر جاری انتخاب شده است
        result = task_obj.select_task(current_user_nationalcode)
        return JsonResponse({'success': result.get('success',True), 'message': result.get('message','')})
    
    # بارگذاری داده‌های تسک
    data = form_manager.load_task_data(request_obj, task_obj, current_user_nationalcode)
    data['mode'] = mode
    return render(request, 'ConfigurationChangeRequest/request-task-select.html', data)

def task_list_view(request, request_obj:Request):
    """
    مشاهده لیست تسک ها
    """
    current_user_nationalcode =  get_current_user(request)

    # بارگذاری داده‌های تسک
    # data = form_manager.load_task_data(request_obj, task_obj, current_user_nationalcode)
    data = {'success':True,
            'is_task':True,
            'mode':'READONLY',
        'request':request_obj.request_instance,
        'tasks':request_obj.tasks
        
    }
    return render(request, 'ConfigurationChangeRequest/request-task-list.html', data)


def task_report_view(request, request_obj:Request, task_obj:Task, mode:str='READONLY'):
    """
    گزارش تسک (برای مجری/تستر)
    """
    current_user_nationalcode =  get_current_user(request)
    form_manager = FormManager(current_user_nationalcode)

    if request.method == 'POST':
        # دریافت گزارش تسک
        form_data = request.POST.dict()

        # نگاشت فیلدهای فرم به نام‌های مورد انتظار
        form_data['operation_date'] = form_data.get('done_date')
        form_data['operation_time'] = form_data.get('done_time')
        form_data['operation_report'] = form_data.get('report_text')
        form_data['operation_result'] = 'true'  # فرض بر موفقیت عملیات

        # ذخیره گزارش تسک
        result = task_obj.save_task_report(task_obj.request_task_id, form_data, current_user_nationalcode)

        if result['success']:
            # انتقال به مرحله بعدی
            next_result = task_obj.next_step('CON')
            if next_result['success']:
                return JsonResponse({'success': True, 'message': next_result.get('message', 'گزارش تسک با موفقیت ذخیره شد'), 'request_id': request_obj.request_id})
            else:
                return JsonResponse({'success': False, 'message': next_result['message']})
        else:
            return JsonResponse({'success': False, 'message': result['message']})

    # بارگذاری داده‌های تسک
    data = form_manager.load_task_data(request_obj, task_obj, current_user_nationalcode)
    data['mode'] = mode
    return render(request, 'ConfigurationChangeRequest/request-task-report.html', data)



def request_notify_group_management(request, request_id:int, operation_type:str, notify_group_id:int)-> dict:
    """
    این تابع گروه های اطلاع رسانی ذیل یک درخواست را مدیریت می کند.

    Args:
        request (_type_): درخواست http
        notify_group_id (int): شناسه گروه اطلاع رسانی مورد نظر 
        request_id (int): شناسه  درخواست
        operation_type (_type_): یکی از موارد زیر است:
            A: برای اضافه کردن
            D: برای حذف کردن
    Return value:
        یک  جسیون مشابه به مورد زیر شامل این اطلاعات:
            {'success':, 'message':''}
            success: در صورتی که اجرا موفقیت آمیز باشد برابر با True و در غیر این صورت False خواهد بود
            message پیام مرتبط خصوصا در صورت وقوع خطا نشان می دهد که چه خطایی رخ داده است
    
    """
    
    current_user_national_code = get_current_user(request)
    obj_form_manager = FormManager(current_user_national_code=current_user_national_code, request_id=-1)
    result = obj_form_manager.notify_group_managment(request_id, notify_group_id, operation_type, 'R')
    return JsonResponse(result)


def request_task_management(request, request_id:int, operation_type:str, task_id:int)-> dict:
    """
    این تابع افراد ذیل یک تسک را مدیریت می کند.

    Args:
        request (_type_): درخواست http
        task_id (int): شناسه تسک مورد نظر در درخواست و یا نوع درخواست
        operation_type (_type_): یکی از موارد زیر است:
            a: اضافه کردن کاربر جدید
            d: حذف کاربر مربوطه
        user_national_code (کد ملی کاربر): کد ملی کاربر مورد نظر
                    
    Return value:
        یک  جسیون مشابه به مورد زیر شامل این اطلاعات:
            {'success':, 'message':''}
            success: در صورتی که اجرا موفقیت آمیز باشد برابر با True و در غیر این صورت False خواهد بود
            message پیام مرتبط خصوصا در صورت وقوع خطا نشان می دهد که چه خطایی رخ داده است
    
    """
    current_user_national_code = get_current_user(request)
    obj_form_manager = FormManager(current_user_national_code=current_user_national_code, request_id=-1)
    result = obj_form_manager.task_management(request_id, task_id, operation_type, 'R')
    return JsonResponse(result)


def request_task_user_management(request, request_task_id:int)-> dict:
    """
    این تابع تسک های ذیل یک درخواست را مدیریت می کند.

    Args:
        request (_type_): درخواست http
        request_id (int): شناسه درخواست مورد نظر
                    
    Return value:
        یک  جسیون مشابه به مورد زیر شامل این اطلاعات:
            {'success':, 'message':''}
            success: در صورتی که اجرا موفقیت آمیز باشد برابر با True و در غیر این صورت False خواهد بود
            message پیام مرتبط خصوصا در صورت وقوع خطا نشان می دهد که چه خطایی رخ داده است
    
    """
    current_user_national_code = get_current_user(request)
    # اطلاعات را از ورودی دریافت می کنیم
    operation_type = request.POST.get('operation_type', 'A')
    user_national_code = request.POST.get('user_national_code','')
    user_role_id = int(request.POST.get('role_id', -1))
    user_team_code = request.POST.get('team_code', '')
    user_role_code = request.POST.get('role_code', 'E')
        
    obj_form_manager = FormManager(current_user_national_code=current_user_national_code, request_id=-1)
    result = obj_form_manager.task_user_management(request_task_id, operation_type, user_national_code,user_role_id, user_team_code, user_role_code, 'R')
    return JsonResponse(result)


def change_type_notify_group_management(request, change_type_id:int, operation_type:str, notify_group_id:int)-> dict:
    """
    این تابع گروه های اطلاع رسانی ذیل یک نوع درخواست را مدیریت می کند.

    Args:
        request (_type_): درخواست http
        notify_group_id (int): شناسه تسک مورد نظر 
        change_type_id (int): شناسه نوع درخواست
        operation_type (_type_): یکی از موارد زیر است:
            A: برای اضافه کردن
            D: برای حذف کردن
    Return value:
        یک  جسیون مشابه به مورد زیر شامل این اطلاعات:
            {'success':, 'message':''}
            success: در صورتی که اجرا موفقیت آمیز باشد برابر با True و در غیر این صورت False خواهد بود
            message پیام مرتبط خصوصا در صورت وقوع خطا نشان می دهد که چه خطایی رخ داده است
    
    """
    
    current_user_national_code = get_current_user(request)
    obj_form_manager = FormManager(current_user_national_code=current_user_national_code, request_id=-1)
    result = obj_form_manager.notify_group_managment(change_type_id, notify_group_id, operation_type, 'C')
    return JsonResponse(result)



def change_type_task_management(request, change_type_id:int, operation_type:str, task_id:int)-> dict:
    """
    این تابع تسک های ذیل یک نوع درخواست را مدیریت می کند.

    Args:
        request (_type_): درخواست http
        task_id (int): شناسه تسک مورد نظر 
        change_type_id (int): شناسه نوع درخواست
        operation_type (_type_): یکی از موارد زیر است:

    Return value:
        یک  جسیون مشابه به مورد زیر شامل این اطلاعات:
            {'success':, 'message':''}
            success: در صورتی که اجرا موفقیت آمیز باشد برابر با True و در غیر این صورت False خواهد بود
            message پیام مرتبط خصوصا در صورت وقوع خطا نشان می دهد که چه خطایی رخ داده است
    
    """
    
    current_user_national_code = get_current_user(request)
    obj_form_manager = FormManager(current_user_national_code=current_user_national_code, request_id=-1)
    result = obj_form_manager.task_management(change_type_id, task_id, operation_type, 'C')
    return JsonResponse(result)


def change_type_user_management(request, change_type_id:int)-> dict:
    """
    این تابع افراد ذیل یک تسک را مدیریت می کند.

    Args:
        request (_type_): درخواست http
        change_type_id (int): شناسه مورد درخواست
                    
    Return value:
        یک  جسیون مشابه به مورد زیر شامل این اطلاعات:
            {'success':, 'message':''}
            success: در صورتی که اجرا موفقیت آمیز باشد برابر با True و در غیر این صورت False خواهد بود
            message پیام مرتبط خصوصا در صورت وقوع خطا نشان می دهد که چه خطایی رخ داده است
    
    """
    
    current_user_national_code = get_current_user(request)

    # اطلاعات را از ورودی دریافت می کنیم
    operation_type = request.POST.get('operation_type', 'A')
    user_national_code = request.POST.get('user_national_code','')
    user_role_id = request.POST.get('role_id', -1)
    user_team_code = request.POST.get('team_code', '')
    user_role_code = request.POST.get('role_code', 'E')
    
    # ########################################داده تستی باید اصلاح شود
    task_id = 1
    
    obj_form_manager = FormManager(current_user_national_code=current_user_national_code, request_id=-1)
    result = obj_form_manager.task_user_management(task_id, operation_type, user_national_code,user_role_id, user_team_code, user_role_code, 'C')
    return JsonResponse(result)


def change_type_list(request):
    current_user_nationalcode =  get_current_user(request)
    from . import models as m
    change_type_list = m.ChangeType.objects.all()
    data={'change_type_list':change_type_list}
    return render(request, 'ConfigurationChangeRequest/change-type-list.html', data)

def change_type_create(request):
    pass

def change_type_edit(request, change_type_id):
    current_user = get_current_user(request)
   
    obj_change_type = ChangeType(current_user, change_type_id)
    data=obj_change_type.load_record_data(current_user)
    
    return render(request, 'ConfigurationChangeRequest/change-type.html', data)

    
def request_action_view(request, request_id, action):
    """
    عملیات روی درخواست (تایید/رد/بازگشت)
    """
    current_user_nationalcode =  get_current_user(request)
    request_obj = Request(current_user_national_code=current_user_nationalcode, request_id=request_id)
    
    if request.method == 'POST':
        form_data = request.POST.dict()
        result = request_obj.next_step(action, current_user_nationalcode, form_data)
        
        if result['success']:
            return JsonResponse({'success': True, 'message': result['message']})
        else:
            return JsonResponse({'success': False, 'message': result['message']})
    
    return JsonResponse({'success': False, 'message': 'امکان انجام عملیات مربوطه وجود ندارد'})

def task_action_view(request, request_id, task_id, action):
    """
    عملیات روی تسک (تایید/رد/بازگشت)
    """
    current_user_nationalcode = get_current_user(request=request)
    request_obj = Request(current_user_national_code=current_user_nationalcode, request_id=request_id)
    
    if request.method == 'POST':
        form_data = request.POST.dict()
        result = request_obj.task_action(task_id, action, current_user_nationalcode, form_data)
        
        if result['success']:
            return JsonResponse({'success': True, 'message': result['message']})
        else:
            return JsonResponse({'success': False, 'message': result['message']})
    
    return JsonResponse({'success': False, 'message': 'متد نامعتبر'})

def request_view_view(request, request_id):
    """
    مشاهده درخواست (فقط خواندنی)
    """
    current_user_nationalcode =  get_current_user(request)
    form_manager= FormManager( current_user_nationalcode)
    
    # بارگذاری داده‌های درخواست
    data = form_manager.load_form_data(request_id, current_user_nationalcode)
    return render(request, 'ConfigurationChangeRequest/request-view.html', data)


def test_messages_view(request):
    data = {'message':'این یک پیام خطا است',
            'success_message':'این پیام موفقیت آمیز است',
            'warning_message':'این یک پیام هشدار است',
            }
    return render(request, 'ConfigurationChangeRequest/test-message.html', data)


