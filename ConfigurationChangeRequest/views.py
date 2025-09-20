from django.shortcuts import render, redirect
from .business import Request, FormManager
from django.http import JsonResponse
import logging
import json
import inspect

requestor = '1280419180'
manager = '1379150728'
rel_manger = '0081578091'
commitee = '5228300880'
executor = '6309920952'
tester = '0063425750'
current_user = requestor

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# def insert_request(request):
#     current_user_nationalcode = current_user
#     data = b.load_form_data(-1, current_user_nationalcode)

#     return render(request, 'ConfigurationChangeRequest/request.html', data)


# def next_step(request, request_id:int, action:str):
#     """
#     این تابع برای پیشبرد مرحله درخواست استفاده می‌شود.

#     پارامترها:
#     request (HttpRequest): درخواست HTTP
#     request_id (int): شناسه درخواست
#     action (str): نوع اقدام که می‌تواند یکی از مقادیر زیر باشد:
#         CON: تایید
#         RET: بازگشت
#         REJ: رد
#     """
#     # erfan
#     # در این قسمت کاربر جاری را دریافت می کنیم
#     current_user_nationalcode = current_user

#     if request.method == 'POST':
#         form_data = {}  # دیکشنری برای ذخیره داده‌های فرم
#         form_data['reject_reason'] = request.POST.get('reject_reason') 
#         form_data['operation_result'] = request.POST.get('operation_result')
#         form_data['operation_date'] = request.POST.get('operation_date')
#         form_data['operation_time'] = request.POST.get('operation_time')
#         form_data['operation_report'] = request.POST.get('operation_report')
#         form_data['operation_result'] = request.POST.get('operation_result')
        
#         form_data['changing_duration_actual_hour'] = request.POST.get('changing_duration_actual_hour')
#         form_data['changing_duration_actual_minute'] = request.POST.get('changing_duration_actual_minute')
#         form_data['downtime_duration_actual_hour'] = request.POST.get('downtime_duration_actual_hour')
#         form_data['downtime_duration_actual_minute'] = request.POST.get('downtime_duration_actual_minute')

#         # اعتبارسنجی و ذخیره مقادیر عددی
#         try:
#             return_json = b.next_step(request_id, current_user_nationalcode, action, form_data)
#             return JsonResponse(return_json)
#         except Exception as e:
#             return JsonResponse({'success': False, 'message': str(e)})
        
#     return  JsonResponse({'success': False, 'errors': 'خطا در نحوه ارسال اطلاعات'})

# def view_request(request, request_id:int):
#     # erfan
#     form_data = b.load_form_data(request_id=request_id, user_nationalcode=current_user )
#     if not form_data['message']: 
#         # اگر در مرحله تست و یا اجرا باشد، باید اطلاعات تکمیلی نیز نمایش داده شود
#         if form_data['request'].status_code in ['EXECUT','TESTER'] and form_data['status'] != 'READONLY':
#             return render(request, 'ConfigurationChangeRequest/request-other-step.html', form_data)
    
#         return render(request, 'ConfigurationChangeRequest/request-readonly.html', form_data)
#     else:
#         return render(request, 'ConfigurationChangeRequest/request.html', form_data)
        
# def submit_request(request, request_id:int):

    
#     if request.method == 'POST':
#         form_data = {}  # دیکشنری برای ذخیره داده‌های فرم

#         # اطلاعات فرم
#         form_data['request_id'] = request_id  # شناسه درخواست
#         #*******************************صفحه اول*****************************
#         #################################سطر اول#############################
#         #-----------------------------قسمت اول-----------------------------
#         # اطلاعات کاربران
#         form_data['requestor_user_nationalcode'] = request.POST.get('requestor_user_nationalcode')  # کد ملی ایجاد کننده درخواست
#         # سمت و تیم کاربر در قالب یک متغییر بازگشت داده می شود.
#         # CAR-73 : یعنی تیم خودرو و سمتی که شناسه آن 73 است
#         utr = request.POST.get('requestor_user_team_role')
#         form_data['requestor_user_team'] = b.get_team_role('T',utr)  #تیم  ایجاد کننده درخواست
#         form_data['requestor_user_role'] = b.get_team_role('R', utr)  # سمت ایجاد کننده درخواست

#         form_data['executor_user_nationalcode'] = request.POST.get('executor_user_nationalcode')  # کد ملی مجری
#         # سمت و تیم کاربر در قالب یک متغییر بازگشت داده می شود.
#         # CAR-73 : یعنی تیم خودرو و سمتی که شناسه آن 73 است
#         utr = request.POST.get('executor_user_team_role')
#         form_data['executor_user_team'] = b.get_team_role('T', utr)  #تیم  مجری
#         form_data['executor_user_role'] = b.get_team_role('R', utr)  # سمت مجری

#         form_data['tester_user_nationalcode'] = request.POST.get('tester_user_nationalcode')  # کد ملی تستر
#         # سمت و تیم کاربر در قالب یک متغییر بازگشت داده می شود.
#         # CAR-73 : یعنی تیم خودرو و سمتی که شناسه آن 73 است
#         utr = request.POST.get('tester_user_team_role')
#         form_data['tester_user_team'] = b.get_team_role('T', utr)  #تیم  تستر
#         form_data['tester_user_role'] = b.get_team_role('R', utr)  # سمت تستر

#         form_data['need_test'] = request.POST.get('need_test') == '1'  # نیاز به تست (Boolean)

#         #-----------------------------قسمت دوم-----------------------------
#         # ویژگی های تغییر
#         form_data['classification'] = request.POST.get('classification')  # طبقه‌بندی
#         form_data['change_level'] = request.POST.get('change_level')  # سطح تغییر
#         form_data['priority'] = request.POST.get('priority')  # اولویت
#         form_data['risk_level'] = request.POST.get('risk_level')  # سطح ریسک
        

#         #################################سطر دوم#############################
#         #-----------------------------قسمت اول-----------------------------
#         # اطلاعات تغییر
#         form_data['change_title'] = request.POST.get('change_title')  # عنوان تغییر
#         form_data['change_description'] = request.POST.get('change_description')  # توضیحات تغییر
#         form_data['change_type'] = request.POST.get('change_type')  # عنوان تغییر

#         # محل تغییر
#         form_data['change_location_data_center'] = request.POST.get('change_location_data_center') == 'true'  # محل تغییر: مرکز داده (Boolean)
#         # دریافت چک باکس‌های داینامیک برای DataCenter
#         extra_information = b.get_dynamic_checkbox('DataCenter', request)
#         # اطمینان از اینکه extra_information یک لیست است
#         if not isinstance(form_data.get('extra_information'), list):
#             form_data['extra_information'] = []
#         form_data['extra_information'].extend(extra_information)                    
        
#         form_data['change_location_database'] = request.POST.get('change_location_database') == 'true'  # محل تغییر: پایگاه داده (Boolean)
#         form_data['change_location_systems'] = request.POST.get('change_location_systems') == 'true'  # محل تغییر: سیستم‌ها (Boolean)
#         # دریافت چک باکس‌های داینامیک برای SystemsServices
#         extra_information = b.get_dynamic_checkbox('SystemsServices', request)
#         # اطمینان از اینکه extra_information یک لیست است
#         if not isinstance(form_data.get('extra_information'), list):
#             form_data['extra_information'] = []
#         form_data['extra_information'].extend(extra_information)                    

#         form_data['change_location_other'] = request.POST.get('change_location_other') == 'true'  # محل تغییر: سایر (Boolean)
#         form_data['change_location_other_description'] = request.POST.get('change_location_other_description')  # توضیحات محل تغییر

#         #-----------------------------قسمت دوم-----------------------------
#         # دامنه تغییرات
#         form_data['need_committee'] = request.POST.get('need_committee') == '1'  # نیاز به کمیته (Boolean)
#         form_data['committee'] = request.POST.get('committee')  # کمیته انتخاب شده
#         form_data['domain'] = request.POST.get('domain')  # دامنه تغییر

#         # دریافت چک باکس‌های داینامیک برای تیم‌ها
#         form_data['teams'] = b.get_selected_items('t', request)

#         # دریافت چک باکس‌های داینامیک برای شرکت‌ها
#         form_data['corps'] = b.get_selected_items('c', request)

#         #*******************************صفحه دوم*****************************
#         #################################سطر اول#############################
#         #-----------------------------قسمت اول-----------------------------
#         # زمانبندی تغییرات
#         form_data['changing_duration_hour'] = int(request.POST.get('duration_hour', 0))  # ساعت مدت زمان تغییرات
#         form_data['changing_duration_minute'] = int(request.POST.get('duration_minute', 0))  # دقیقه مدت زمان تغییرات
#         form_data['downtime_duration_hour'] = int(request.POST.get('estimate_downtime_hour', 0))  # ساعت مدت زمان توقف
#         form_data['downtime_duration_minute'] = int(request.POST.get('estimate_downtime_minute', 0))  # دقیقه مدت زمان توقف
#         form_data['downtime_duration_worstcase_hour'] = int(request.POST.get('worstcase_downtime_hour', 0))  # ساعت بدترین مدت زمان توقف
#         form_data['downtime_duration_worstcase_minute'] = int(request.POST.get('worstcase_downtime_minute', 0))  # دقیقه بدترین مدت زمان توقف
#         form_data['change_date'] = request.POST.get('request_date')  # تاریخ تغییر
#         form_data['change_time'] = request.POST.get('request_time')  # تاریخ تغییر
#         # ############################تست تاریخ شمسی#####################

        
        
        
#         #-----------------------------قسمت دوم-----------------------------
#         # حوزه اثرگذاری تغییر
#         form_data['stop_critical_service'] = request.POST.get('ImpactOnCriticalService') == 'true'  # توقف خدمات بحرانی (Boolean)
#         form_data['critical_service_title'] = request.POST.get('ImpactOnCriticalServiceDescription')  # عنوان خدمات بحرانی
#         form_data['stop_sensitive_service'] = request.POST.get('ImpactOnSensitiveService') == 'true'  # توقف خدمات حساس (Boolean)
#         form_data['stop_service_title'] = request.POST.get('ImpactOnSensitiveServiceDescription')  # عنوان خدمات متوقف شده
#         form_data['not_stop_any_service'] = request.POST.get('ImpactNotOnAnyService') == 'true'  # عدم توقف هیچ خدماتی (Boolean)

#         #################################سطر دوم#############################
#         #-----------------------------قسمت اول-----------------------------
#         # الزام تغییرات
#         form_data['reason_regulatory'] = request.POST.get('ReasonRegulatory') == 'true'  # الزام قانونی (Boolean)
#         form_data['reason_technical'] = request.POST.get('ReasonTechnical') == 'true'  # الزام فنی (Boolean)
#         form_data['reason_security'] = request.POST.get('ReasonSecurity') == 'true'  # الزام امنیتی (Boolean)
#         form_data['reason_business'] = request.POST.get('ReasonBusiness') == 'true'  # الزام کسب و کاری (Boolean)
#         form_data['reason_other'] = request.POST.get('ReasonOther') == 'true'  # سایر الزامات (Boolean)
#         form_data['reason_other_description'] = request.POST.get('ReasonOtherDescription')  # توضیحات الزامات دیگر


#         #-----------------------------قسمت دوم-----------------------------
#         # طرح بازگشت
#         form_data['has_role_back_plan'] = request.POST.get('Rollback') == '1'  # وجود برنامه بازگشت (Boolean)
#         form_data['role_back_plan_description'] = request.POST.get('RollbackPlan')  # توضیحات برنامه بازگشت

#         #---------------------------نظرم مدیر---------------------------------
#         form_data['manager_opinion'] = request.POST.get('manager_opinion')
#         form_data['manager_reject_description'] = request.POST.get('manager_reject_description')

#         # اعتبارسنجی فرم
#         errors = b.form_validation(form_data)
#         if errors:
#             # اگر خطا وجود داشت، آن را به همراه success برابر با false برگردانید
#             return JsonResponse({'success': False, 'errors': errors})

#         try:
#             # ذخیره فرم
#             request_id = b.save_form(form_data)

#             # برگرداندن موفقیت‌آمیز بودن عملیات
#             return JsonResponse({'success': True, 'request_id': request_id})

#         except Exception as e:
#             # در صورت بروز خطا، پیام خطا را به JsonResponse اضافه کنید
#             return JsonResponse({'success': False, 'errors': str(e)})


#     return  JsonResponse({'success': False, 'errors': 'خطا در نحوه ارسال اطلاعات'})

# def call_function_view(request, function_name):
#     if request.method == 'POST':
#         params = json.loads(request.body)
#         function = getattr(__import__('ConfigurationChangeRequest.business', fromlist=['']), function_name, None)
#         if function:
#             output = function(**params)  # فراخوانی تابع با پارامترها
#             return JsonResponse({'output': output})
#     return JsonResponse({'output': 'Invalid function or parameters.'})

# def function_test_view(request):
#     functions = {name: func for name, func in inspect.getmembers(__import__('ConfigurationChangeRequest.business', fromlist=['']), inspect.isfunction)}
#     function_params = {name: list(inspect.signature(func).parameters.keys()) for name, func in functions.items()}
#     return render(request, 'ConfigurationChangeRequest/test.html', {'functions': functions, 'function_params': json.dumps(function_params)})

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
    current_user_nationalcode = current_user
    request_id = int(request.POST.get('request_id')) if request.POST.get('request_id') else -1

    # یک نمونه از شی فرم ایجاد می کنیم
    objFormManager = FormManager(request_id=request_id)



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

def get_full_form_data(request):
    # دریافت اطلاعات فرم ساده
    form_data = get_simple_form_data(request=request)
    objFormManager :FormManager= form_data['objFormManager']  # اصلاح: استفاده از [] به جای ()
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
    form_data['change_location_data_center'] = request.POST.get('change_location_data_center') == 'true'  # محل تغییر: مرکز داده (Boolean)
    # دریافت چک باکس‌های داینامیک برای DataCenter
    extra_information = objFormManager.get_dynamic_checkbox('DataCenter', request)
    # اطمینان از اینکه extra_information یک لیست است
    if not isinstance(form_data.get('extra_information'), list):
        form_data['extra_information'] = []
    form_data['extra_information'].extend(extra_information)                    
    
    form_data['change_location_database'] = request.POST.get('change_location_database') == 'true'  # محل تغییر: پایگاه داده (Boolean)
    form_data['change_location_systems'] = request.POST.get('change_location_systems') == 'true'  # محل تغییر: سیستم‌ها (Boolean)
    # دریافت چک باکس‌های داینامیک برای SystemsServices
    extra_information = objFormManager.get_dynamic_checkbox('SystemsServices', request)
    # اطمینان از اینکه extra_information یک لیست است
    if not isinstance(form_data.get('extra_information'), list):
        form_data['extra_information'] = []
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
    current_user_nationalcode = current_user
    form_manager = FormManager()
    
    if request.method == 'POST':
        # دریافت اطلاعات فرم
        form_data = get_simple_form_data(request=request)
        
        # اعتبارسنجی فرم
        validation_result = form_manager.form_validation(form_data)
        
        if validation_result['success']:
            # ایجاد درخواست
            request_obj = Request(-1)
            result = request_obj.create_request(form_data, current_user_nationalcode)
            
            if result['success']:
                return JsonResponse({
                    'success': True, 
                    'request_id': result['request_id'],
                    'message': 'درخواست تغییر با موفقیت ایجاد شد و برای بررسی مدیر ارسال گردید'
                })
            else:
                return JsonResponse({'success': False, 'message': result['message']})
        else:
            return JsonResponse({'success': False, 'message': validation_result['message']})
    
    # بارگذاری داده‌های فرم
    data = form_manager.load_form_data(-1, current_user_nationalcode)
    return render(request, 'ConfigurationChangeRequest/request-simple.html', data)

def request_view(request, request_id):
    """
    برای مشاهده فرم درخواست از این تابع استفاده می شود

    Args:
        request (request): اطلاعات درخواست http
        request_id (int): شناسه درخواست
    """
    current_user_nationalcode = current_user
    data = {}

    # ابتدا یک نمونه از شی درخواست ایجاد می کنیم
    request_obj = Request(request_id=request_id)    
    
    # اگر چنین درخواستی وجود نداشته باشد، باید پیام خطا به کاربر بدهیم
    if request_obj.request_id is None or request_obj.request_id < 0:
        return render(request, 'ConfigurationChangeRequest/404.html', data)    
    
    if request_obj.error_message:
        return JsonResponse({'success': False, 'message': request_obj.error_message})
    
    # اگر درخواست معتبر باشد، باید بررسی کنیم که کدام فرم باید برای این کاربر باز شود
    form_manager = FormManager(request_id=request_id)   
    result = form_manager.check_form_status(user_nationalcode=current_user_nationalcode, request_id=request_id)
    
    # وضعیت فرم را به دست می آوریم. وضعیت پیش فرض درج است
    mode = result.get('mode', 'INSERT')
    # نوع فرم را به دست می آوریم، نوع پیش فرض، درخواست ساده است
    form = result.get('form', 'RequestSimple')
    
    # اگر وضعیت درج باشد، آنگاه باید به صفحه اصلی هدایت شویم
    if mode == 'INSERT':
        return request_create(request=request)
    
 
     
    if mode == 'UPDATE':
        data['mode'] = 'UPDATE'
    else:
        data['mode'] = 'READONLY'
    
    # اگر حالت به روزرسانی باشد
    # و داده های جدید ارسال شده باشند
    if request.method == 'POST':
        # دریافت اطلاعات فرم
        if form == "RequestSimple":
            form_data = get_simple_form_data(request=request)
        elif form == "RequestFull":
            form_data = get_full_form_data(request=request)      
            
        # چون الان در حالت ویرایش هستیم، باید شناسه درخواست را هم اضافه کنیم
        form_data['request_id'] = request_id 
        
        # اعتبارسنجی فرم
        validation_result = form_manager.form_validation(form_data)
        if validation_result['success']:
            # ایجاد درخواست
            request_obj = Request(request_id=request_id)
            # اطلاعات جدید درخواست به روزرسانی می شود
            result = request_obj.update_request(form_data, current_user_nationalcode)
            
            if result['success']:
                # فرم باید به مرحله بعد ارسال شود
                result = request_obj.next_step(
                    action_code=form_data.get('action', 'CON'), user_nationalcode=current_user_nationalcode
                )                    
                if result['success']:
                    return JsonResponse({
                        'success': True, 
                        'request_id': request_id,
                        'message': 'اطلاعات با موفقیت ذخیره شد'
                    })
                else:
                    return JsonResponse({'success': False, 'message': result['message']})        

            else:
                return JsonResponse({'success': False, 'message': result['message']})        
        
        
    # بارگذاری داده‌های فرم
    data = form_manager.load_form_data(request_id, current_user_nationalcode)    

    # اگر فرم درخواست ساده باشد
    if form == 'RequestSimple':
        return render(request, 'ConfigurationChangeRequest/request-simple.html', data)

    # اگر فرم درخواست کامل باشد
    elif form == 'RequestFull':
        return request_full_view(request, request_id, data)
    
    # اگر فرم انتخاب تسک باشد
    elif form == 'TaskSelect':
        return task_select_view(request, request_id, task_id)
    
    # اگر فرم گزارش تسک باشد
    elif form == 'TaskReport':
        return task_report_view(request, request_id, task_id)
    
    # در غیر این صورت، فرم پیش‌فرض برای ایجاد درخواست بارگذاری می شود
    return request_create(request)


def request_full_view(request, request_id, data):
    """
    فرم درخواست کامل (مرحله دوم)
    """
    current_user_nationalcode = current_user
    form_manager = FormManager()
    
    if request.method == 'POST':
        # دریافت اطلاعات فرم کامل
        form_data = request.POST.dict()
        form_data['request_id'] = request_id
        
        # اعتبارسنجی فرم
        validation_result = form_manager.form_validation(form_data)
        
        if validation_result['success']:
            # به‌روزرسانی درخواست
            request_obj = Request(request_id)
            result = request_obj.update_request(form_data)
            
            if result['success']:
                return JsonResponse({'success': True, 'message': 'درخواست با موفقیت به‌روزرسانی شد'})
            else:
                return JsonResponse({'success': False, 'message': result['message']})
        else:
            return JsonResponse({'success': False, 'message': validation_result['message']})
    
    # بارگذاری داده‌های فرم
    if not data:
        data = form_manager.load_form_data(request_id, current_user_nationalcode)
    
    # اضافه کردن لیست کاربران برای کومبو
    if 'all_users' in data:
        data['users'] = data['all_users']
    
    return render(request, 'ConfigurationChangeRequest/request-full.html', data)

def task_select_view(request, request_id, task_id):
    """
    انتخاب تسک (برای مجری/تستر)
    """
    current_user_nationalcode = current_user
    form_manager = FormManager()
    
    if request.method == 'POST':
        # انتخاب تسک
        request_obj = Request(request_id)
        result = request_obj.select_task(task_id, current_user_nationalcode)
        
        if result['success']:
            return JsonResponse({'success': True, 'message': 'تسک با موفقیت انتخاب شد'})
        else:
            return JsonResponse({'success': False, 'message': result['message']})
    
    # بارگذاری داده‌های تسک
    data = form_manager.load_task_data(request_id, task_id, current_user_nationalcode)
    return render(request, 'ConfigurationChangeRequest/task-select.html', data)

def task_report_view(request, request_id, task_id):
    """
    گزارش تسک (برای مجری/تستر)
    """
    current_user_nationalcode = current_user
    form_manager = FormManager()
    
    if request.method == 'POST':
        # دریافت گزارش تسک
        form_data = request.POST.dict()
        form_data['request_id'] = request_id
        form_data['task_id'] = task_id
        
        # اعتبارسنجی فرم
        validation_result = form_manager.validate_task_report(form_data)
        
        if validation_result['success']:
            # ذخیره گزارش تسک
            request_obj = Request(request_id)
            result = request_obj.save_task_report(task_id, form_data, current_user_nationalcode)
            
            if result['success']:
                return JsonResponse({'success': True, 'message': 'گزارش تسک با موفقیت ذخیره شد'})
            else:
                return JsonResponse({'success': False, 'message': result['message']})
        else:
            return JsonResponse({'success': False, 'message': validation_result['message']})
    
    # بارگذاری داده‌های تسک
    data = form_manager.load_task_data(request_id, task_id, current_user_nationalcode)
    return render(request, 'ConfigurationChangeRequest/task-report.html', data)

def request_action_view(request, request_id, action):
    """
    عملیات روی درخواست (تایید/رد/بازگشت)
    """
    current_user_nationalcode = current_user
    request_obj = Request(request_id)
    
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
    current_user_nationalcode = current_user
    request_obj = Request(request_id)
    
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
    current_user_nationalcode = current_user
    form_manager = FormManager()
    
    # بارگذاری داده‌های درخواست
    data = form_manager.load_form_data(request_id, current_user_nationalcode)
    return render(request, 'ConfigurationChangeRequest/request-view.html', data)


def test_messages_view(request):
    data = {'message':'این یک پیام خطا است',
            'success_message':'این پیام موفقیت آمیز است',
            'warning_message':'این یک پیام هشدار است',
            }
    return render(request, 'ConfigurationChangeRequest/test-message.html', data)
