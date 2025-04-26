from django.shortcuts import render, redirect
from . import business as b
from django.http import JsonResponse
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def insert_request(request):
    current_user_nationalcode = '1280419180'
    data = b.load_form_data(-1, current_user_nationalcode)

    return render(request, 'ConfigurationChangeRequest/request.html', data)

def next_step(request, request_id:int, action:str):
    """
    این تابع برای پیشبرد مرحله درخواست استفاده می‌شود.

    پارامترها:
    request (HttpRequest): درخواست HTTP
    request_id (int): شناسه درخواست
    action (str): نوع اقدام که می‌تواند یکی از مقادیر زیر باشد:
        CON: تایید
        RET: بازگشت
        REJ: رد
    """
    # erfan
    # در این قسمت کاربر جاری را دریافت می کنیم
    current_user_nationalcode = '1280419180'
    # current_user_nationalcode = '1379150728'
    # current_user_nationalcode = '1280419180'
    if request.method == 'POST':
        form_data = {}  # دیکشنری برای ذخیره داده‌های فرم
        form_data['reject_reason'] = request.POST.get('reject_reason') 
    
        try:
            return_json = b.next_step(request_id, current_user_nationalcode, action, form_data)
            return JsonResponse(return_json)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
        
    return  JsonResponse({'success': False, 'errors': 'خطا در نحوه ارسال اطلاعات'})

def view_request(request, request_id:int):
    # erfan
    current_user = '1280419180'
    manager_user = '1379150728'
    # current_user = manager_user
    form_data = b.load_form_data(request_id=request_id, user_nationalcode=current_user )
    # اگر در مرحله تست و یا اجرا باشد، باید اطلاعات تکمیلی نیز نمایش داده شود
    if form_data['request'].status_code in ['EXECUT','TESTER']:
        return render(request, 'ConfigurationChangeRequest/request-other-step.html', form_data)
    
    return render(request, 'ConfigurationChangeRequest/request-readonly.html', form_data)
def submit_request(request, request_id:int):

    
    if request.method == 'POST':
        form_data = {}  # دیکشنری برای ذخیره داده‌های فرم

        # اطلاعات فرم
        form_data['request_id'] = request_id  # شناسه درخواست
        #*******************************صفحه اول*****************************
        #################################سطر اول#############################
        #-----------------------------قسمت اول-----------------------------
        # اطلاعات کاربران
        form_data['requestor_user_nationalcode'] = request.POST.get('requestor_user_nationalcode')  # کد ملی ایجاد کننده درخواست
        # سمت و تیم کاربر در قالب یک متغییر بازگشت داده می شود.
        # CAR-73 : یعنی تیم خودرو و سمتی که شناسه آن 73 است
        utr = request.POST.get('requestor_user_team_role')
        form_data['requestor_user_team'] = b.get_team_role('T',utr)  #تیم  ایجاد کننده درخواست
        form_data['requestor_user_role'] = b.get_team_role('R', utr)  # سمت ایجاد کننده درخواست

        form_data['executor_user_nationalcode'] = request.POST.get('executor_user_nationalcode')  # کد ملی مجری
        # سمت و تیم کاربر در قالب یک متغییر بازگشت داده می شود.
        # CAR-73 : یعنی تیم خودرو و سمتی که شناسه آن 73 است
        utr = request.POST.get('executor_user_team_role')
        form_data['executor_user_team'] = b.get_team_role('T', utr)  #تیم  مجری
        form_data['executor_user_role'] = b.get_team_role('R', utr)  # سمت مجری

        form_data['tester_user_nationalcode'] = request.POST.get('tester_user_nationalcode')  # کد ملی تستر
        # سمت و تیم کاربر در قالب یک متغییر بازگشت داده می شود.
        # CAR-73 : یعنی تیم خودرو و سمتی که شناسه آن 73 است
        utr = request.POST.get('tester_user_team_role')
        form_data['tester_user_team'] = b.get_team_role('T', utr)  #تیم  تستر
        form_data['tester_user_role'] = b.get_team_role('R', utr)  # سمت تستر

        form_data['need_test'] = request.POST.get('need_test') == '1'  # نیاز به تست (Boolean)

        #-----------------------------قسمت دوم-----------------------------
        # ویژگی های تغییر
        form_data['classification'] = request.POST.get('classification')  # طبقه‌بندی
        form_data['change_level'] = request.POST.get('change_level')  # سطح تغییر
        form_data['priority'] = request.POST.get('priority')  # اولویت
        form_data['risk_level'] = request.POST.get('risk_level')  # سطح ریسک
        

        #################################سطر دوم#############################
        #-----------------------------قسمت اول-----------------------------
        # اطلاعات تغییر
        form_data['change_title'] = request.POST.get('change_title')  # عنوان تغییر
        form_data['change_description'] = request.POST.get('change_description')  # توضیحات تغییر
        form_data['change_type'] = request.POST.get('change_type')  # عنوان تغییر

        # محل تغییر
        form_data['change_location_data_center'] = request.POST.get('change_location_data_center') == 'true'  # محل تغییر: مرکز داده (Boolean)
        # دریافت چک باکس‌های داینامیک برای DataCenter
        extra_information = b.get_dynamic_checkbox('DataCenter', request)
        # اطمینان از اینکه extra_information یک لیست است
        if not isinstance(form_data.get('extra_information'), list):
            form_data['extra_information'] = []
        form_data['extra_information'].extend(extra_information)                    
        
        form_data['change_location_database'] = request.POST.get('change_location_database') == 'true'  # محل تغییر: پایگاه داده (Boolean)
        form_data['change_location_systems'] = request.POST.get('change_location_systems') == 'true'  # محل تغییر: سیستم‌ها (Boolean)
        # دریافت چک باکس‌های داینامیک برای SystemsServices
        extra_information = b.get_dynamic_checkbox('SystemsServices', request)
        # اطمینان از اینکه extra_information یک لیست است
        if not isinstance(form_data.get('extra_information'), list):
            form_data['extra_information'] = []
        form_data['extra_information'].extend(extra_information)                    

        form_data['change_location_other'] = request.POST.get('change_location_other') == 'true'  # محل تغییر: سایر (Boolean)
        form_data['change_location_other_description'] = request.POST.get('change_location_other_description')  # توضیحات محل تغییر

        #-----------------------------قسمت دوم-----------------------------
        # دامنه تغییرات
        form_data['need_committee'] = request.POST.get('need_committee') == '1'  # نیاز به کمیته (Boolean)
        form_data['committee'] = request.POST.get('committee')  # کمیته انتخاب شده
        form_data['domain'] = request.POST.get('domain')  # دامنه تغییر

        # دریافت چک باکس‌های داینامیک برای تیم‌ها
        form_data['teams'] = b.get_selected_items('t', request)

        # دریافت چک باکس‌های داینامیک برای شرکت‌ها
        form_data['corps'] = b.get_selected_items('c', request)

        #*******************************صفحه دوم*****************************
        #################################سطر اول#############################
        #-----------------------------قسمت اول-----------------------------
        # زمانبندی تغییرات
        form_data['changing_duration_hour'] = int(request.POST.get('duration_hour', 0))  # ساعت مدت زمان تغییرات
        form_data['changing_duration_minute'] = int(request.POST.get('duration_minute', 0))  # دقیقه مدت زمان تغییرات
        form_data['downtime_duration_hour'] = int(request.POST.get('estimate_downtime_hour', 0))  # ساعت مدت زمان توقف
        form_data['downtime_duration_minute'] = int(request.POST.get('estimate_downtime_minute', 0))  # دقیقه مدت زمان توقف
        form_data['downtime_duration_worstcase_hour'] = int(request.POST.get('worstcase_downtime_hour', 0))  # ساعت بدترین مدت زمان توقف
        form_data['downtime_duration_worstcase_minute'] = int(request.POST.get('worstcase_downtime_minute', 0))  # دقیقه بدترین مدت زمان توقف
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
        form_data['manager_opinion'] = request.POST.get('manager_opinion')
        form_data['manager_reject_description'] = request.POST.get('manager_reject_description')

        # اعتبارسنجی فرم
        errors = b.form_validation(form_data)
        if errors:
            # اگر خطا وجود داشت، آن را به همراه success برابر با false برگردانید
            return JsonResponse({'success': False, 'errors': errors})

        try:
            # ذخیره فرم
            request_id = b.save_form(form_data)

            # برگرداندن موفقیت‌آمیز بودن عملیات
            return JsonResponse({'success': True, 'request_id': request_id})

        except Exception as e:
            # در صورت بروز خطا، پیام خطا را به JsonResponse اضافه کنید
            return JsonResponse({'success': False, 'errors': str(e)})


    return  JsonResponse({'success': False, 'errors': 'خطا در نحوه ارسال اطلاعات'})