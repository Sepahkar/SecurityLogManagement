from asyncio import current_task
import json
from random import choice
from collections import defaultdict
from django.core.signals import request_started
from django.db.transaction import commit
# from requests import request
from datetime import datetime

from urllib3 import request
import Utility

# from ConfigurationChangeRequest.views import commitee
from . import models as m
import jdatetime
from . import validator
from django.core.exceptions import ValidationError
from datetime import datetime
# from Utility.APIManager.Portal.register_document import v2 as register_document
# from Utility.APIManager.Portal.send_document import ver2 as send_document
# from Utility.APIManager.Portal.update_document_state_code import (
#     v1 as update_document_state_code,
# )
# from Utility.APIManager.Portal.terminate_flow import v1 as terminate_flow
# from Utility.APIManager.Portal.finish_flow import v1 as finish_flow

from Utility.APIManager.Notification.send_email import v1 as send_email
from Config import settings
from typing import List, Optional, Any
from django.db.models import QuerySet
from .singleton import singleton

APP_CODE = settings.APPCODE



class Cartable:
    doc_id: int=-1
    app_code: str=''
    doc_state: str=''

    def __init__(self) -> None:
        self.app_code = settings.APPCODE
        self.doc_id = -1

    def create_doc(
        self,
        doc_title: str,
        request_id: int,
        document_owner_national_code: str,
        priority: str = "NORMAL",
    ):
        """
        این تابع برای ایجاد یک سند استفاده می شود.

        Args:
            doc_title (str): عنوان سند مثلا : درخواست تغییرات سرورهای هورایزن
            request_id (int): شناسه درخواست تغییرات
            document_owner_national_code (str): کد ملی فرد درخواست دهنده
            priority (str, optional): اولویت درخواست، به صورت پیش فرض عادی است. Defaults to 'NORMAL'.
        """
        self.doc_id = 1

    def update_priority(self, new_priority):
        if not self.validate_doc():
            return {
                "success": False,
                "message": "قبل از به روزرسانی اولویت، سند باید ایجاد شده باشد",
            }
        # ... (سایر منطق تابع در صورت نیاز)
        return {"success": True, "message": "اولویت با موفقیت به‌روزرسانی شد"}

    def send_cartable(
        self,
        receiver: str,
        sender: str,
        new_doc_state: str = None,
        due_date: str = None,
    ):
        # اگر سند وجود نداشته باشد پیام خطا می دهد
        if not self.validate_doc():
            return {
                "success": False,
                "message": "قبل از ارسال، سند باید ایجاد شده باشد",
            }

        # ... (سایر منطق تابع در صورت نیاز)
        return {"success": True, "message": "سند با موفقیت ارسال شد"}

    def send_cartables(
        self, sender_receivers: [{}], new_doc_state: str = None, due_date: str = None
    ):
        # اگر سند وجود نداشته باشد پیام خطا می دهد
        if not self.validate_doc():
            return {
                "success": False,
                "message": "قبل از ارسال، سند باید ایجاد شده باشد",
            }

        results = []
        for item in sender_receivers:
            receiver = item.get("receiver")
            sender = item.get("sender")
            result = self.send_cartable(receiver, sender, new_doc_state, due_date)
            results.append(result)

        # اگر حتی یکی از ارسال‌ها موفق نباشد، پیام خطا بازگردانده می‌شود
        if not all(r.get("success") for r in results):
            failed_messages = [
                r.get("message") for r in results if not r.get("success")
            ]
            return {
                "success": False,
                "message": "برخی از ارسال‌ها با خطا مواجه شدند: "
                + "; ".join(failed_messages),
            }

        return {"success": True, "message": "سندها با موفقیت ارسال شدند"}

    def exit_from_cartable(
        self, national_code:str
    ):
        # اگر سند وجود نداشته باشد پیام خطا می دهد
        if not self.validate_doc():
            return {
                "success": False,
                "message": "قبل از خارج کردن سند از کارتابل باید ایجاد شده باشد",
            }
        # ... (سایر منطق تابع در صورت نیاز)
        return {"success": True, "message": "سند با موفقیت از کارتابل خارج شد"}

    def exit_from_all_cartables(
        self,
    ):
        # اگر سند وجود نداشته باشد پیام خطا می دهد
        if not self.validate_doc():
            return {
                "success": False,
                "message": "قبل از خارج کردن سند از کارتابل باید ایجاد شده باشد",
            }
        # ... (سایر منطق تابع در صورت نیاز)
        return {"success": True, "message": "سند با موفقیت از همه کارتابل‌ها خارج شد"}

    def validate_doc(self) -> bool:
        """
        این تابع بررسی می کند که آیا شناسه سند معتبر است یا خیر

        Returns:
            bool: در صورتی که شناسه سند وجود نداشته باشد یا معتبر نباشد، مقدار False و در غیر این صورت مقدار True بازگشت می دهد
        """
        # اگر هنوز سند ایجاد نشده باشد
        if not self.doc_id:
            return False
        return True
        # باید با فراخوانی یک API کنترل کنیم که سند وجود دارد


# @singleton
class FormManager:
    """
    این کلاس دربردارنده توابع عمومی برای مدیریت اطلاعات فرم هامی باشد

    Returns:
        FormManager obj: یک شی از کلاس مربوطه بازگشت می دهد
    """

    request_obj:"Request" = None
    error_message: str = None
    request_id: int = -1
    current_user_national_code:str=''

    def __init__(self,current_user_national_code:str, request_id: int = -1):
        self.current_user_national_code = current_user_national_code
        # از ایجاد Request در اینجا خودداری می‌کنیم تا وابستگی دوری ایجاد نشود
        self.request_obj = None
        self.error_message = None
        self.request_id = request_id if request_id and request_id > 0 else -1

    def __get_team_role(self, team_role: str, value: str):
        """
        این تابع کد سمت و تیم را که به صورت یک رشته جدا شده با - است را دریافت کرده و سمت و یا تیم مربوطه را بازگشت می دهد

        Args:
            team_role (str): در صورتی که هدف گرفتن تیم باشد باید کارکتر T و در صورتی که می خواهیم سمت را بازگشت دهیم کارکتر R را ارسال می کنیم
            value (str): این رشته شامل کد تیم - شناسه سمت است

        Returns:
            str: در صورت معتبر بودن مقادیر شناسه سمت و یا کد تیم را بازگشت می دهد در غیر این صورت مقدار None بازگشت می دهد
        """
        if "-" in value:
            if team_role == "T":
                return value.split("-")[0]
            elif team_role == "R":
                return int(value.split("-")[1])
        else:
            return None

        return None

    def __is_valid_string(self, s: str) -> bool:
        # حذف فاصله‌های اول و آخر و فاصله‌های وسط
        cleaned = s.strip()

        # شرط 1: حداقل طول 5 کاراکتر
        if len(cleaned) < 5:
            return False

        # شرط 2: همه کاراکترها نباید تکراری باشند
        if len(set(cleaned)) == 1:
            return False

        return True

    def __is_valid_integer(self, value):
        """بررسی می‌کند که آیا مقدار یک عدد صحیح معتبر است."""
        try:
            int_value = int(value)  # تبدیل به عدد صحیح
            return True, int_value  # اگر معتبر بود، True و مقدار عددی را برمی‌گرداند
        except ValueError:
            return False, None  # اگر نامعتبر بود، False و None را برمی‌گرداند

    def get_user_team_role(self, user_team_role):
        # استخراج تیم و سمت کاربر
        data = {"success": True, "message":""}
        user_team_role 
        if user_team_role:
            team_code = self.__get_team_role(
                "T", user_team_role
            )
            role_id = self.__get_team_role(
                "R", user_team_role
            )
        else:
            return {"success": False, "message": "کاربر تیم و سمت معتبری ندارد"}

        # تبدیل به انواع مناسب
        if team_code:
            team_code = str(team_code)  # team_code باید string باشد
        if role_id:
            role_id = int(role_id)  # role_id باید integer باشد        

        data.update(
            {
                "team_code":team_code,
                "role_id":role_id
            }
        )
        return data


    # این تابع بررسی می کند که با توجه به وضعیت فعلی سیستم، کدام فرم و در چه حالتی برای این کاربر باید به چه صورتی نمایش داده شود؟
    def check_form_status(
        self, user_nationalcode: str, request_id: int = -1 ) -> dict:
        """
        این تابع با توجه به کاربر جاری و شناسه درخواست، مشخص می کند که کدام فرم و در چه حالتی باید باز شود

        Args:
            user_nationalcode (str): کد ملی کاربر جاری
            request_id (int): شناسه درخواست

        Returns:
            _type_: دو مقدار را بازگشت می دهد، اولی کد وضعیت و دومی فرمی که باید باز شود قالب مقدار بازگشتی به این صورت است
            {'mode':'form_mode','form':'form_name'}
            mode:
                INSERT: فرم در حالت درج است
                READONLY: فرم در حالت فقط خواندنی است و امکان تغییر ندارد
                UPDATE: فرم در حالت به روزرسانی است
                INVALID: فرم معتیر نیست یا کاربر جاری اجازه مشاهده این درخواست را ندارد
            form:
                RequestSimple: فرم درخواست ساده، این فرم توسط درخواست دهنده و مدیر مستقیم قابل مشاهده است
                RequestFull: این فرم شامل همه اطلاعات بوده و توسط مدیر مربوطه و کاربر کمیته قابل مشاهده است
                TaskSelect: در این مرحله تستر و یا مجری تسک را انتخاب می کنند
                TaskReport: در این مرحله تستر و یا مجری تسک گزارش خود را وارد می کنند

        """

        # اگر شناسه درخواست نامعتبر باشد  در حالت درج باید باز شود
        if not self.request_id or request_id <= 0:
            return {"mode": "INSERT", "form": "RequestSimple"}

        # ایجاد یک شی درخواست
        request_obj:Request = Request(current_user_national_code=self.current_user_national_code, request_id=self.request_id)
        request_status = request_obj.status_code
        self.request_obj = request_obj
        # این متغییرها وضعیت و فرم را مشخص می کنند
        mode = "Readonly"
        form = "Invalid"

        # اینجا نوع فرم را بر اساس وضعیت فرم و کاربر جاری به دست می آوریم
        # موضوع این است که وقتی مثلا درخواست کننده با مدیر مربوطه یکسان باشد، قدری پیچیده می شود
        # در چنین مواردی اینکه تشخیص بدهیم که آیا باید فرم Simple را نشان بدهیم یا Full را
        # دشوار است
        
        # در چه صورتی فرم ساده باید نمایش داده شود؟
        # در صورتی که کاربر جاری درخواست دهنده و یا مدیر مستقیم باشد
        
        # با توجه به مقدار request_status وضعیت فرم و دسترسی کاربر را تعیین می‌کنیم
        # برای اینکه اشتباهی رخ ندهد، بهتر است این کار را بکنیم
        # به ازای هر وضعیت، بررسی زیر را انجام دهیم
        # 1- کاربر جاری را بررسی کنیم
        # 2- اگر کاربر باید به این فرم دسترسی به روزرسانی داشته باشد، به وی اجازه به روزرسانی بدهیم
        # 3- اگر کاربر در مرحله های قبلی بوده است باید به این فرم دسترسی فقط خواندنی داشته باشد
        # 4- اگر کاربر مربوط به مراحل بعدی است غیر مجاز است
        # 5- اگر کاربر مربوط به این درخواست نیست غیر مجاز است
        
        # انواع وضعیت هایی که درخواست می تواند داشته باشد:
       
        # ('DRAFTD', 'پیش نویس'): 
        # مجاز به ویرایش: درخواست دهنده         فرم : درخواست ساده
        # فقط خواندنی: مدیر درخواست دهنده      فرم: درخواست ساده
       
        # ('DIRMAN', 'اظهار نظر مدیر مستقیم'):
        # مجاز به ویرایش: مدیر مستقیم       فرم:درخواست ساده
        # فقط خواندنی: درخواست دهنده        فرم: درخواست ساده
       
        # ('RELMAN', 'اظهار نظر مدیر مربوطه')
        # مجاز به ویرایش: مدیر مربوطه                  فرم: درخواست کامل
        # فقط خواندنی: دبیر کمیته       فرم: درخواست کامل فقط خواندنی
        # فقط خواندنی: درخواست دهنده و مدیر مستقیم      فرم: درخواست ساده

        # برای اینکه اشتباهی رخ ندهد، بهتر است این کار را بکنیم
        # به ازای هر وضعیت، بررسی زیر را انجام دهیم
        # 1- کاربر جاری را بررسی کنیم
        # 2- اگر کاربر باید به این فرم دسترسی به روزرسانی داشته باشد، به وی اجازه به روزرسانی بدهیم
        # 3- اگر کاربر در مرحله های قبلی بوده است باید به این فرم دسترسی فقط خواندنی داشته باشد
        # 4- اگر کاربر مربوط به مراحل بعدی است غیر مجاز است
        # 5- اگر کاربر مربوط به این درخواست نیست غیر مجاز است
        
        # انواع وضعیت هایی که درخواست می تواند داشته باشد:
       
        # ('DRAFTD', 'پیش نویس'): 
        # مجاز به ویرایش: درخواست دهنده         فرم : درخواست ساده
        # فقط خواندنی: مدیر درخواست دهنده      فرم: درخواست ساده
       
        # ('DIRMAN', 'اظهار نظر مدیر مستقیم'):
        # مجاز به ویرایش: مدیر مستقیم       فرم:درخواست ساده
        # فقط خواندنی: درخواست دهنده        فرم: درخواست ساده
       
        # ('RELMAN', 'اظهار نظر مدیر مربوطه')
        # مجاز به ویرایش: مدیر مربوطه                  فرم: درخواست کامل
        # فقط خواندنی: دبیر کمیته       فرم: درخواست کامل فقط خواندنی
        # فقط خواندنی: درخواست دهنده و مدیر مستقیم      فرم: درخواست ساده
        
        # ('COMITE', 'اظهار نظر کمیته'): 
        # مجاز به ویرایش: دبیرکمیته                    فرم: درخواست کامل
        # فقط خواندنی: مدیر درخواست دهنده       فرم: درخواست کامل فقط خواندنی
        # فقط خواندنی: درخواست دهنده و مدیر مستقیم      فرم: درخواست ساده
        
        # ('DOTASK', 'انجام تسک ها'): 
        # فقط خواندنی: درخواست دهنده، مدیر مستقیم، مدیر مربوطه، دبیرکمیته           فرم:لیست تسک ها فقط خواندنی
        # برای سایر نقش ها لازم است که وضعیت تسک هم کنترل شود
            # ('EXERED', 'آماده انتخاب مجری')
            # مجاز به ویرایش : مجریان       فرم: انتخاب تسک
            # فقط خواندنی: تسترها       فرم: انتخاب تسک

            # ('EXESEL', 'مجری انتخاب شده'),
            # مجاز به ویرایش : مجری منتخب      فرم: گزارش تسک
            # فقط خواندنی: مجریان، تسترها       فرم: انتخاب تسک

            # ('TESRED', 'آماده انتخاب تستر'),
            # مجاز به ویرایش: تسترها        فرم: انتخاب تسک
            # فقط خواندنی: مجری منتخب          فرم: گزارش تسک
            # فقط خواندنی: مجریان       فرم: انتخاب تسک
            
            # ('TESSEL', 'تستر انتخاب شده'),
            # مجاز به ویرایش: تستر منتخب       فرم : گزارش تسک
            # فقط خواندنی: مجری منتخب       فرم: گزارش تسک
            # فقط خواندنی: مجریان و تسترها      فرم: انتخاب تسک
            
            # ('FINISH', 'انجام موفق'),
            # ('FAILED', 'انجام ناموفق'),    
            # فقط خواندنی: تستر منتخب، مجری منتخب       فرم : گزارش تسک
            # فقط خواندنی: مجری منتخب       فرم: گزارش تسک
           
            
        
        # ('FINISH', 'خاتمه یافته'):
        # فقط خواندنی: درخواست دهنده، مدیر مستقیم، مدیر مربوطه، دبیرکمیته           فرم:لیست تسک ها فقط خواندنی
        
        # ('FAILED', 'خاتمه ناموفقیت آمیز'):
        # فقط خواندنی: درخواست دهنده، مدیر مستقیم، مدیر مربوطه، دبیرکمیته           فرم:لیست تسک ها فقط خواندنی
        
        
        
        #توجه کنید، ممکن بود این کد را به صورت ساده تر و فشرده تر نوشت، ولی به دلیل خوانایی از فاکتور گیری و یا مقادیر پیش فرض چندگانه اجتناب شده است
        if request_status == "DRAFTD":
            # پیش نویس
            if user_nationalcode == request_obj.user_requestor.national_code:
                form = "RequestSimple"
                mode = "UPDATE"
            elif user_nationalcode == request_obj.user_direct_manager.national_code:
                form = "RequestSimple"
                mode = "READONLY"
            else:
                form = "Invalid"
                mode = "INVALID"

        elif request_status == "DIRMAN":
            # اظهار نظر مدیر مستقیم
            if user_nationalcode == request_obj.user_direct_manager.national_code:
                form = "RequestSimple"
                mode = "UPDATE"
            elif user_nationalcode == request_obj.user_requestor.national_code:
                form = "RequestSimple"
                mode = "READONLY"
            else:
                form = "Invalid"
                mode = "INVALID"

        elif request_status == "RELMAN":
            # اظهار نظر مدیر مربوطه
            if user_nationalcode == request_obj.user_related_manager.national_code:
                form = "RequestFull"
                mode = "UPDATE"
            elif user_nationalcode == request_obj.user_committee.national_code:
                form = "RequestFull-Readonly"
                mode = "READONLY"
            elif user_nationalcode in (
                request_obj.user_requestor.national_code,
                request_obj.user_direct_manager.national_code,
            ):
                form = "RequestSimple"
                mode = "READONLY"
            else:
                form = "Invalid"
                mode = "INVALID"

        elif request_status == "COMITE":
            # اظهار نظر کمیته
            if user_nationalcode == request_obj.user_committee.national_code:
                form = "RequestFull"
                mode = "UPDATE"
            elif user_nationalcode == request_obj.user_related_manager.national_code:
                form = "RequestFull-Readonly"
                mode = "READONLY"
            elif user_nationalcode in (
                request_obj.user_requestor.national_code,
                request_obj.user_direct_manager.national_code,
            ):
                form = "RequestSimple"
                mode = "READONLY"
            else:
                form = "Invalid"
                mode = "INVALID"

        elif request_status == "DOTASK":
            # انجام تسک ها
            if user_nationalcode in (
                request_obj.user_requestor.national_code,
                request_obj.user_direct_manager.national_code,
                request_obj.user_related_manager.national_code,
                getattr(request_obj.user_committee, 'national_code', None),
            ):
                form = "TaskList"
                mode = "READONLY"
            else:
                # تسک جاری را به دست می آوریم
                task:Task = request_obj.current_task
                
                # حالا کنترل می کنیم که وضعیت تسک چیست؟
                task_status = task.status_code

                # حالتهایی که ممکن است اتفاق بیافتد:
                # ('EXERED', 'آماده انتخاب مجری'),
                # ('EXESEL', 'مجری انتخاب شده'),
                # ('TESRED', 'آماده انتخاب تستر'),
                # ('TESSEL', 'تستر انتخاب شده'),
                # ('FINISH', 'انجام موفق'),
                # ('FAILED', 'انجام ناموفق'),                

                # نکات مهم:
                # 1- این کد به دلیل افزایش خوانایی غیرفشرده نوشته شده است
                # 2- با توجه به اینکه مثلا یک مجری می تواند تستر هم باشد، ترتیب کنترل شرط ها مهم است
                
                # تسک هنوز شروع نشده است
                if task_status == 'DEFINE':
                    form = "Invalid"
                    mode = "INVALID"
                
                # آماده انتخاب مجری
                elif task_status == 'EXERED':
                    # اگر کاربر در لیست مجریان باشد
                    if any(user_nationalcode == executor.national_code for executor in task.executors):
                        form = 'TaskSelect'
                        mode = "UPDATE"
                    # اگر کاربر در لیست تسترها باشد
                    elif any(user_nationalcode == tester.national_code for tester in task.testers):
                        form = 'TaskSelect'
                        mode = "READONLY"
                    else:
                        form = "Invalid"
                        mode = "INVALID"
                        
                # مجری انتخاب شده است
                elif task_status == 'EXESEL':
                    # اگر کاربر مجری منتخب باشد
                    if task.selected_executor and user_nationalcode == task.selected_executor.national_code:
                        form = 'TaskReport'
                        mode = "UPDATE"
                    # اگر کاربر مجری منتخب نباشد، ولی در لیست مجریان باشد
                    elif any(user_nationalcode == executor.national_code for executor in task.executors):
                        form = 'TaskSelect'
                        mode = "READONLY"
                    # اگر کاربر در لیست تسترهای منختب باشد
                    elif any(user_nationalcode == tester.national_code for tester in task.testers):
                        form = 'TaskSelect'
                        mode = "READONLY"
                    else:
                        form = "Invalid"
                        mode = "INVALID"
                
                # آماده انتخاب تستر
                elif task_status == 'TESRED':
                    # اگر کاربر در لیست تسترها باشد
                    if any(user_nationalcode == tester.national_code for tester in task.testers):
                        form = 'TaskSelect'
                        mode = "UPDATE"
                    # اگر کاربر مجری منتخب باشد
                    elif task.selected_executor and user_nationalcode == task.selected_executor.national_code:
                        form = 'TaskReport'
                        mode = "READONLY"
                    # اگر کاربر در لیست مجریان باشد
                    elif any(user_nationalcode == executor.national_code for executor in task.executors):
                        form = 'TaskSelect'
                        mode = "READONLY"
                    else:
                        form = "Invalid"
                        mode = "INVALID"
                
                # تستر انتخاب شده است
                elif task_status == 'TESSEL':
                    # اگر کاربر تستر منتخب باشد
                    if task.selected_tester and user_nationalcode == task.selected_tester.national_code:
                        form = 'TaskReport'
                        mode = "UPDATE"
                    # اگر کاربر مجری منتخب باشد
                    elif task.selected_executor and user_nationalcode == task.selected_executor.national_code:
                        form = 'TaskReport'
                        mode = "READONLY"
                    # اگر کاربر در لیست تسترها باشد
                    elif any(user_nationalcode == tester.national_code for tester in task.testers):
                        form = 'TaskSelect'
                        mode = "READONLY"
                    # اگر کاربر در لیست مجریان باشد
                    elif any(user_nationalcode == executor.national_code for executor in task.executors):
                        form = 'TaskSelect'
                        mode = "READONLY"
                    else:
                        form = "Invalid"
                        mode = "INVALID"
                
                # تسک موفقیت آمیز خاتمه یافته
                # انجام تسک ناموفق بوده است
                elif task_status == 'FINISH' or task_status == 'FAILED':
                    # اگر کاربر تستر منتخب باشد
                    if user_nationalcode == task.selected_tester.national_code:
                        form = 'TaskReport'
                        mode = "READONLY"
                    # اگر کاربر مجری منتخب باشد
                    elif user_nationalcode == task.selected_executor.national_code:
                        form = 'TaskReport'
                        mode = "READONLY"
                    # اگر کاربر در لیست تسترها باشد
                    elif any(user_nationalcode == tester.national_code for tester in task.testers):
                        form = 'TaskSelect'
                        mode = "READONLY"
                    # اگر کاربر در لیست مجریان باشد
                    elif any(user_nationalcode == executor.national_code for executor in task.executors):
                        form = 'TaskSelect'
                        mode = "READONLY"
                    else:
                        form = "Invalid"
                        mode = "INVALID"
                else:
                    form = "Invalid"
                    mode = "INVALID"                    
        elif request_status in ("FINISH", "FAILED"):
            # خاتمه یافته یا خاتمه ناموفقیت آمیز
            if user_nationalcode in (
                request_obj.user_requestor.national_code,
                request_obj.user_direct_manager.national_code,
                request_obj.user_related_manager.national_code,
                request_obj.user_committee.national_code,
            ):
                form = "TaskList-Readonly"
                mode = "READONLY"
            else:
                form = "Invalid"
                mode = "INVALID"

        else:
            # وضعیت نامعتبر
            form = "Invalid"
            mode = "INVALID"

            
        return {"mode": mode, "form": form}

    def load_task_data(self, request_obj:"Request", task_obj:"Task", user_nationalcode: str):
        """
        بارگذاری داده‌های تسک
        """
        form_data = {"success": True, "message": ""}

        # دریافت اطلاعات درخواست
        form_data["request"] = request_obj.request_instance
        form_data["request_id"] = request_obj.request_id

        # دریافت اطلاعات تسک
        form_data["task"] = task_obj.task_instance

        # دریافت اطلاعات کاربران تسک
        form_data["task_users"] = task_obj.users
        form_data["task_executors"] = task_obj.executors
        form_data["task_testers"] = task_obj.testers
        
        form_data["task_selected_executor"] = task_obj.selected_executor
        form_data["task_selected_tester"] = task_obj.selected_tester
        
        form_data["status_code"] = task_obj.status_code
        form_data["status_title"] = task_obj.status_title if task_obj.status_title else 'انتخاب تسک توسط مجریان'

        # دریافت اطلاعات کاربر جاری
        form_data["current_user"] = user_nationalcode
        form_data["is_task"] = True

        # حالا باید ببینیم این کاربر مجری و یا تستر است؟
        tester_executor = 'E' if user_nationalcode in [u.national_code for u in task_obj.executors] else 'T'

        form_data['done_date'] = task_obj.executor_done_date if tester_executor == 'E' else task_obj.tester_done_date
        form_data['done_time'] = task_obj.executor_done_time if tester_executor == 'E' else task_obj.tester_done_time
        form_data['report'] = task_obj.executor_report if tester_executor == 'E' else task_obj.tester_report
        
        return form_data

    def validate_task_report(self, form_data: dict) -> dict:
        """
        اعتبارسنجی گزارش تسک
        """
        errors = []

        # فیلدهای الزامی
        required_fields = [
            ("operation_date", "تاریخ انجام عملیات"),
            ("operation_time", "زمان انجام عملیات"),
            ("operation_report", "گزارش انجام عملیات"),
            ("operation_result", "نتیجه عملیات"),
        ]

        for field, description in required_fields:
            if not form_data.get(field):
                errors.append(f"{description} الزامی است")

        if errors:
            return {"success": False, "message": "<br>".join(errors)}
        else:
            return {"success": True, "message": ""}

    def get_current_user_info(self, user_nationalcode: str) -> dict:
        """
        دریافت اطلاعات کاربر جاری
        """
        try:
            user = m.User.objects.get(national_code=user_nationalcode)
            user_team_roles = m.UserTeamRole.objects.filter(
                national_code=user_nationalcode
            )

            team_roles = []
            for utr in user_team_roles:
                team_roles.append(
                    {
                        "role_title": utr.role_title,
                        "role_id": utr.role_id,
                        "team_name": utr.team_code.team_name if utr.team_code else "",
                        "team_code": utr.team_code.team_code if utr.team_code else "",
                        "manager_national_code": (
                            utr.manager_national_code.national_code
                            if utr.manager_national_code
                            else ""
                        ),
                    }
                )

            return {
                "fullname": f"{user.first_name} {user.last_name}",
                "username": user.username,
                "national_code": user.national_code,
                "gender": user.gender,
                "is_active": True,
                "team_roles": team_roles,
            }
        except:
            return {}

    def get_all_users_info(self) -> list:
        """
        دریافت اطلاعات همه کاربران
        """
        try:
            users = m.User.objects.all()[:10]  # محدود کردن به 10 کاربر
            all_users = []

            for user in users:
                user_team_roles = m.UserTeamRole.objects.filter(
                    national_code=user.national_code
                )
                team_roles = []

                for utr in user_team_roles:
                    team_roles.append(
                        {
                            "role_title": utr.role_title,
                            "role_id": utr.role_id,
                            "team_name": (
                                utr.team_code.team_name if utr.team_code else ""
                            ),
                            "team_code": (
                                utr.team_code.team_code if utr.team_code else ""
                            ),
                            "manager_national_code": (
                                utr.manager_national_code.national_code
                                if utr.manager_national_code
                                else ""
                            ),
                        }
                    )

                all_users.append(
                    {
                        "fullname": f"{user.first_name} {user.last_name}",
                        "username": user.username,
                        "national_code": user.national_code,
                        "gender": user.gender,
                        "is_active": True,
                        "team_roles": team_roles,
                    }
                )

            return all_users
        except:
            return []

    def form_validation(self, form_data: json) -> json:
        """
        این تابع بر مبنای داده های ورودی، صحت سنجی اطلاعات فرم را انجام می دهد

        Args:
            form_data (json): این متغییر دربردارنده اطلاعات فرم است

        Returns:
            json: خروجی در قالب زیر است
            {'success':False, 'message':''}
        """
        user_nationalcode = form_data.get("user_nationalcode", -1)
        request_id = form_data.get("request_id", -1)
        request_task_id = form_data.get("request_task_id", -1)

        # وضعیت جاری فرم را به دست می آوریم
        form_status = self.check_form_status(
            user_nationalcode=user_nationalcode,
            request_id=request_id,
        )
        form_mode = form_status["mode"]
        form_name = form_status["form"]

        error_message = []

        # اگر کاربر مجاز به دیدن این فرم نباشد
        if form_mode == "INVALID":
            return {
                "success": False,
                "message": "متاسفانه شما مجاز به باز کردن این فرم نمی باشید",
            }

        # اگر فرم در حالت فقط خواندنی باشد، اعتبارسنجی معنی ندارد
        if form_mode == "READONLY":
            return {"success": True, "message": ""}

        # فیلدهای اجباری
        required_fields = [
            ("change_type", "نوع تغییر اجباری است"),
            ("change_title", "عنوان تغییرات اجباری است"),
            ("change_description", "توضیحات تغییرات را وارد کنید"),
            ("user_nationalcode", "کد ملی درخواست دهنده اجباری است"),
        ]

        # تیم و سمت درخواست کننده صرفا در زمان درج کنترل می شود
        if form_mode == "INSERT":
            # تیم و سمت کاربر را به دست می آوریم
            # در صورتی که کاربر جاری یک سمت دارد فرقی ندارد
            # اما وقتی کاربر چند سمت داشته باشد، می تواند سمت و تیم خود را انتخاب کند
            # این موضوع به این دلیل اهمیت دارد که ما برای مدیر مستقیم تیم و سمتی که انتخاب کرده است ارسال می کنیم
            user_team_code =form_data.get("requestor_team_code")
            if not user_team_code:
                error_message.append("تیم کاربر به درستی انتخاب نشده است.")

            user_role_id = form_data.get("requestor_role_id")
            if not user_role_id:
                error_message.append("سمت کاربر به درستی انتخاب نشده است.")

        if form_mode in ("INSERT", "UPDATE"):
            # حالا کنترل می کنیم که عنوان درخواست به درستی ثبت شده باشد
            request_title = form_data.get("change_title")
            # طول عنوان درخواست باید حداقل 5 کارکتر بدون فاصله باشد
            if not self.__is_valid_string(request_title):
                error_message.append("لطفا عنوان مناسبی برای درخواست وارد نمایید.")

            # حالا کنترل می کنیم که شرح درخواست به درستی ثبت شده باشد
            request_description = form_data.get("change_description")
            if not self.__is_valid_string(request_description):
                error_message.append("لطفا عنوان مناسبی برای شرح درخواست وارد نمایید.")

            # حالا کنترل می کنیم که نوع درخواست را انتخاب کرده باشد
            request_type = form_data.get("change_type")
            valid, request_type = self.__is_valid_integer(request_type)
            if not valid or request_type <= 0:
                error_message.append("لطفا نوع تغییر را انتخاب کنید.")

        # اگر فرم اطلاعات کامل باشد، باید اعتبارسنجی برای تمامی فیلدها صورت بگیرد
        if form_name == "RequestFull":

            # اگر نیاز به کمیته ندارد، باید شناسه مربوطه حذف شود
            if not form_data.get("need_committee", False):
                form_data.pop("committee", None)
            else:
                required_fields.append(("committee", "انتخاب کمیته الزامی است."))

            # بررسی فیلدهای الزامی
            for field, msg in required_fields:
                if not form_data.get(field):
                    error_message.append(msg)

            # فیلدهای تاریخ
            date_fields = [
                ("change_date", "تاریخ تغییرات"),
                ("change_date_actual", "تاریخ واقعی انجام تغییرات"),
            ]

            for field, description in date_fields:
                date = form_data.get(field)
                if date:
                    try:
                        # بررسی اینکه آیا ورودی از نوع رشته است
                        if isinstance(date, str):
                            # تبدیل به تاریخ شمسی
                            date = jdatetime.datetime.strptime(date, "%Y/%m/%d")
                        else:
                            error_message.append(
                                f"فرمت تاریخ برای '{description}' نامعتبر است."
                            )
                    except ValueError:
                        error_message.append(
                            f"'{description}' باید در فرمت 'YYYY-MM-DD' باشد."
                        )

            time_fields = [
                ("change_time", "ساعت تغییرات"),
            ]

            for field, description in time_fields:
                time = form_data.get(field)
                if time:
                    try:
                        # بررسی اینکه آیا ورودی از نوع رشته است
                        if isinstance(time, str):
                            # بررسی اینکه آیا فرمت زمان صحیح است
                            hours, minutes = map(int, time.split(":"))
                            if 0 <= hours <= 24 and 0 <= minutes <= 59:
                                pass
                            else:
                                error_message.append(
                                    f"فرمت ساعت برای '{description}' نامعتبر است. ساعت باید بین 00:00 تا 23:59 باشد."
                                )
                        else:
                            error_message.append(
                                f"فرمت ساعت برای '{description}' نامعتبر است."
                            )
                    except ValueError:
                        error_message.append(f"'{description}' باید در فرمت 'HH:MM' باشد.")

            # کد ملی درخواست کننده
            if (
                form_data.get("user_nationalcode")
                and not m.User.objects.filter(
                    national_code=form_data["user_nationalcode"]
                ).exists()
            ):
                error_message.append("کد ملی درخواست کننده نامعتبر است.")
                
            # # به دست آوردن تیم و سمت کاربر درخواست دهنده
            # result = self.__get_user_team_role(form_data.get('user_team_role'))

            # # اگر در استخراج داده ها با خطایی مواجه شده باشیم
            # if not result.get('success', False):
            #     error_message.append(result.get('message'), 'امکان تشخصیص تیم و سمت کاربر وجود ندارد')
            # else:
            #     form_data['requestor_team_code'] = result.get('team_code')
            #     form_data['requestor_role_id'] = result.get('role_id')

            # # تیم درخواست‌دهنده
            # if (not m.Team.objects.filter(
            #         team_code=form_data["requestor_team_code"]
            #     ).exists()
            # ):
            #     error_message.append("تیم درخواست‌دهنده نامعتبر است.")


            # # کد ملی مدیر
            # if not form_data.get("manager_nationalcode"):
            #     manager_nationalcode = (
            #         m.UserTeamRole.objects.filter(
            #             team_code=form_data["requestor_team_code"],
            #             role_id=form_data["requestor_role_id"],
            #         )
            #         .values("manager_national_code")
            #         .first()
            #     )
            #     if manager_nationalcode:
            #         form_data["manager_nationalcode"] = manager_nationalcode[
            #             "manager_national_code"
            #         ]
            #     # حالتی است که مدیر کاربر پیدا نشده است
            #     else:
            #         error_message.append(
            #             "امکان تشخیص دادن مدیر کاربر درخواست دهنده وجود ندارد"
            #         )
            # elif not m.User.objects.filter(
            #     national_code=form_data["manager_nationalcode"]
            # ).exists():
            #     error_message.append("کد ملی مدیر نامعتبر است.")
            
            # کنترل کمیته مربوطه و کاربر آن، در صورتی انجام می شود که گزینه نیاز به کمیته دارد انتخاب شده باشد
            if form_data.get("need_committee", False):
                # شناسه کمیته
                if (
                    form_data.get("committee")
                    and not m.Committee.objects.filter(id=form_data["committee"]).exists()
                ):
                    error_message.append("شناسه کمیته نامعتبر است.")

                # کد ملی کاربر کمیته
                if (
                    form_data.get("committee_user_nationalcode")
                    and not m.User.objects.filter(
                        national_code=form_data["committee_user_nationalcode"]
                    ).exists()
                ):
                    error_message.append("کد ملی دبیر کمیته نامعتبر است.")

                if not form_data.get("committee_user_nationalcode"):
                    committee_user_nationalcode = (
                        m.Committee.objects.filter(id=form_data.get("committee",-1))
                        .values("administrator_nationalcode")
                        .first()
                    )
                    if committee_user_nationalcode:
                        form_data["committee_user_nationalcode"] = (
                            committee_user_nationalcode["administrator_nationalcode"]
                        )
                    # حالتی است که دبیر کمیته پیدا نشده است
                    else:
                        error_message.append("امکان تشخیص دادن دبیر کمیته وجود ندارد")
                elif not m.User.objects.filter(
                    national_code=form_data["committee_user_nationalcode"]
                ).exists():
                    error_message.append("کد ملی دبیر کمیته نامعتبر است.")

            # گستردگی تغییرات
            if (
                form_data.get("change_level")
                and not m.ConstValue.objects.filter(
                    id=form_data["change_level"]
                ).exists()
            ):
                error_message.append("گستردگی تغییرات نامعتبر است.")

            # طبقه‌بندی
            if (
                form_data.get("classification")
                and not m.ConstValue.objects.filter(
                    id=form_data["classification"]
                ).exists()
            ):
                error_message.append("طبقه‌بندی نامعتبر است.")

            # اولویت
            if (
                form_data.get("priority")
                and not m.ConstValue.objects.filter(id=form_data["priority"]).exists()
            ):
                error_message.append("اولویت نامعتبر است.")

            # سطح ریسک
            if (
                form_data.get("risk_level")
                and not m.ConstValue.objects.filter(id=form_data["risk_level"]).exists()
            ):
                error_message.append("سطح ریسک نامعتبر است.")

            # دامنه تغییر
            if (
                form_data.get("change_domain")
                and not m.ConstValue.objects.filter(
                    id=form_data["change_domain"]
                ).exists()
            ):
                error_message.append("دامنه تغییر نامعتبر است.")

            # نوع تغییر
            if (
                form_data.get("change_type")
                and not m.ChangeType.objects.filter(
                    id=form_data["change_type"]
                ).exists()
            ):
                error_message.append("نوع تغییر نامعتبر است.")

            # اعتبارسنجی محل تغییر: سایر
            try:
                validator.Validator.validate_change_location_other(
                    form_data.get("change_location_other"),
                    form_data.get("change_location_other_description"),
                )
            except ValidationError as e:
                error_message.append(str(e))

            # اعتبارسنجی توقف خدمات بحرانی و حساس
            try:
                validator.Validator.validate_critical_service(
                    form_data.get("stop_critical_service"),
                    form_data.get("critical_service_title"),
                )
            except ValidationError as e:
                error_message.append(str(e))

            try:
                validator.Validator.validate_sensitive_service(
                    form_data.get("stop_sensitive_service"),
                    form_data.get("stop_service_title"),
                )
            except ValidationError as e:
                error_message.append(str(e))

            # اعتبارسنجی سایر الزامات
            try:
                validator.Validator.validate_reason_other(
                    form_data.get("reason_other"),
                    form_data.get("reason_other_description"),
                )
            except ValidationError as e:
                error_message.append(str(e))

            # اعتبارسنجی نظر مدیر
            try:
                validator.Validator.validate_manager_opinion(
                    form_data.get("manager_opinion"),
                    form_data.get("manager_reject_description"),
                )
            except ValidationError as e:
                error_message.append(str(e))

            # اعتبارسنجی فیلدهای کمیته
            try:
                validator.Validator.validate_committee_fields(
                    form_data.get("need_committee"),
                    form_data.get("committee_user_nationalcode"),
                    form_data.get("committee_opinion_date"),
                    form_data.get("committee_opinion"),
                    form_data.get("committee_reject_description"),
                )
            except ValidationError as e:
                error_message.append(str(e))

            # اعتبارسنجی تاریخ تست و گزارش تست
            try:
                validator.Validator.validate_test_date(
                    form_data.get("test_date"), form_data.get("changing_date_actual")
                )
            except ValidationError as e:
                error_message.append(str(e))

            try:
                validator.Validator.validate_tester_report_date(
                    form_data.get("tester_report_date"), form_data.get("test_date")
                )
            except ValidationError as e:
                error_message.append(str(e))

            # اعتبارسنجی کلیدهای خارجی برای تیم‌ها
            for team_code in form_data.get("teams", []):
                if not m.Team.objects.filter(team_code=team_code).exists():
                    error_message.append(f"کد تیم '{team_code}' نامعتبر است.")

            # اعتبارسنجی کلیدهای خارجی برای شرکت‌ها
            for corp_code in form_data.get("corps", []):
                if not m.Corp.objects.filter(corp_code=corp_code).exists():
                    error_message.append(f"کد شرکت '{corp_code}' نامعتبر است.")

            # اعتبارسنجی مقادیر اطلاعات تکمیلی
            for extra_info_id in form_data.get("extra_information", []):
                if not m.ConstValue.objects.filter(id=extra_info_id).exists():
                    error_message.append(
                        f"مقدار اطلاعات تکمیلی با شناسه '{extra_info_id}' نامعتبر است."
                    )

        # اگر اعتبارسنجی با خطا مواجه شده باشد
        if error_message:
            return {"success": False, "message": "<br>".join(error_message)}
        else:
            return {"success": True, "message": ""}

    # def next_step_request(
    #     self, request_id: int, user_nationalcode: int, action: str, form_data: dict
    # ) -> dict:
    #     # دریافت درخواست بر اساس request_id
    #     request_instance = get_request_instance(request_id)
    #     if not request_instance:
    #         return {"success": False, "message": "شناسه درخواست نامعتبر است"}

    # def next_step_task(
    #     self, request_task_id: int, user_nationalcode: int, action: str, form_data: dict
    # ) -> dict:
    #     # دریافت درخواست بر اساس request_id
    #     request_instance = get_request_instance(request_task_id)
    #     if not request_instance:
    #         return {"success": False, "message": "شناسه درخواست نامعتبر است"}

    # # این تابع با توجه به مرحله فعلی، به مرحله بعدی می رود
    # def next_step(
    #     self,
    #     request_id: int,
    #     user_nationalcode: int,
    #     task_id: int,
    #     action: str,
    #     form_data: dict,
    # ) -> dict:
    #     # دریافت درخواست بر اساس request_id
    #     request_instance = get_request_instance(request_id)
    #     if not request_instance:
    #         return {"success": False, "message": "شناسه درخواست نامعتبر است"}

    #     # ابتدا باید کنترل کنیم که آیا کاربر جاری مجاز به انجام عملیات بر روی فرم هست یا خیر؟
    #     form_status = check_form_status(user_nationalcode, request_id)
    #     form_data["form_status"] = form_status["status"]

    #     # اگر کاربر جزو کاربران مجاز این درخواست نباشد
    #     if form_status == "INVALID":
    #         return {
    #             "success": False,
    #             "message": "شما مجوز دسترسی به این درخواست را ندارید",
    #         }

    #     # اگر کاربر مجاز باشد ولی در این مرحله امکان انجام عملیات نداشته باشد
    #     if form_status == "READONLY":
    #         return {
    #             "success": False,
    #             "message": "شما در این مرحله امکان انجام عملیات را ندارید",
    #         }

    #     # وضعیت فعلی درخواست
    #     current_status = request_instance.status_code

    #     # حالا مرحله بعدی را مشخص می کنیم
    #     validation_error = ""
    #     # تعیین وضعیت جدید بر اساس action
    #     if action == "CON":
    #         new_status = get_next_status(current_status)
    #     elif action == "RET":
    #         new_status = get_previous_status(current_status)
    #     elif action == "REJ":
    #         # اعتبارسنجی را انجام می دهیم
    #         new_status = "FAILED"
    #     else:
    #         return {"success": False, "message": "نوع عملیات درخواستی معتبر نمی باشد"}

    #     # اعتبارسنجی انجام می شود
    #     validation_error = step_data_validation(
    #         action=action, step=current_status, data=form_data
    #     )
    #     # اگر اعتبارسنجی با خطا مواجه شده باشد
    #     if validation_error:
    #         return {"success": False, "message": "<br>".join(validation_error)}

    #     # با توجه به وضعیت فعلی اطلاعات کاربر مربوطه را به دست می آوریم
    #     if new_status not in ("FAILED", "FINISH"):
    #         user_info = get_user_information(request_id, new_status)
    #         if user_info == "-1":
    #             return {
    #                 "success": False,
    #                 "message": "امکان تعیین کاربر بعدی جهت ارسال وجود ندارد",
    #             }

    #     # به‌روزرسانی وضعیت درخواست
    #     request_instance.status_code = new_status
    #     request_instance.save()

    #     # داده ها را ذخیره می کنیم
    #     step_data_save(
    #         action=action,
    #         request=request_instance,
    #         status=current_status,
    #         data=form_data,
    #     )

    #     # فراخوانی توابع مربوطه بر اساس وضعیت جدید
    #     if current_status == "DRAFTD":
    #         doc_response = register_document(
    #             app_doc_id=request_instance.id,
    #             priority=get_priority_title(request_instance.priority.id),
    #             doc_state="پیش نویس",
    #             document_title=request_instance.change_title,
    #             app_code=APP_CODE,
    #             owner_nationalcode=request_instance.requestor_nationalcode,
    #         )
    #         request_instance.doc_id = doc_response["data"]["id"]
    #         request_instance.save()
    #     if new_status in ["MANAGE", "EXECUT", "COMITE", "TESTER"]:
    #         send_document(
    #             doc_id=request_instance.doc_id,
    #             sender_national_code=user_nationalcode,
    #             inbox_owners_national_code=get_inbox_owners_national_code(
    #                 new_status, request_instance
    #             ),
    #         )
    #     elif new_status == "FINISH":
    #         finish_flow(request_instance.doc_id, APP_CODE)
    #     elif new_status == "FAILED":
    #         terminate_flow(request_instance.doc_id, APP_CODE)

    #     # به‌روزرسانی وضعیت سند
    #     # erfan
    #     update_document_state_code(request_instance.doc_id, APP_CODE, new_status)

    #     # حالت هایی که فرآیند پایان می یابد
    #     if new_status == "FAILED":
    #         message = "با توجه به رد مدرک، فرآیند متوقف گردید"
    #     elif new_status == "FINISH":
    #         message = "فرآیند با موفقیت خاتمه پیدا کرد"
    #     else:
    #         message = f"فرم با موفقیت برای {user_info} ارسال شد"
    #     return {"success": True, "message": message, "request_id": request_id}

    # def get_next_status(current_status):
    #     # تابعی برای دریافت وضعیت بعدی بر اساس وضعیت فعلی
    #     status_order = ["DRAFTD", "MANAGE", "COMITE", "EXECUT", "TESTER", "FINISH"]
    #     return status_order[status_order.index(current_status) + 1]

    # # این تابع بر اساس مرحله و عملیات، داده های ارسالی را صحت سنجی می کند
    # def step_data_validation(self, action: str, step: str, data: dict) -> list[str]:
    #     # اگر عملیات رد مدرک باشد، فقط باید کنترل کنیم که دلیل رد مدرک ارسال شده است
    #     error_message = []
    #     if action == "REJ":
    #         if not data.get("reject_reason"):
    #             return ["دلیل رد مدرک مشخص نشده است"]
    #     # اگر عملیات تایید و مرحله تستر یا مجری باشد باید فیلدهای مربوطه را کنترل کنیم
    #     elif step in ["EXECUT", "TESTER"]:
    #         operation_date = data.get("operation_date")
    #         if not operation_date:
    #             error_message.append("تاریخ انجام عملیات مشخص نشده است")
    #         operation_time = data.get("operation_time")
    #         if not operation_time:
    #             error_message.append("زمان انجام عملیات مشخص نشده است")
    #         operation_report = data.get("operation_report")
    #         if not operation_report:
    #             error_message.append("گزارش انجام عملیات مشخص نشده است")
    #         operation_result = data.get("operation_result")
    #         if operation_result.lower() not in ["true", "false"]:
    #             error_message.append("نتیجه عملیات نامعتبر است")
    #         else:
    #             if data.get("operation_result") == "true":
    #                 data["operation_result"] = True
    #             else:
    #                 data["operation_result"] = False

    #         # اگر مجری باشد، فیلدهای زیر را هم باید تکمیل کند
    #         if step == "EXECUT":

    #             fields_to_check = {
    #                 "changing_duration_actual_hour": (
    #                     "ساعت مدت زمان انجام تغییرات",
    #                     data.get("changing_duration_actual_hour"),
    #                 ),
    #                 "changing_duration_actual_minute": (
    #                     "دقیقه مدت زمان انجام تغییرات",
    #                     data.get("changing_duration_actual_minute"),
    #                 ),
    #                 "downtime_duration_actual_hour": (
    #                     "ساعت مدت زمان قطعی سیستم",
    #                     data.get("downtime_duration_actual_hour"),
    #                 ),
    #                 "downtime_duration_actual_minute": (
    #                     "دقیقه مدت زمان قطعی سیستم",
    #                     data.get("downtime_duration_actual_minute"),
    #                 ),
    #             }

    #             for field, (persian_title, value) in fields_to_check.items():
    #                 is_valid, int_value = is_valid_integer(value)
    #                 if is_valid:
    #                     data[field] = int_value  # ذخیره مقدار عددی معتبر
    #                 else:
    #                     error_message.append(
    #                         f"مقدار برای '{persian_title}' باید یک عدد صحیح معتبر باشد."
    #                     )

    #             # changing_duration_actual_hour = data.get('changing_duration_actual_hour')
    #             # if changing_duration_actual_hour is None or not isinstance(changing_duration_actual_hour, int):
    #             #     error_message.append('مدت زمان واقعی تغییر نامعتبر است')
    #             # changing_duration_actual_minute = data.get('changing_duration_actual_minute')
    #             # if changing_duration_actual_minute is None or not isinstance(changing_duration_actual_minute, int) or changing_duration_actual_minute < 0 or changing_duration_actual_minute > 59:
    #             #     error_message.append('دقیقه مدت زمان واقعی تغییر نامعتبر است')
    #             # downtime_duration_actual_hour = data.get('downtime_duration_actual_hour')
    #             # if downtime_duration_actual_hour is None or not isinstance(downtime_duration_actual_hour, int):
    #             #     error_message.append('مدت زمان قطعی سیستم نامعتبر است')
    #             # downtime_duration_actual_minute = data.get('downtime_duration_actual_minute')
    #             # if downtime_duration_actual_minute is None or not isinstance(downtime_duration_actual_minute, int) or downtime_duration_actual_minute < 0 or downtime_duration_actual_minute > 59:
    #             #     error_message.append('دقیقه مدت زمان قطعی سیستم نامعتبر است')

    #     return error_message

    # def step_data_save(
    #     self,
    #     action: str,
    #     request: m.ConfigurationChangeRequest,
    #     status: str,
    #     data: dict,
    # ):
    #     # به‌روزرسانی فیلدهای opinion و date بر اساس نقش و action
    #     current_date = jdatetime.datetime.now()
    #     current_time = current_date.strftime("%H:%M")

    #     if status == "MANAGE":
    #         request.manager_opinion = action == "CON"
    #         request.manager_opinion_date = current_date.strftime("%Y/%m/%d")
    #         request.manager_opinion_time = current_time
    #     elif status == "COMITE":
    #         request.committee_opinion = action == "CON"
    #         request.committee_opinion_date = current_date.strftime("%Y/%m/%d")
    #         request.committee_opinion_time = current_time
    #     elif status == "EXECUT":
    #         request.executor_report = action == "CON"
    #         request.executor_report_date = current_date.strftime("%Y/%m/%d")
    #         request.executor_report_time = current_time

    #         request.execution_description = data.get("operation_report")
    #         request.changing_date_actual = data.get("operation_date")
    #         request.changing_time_actual = data.get("operation_time")
    #         request.executor_report = data.get("operation_result")

    #         changing_duration_actual_hour = int(
    #             data.get("changing_duration_actual_hour")
    #         )
    #         changing_duration_actual_minute = int(
    #             data.get("changing_duration_actual_minute")
    #         )
    #         request.changing_duration_actual = (
    #             changing_duration_actual_hour * 60 + changing_duration_actual_minute
    #         )

    #         downtime_duration_actual_hour = int(
    #             data.get("downtime_duration_actual_hour")
    #         )
    #         downtime_duration_actual_minute = int(
    #             data.get("downtime_duration_actual_minute")
    #         )
    #         request.downtime_duration = (
    #             downtime_duration_actual_hour * 60 + downtime_duration_actual_minute
    #         )

    #     elif status == "TESTER":
    #         request.tester_report = action == "CON"
    #         request.tester_report_date = current_date.strftime("%Y/%m/%d")
    #         request.tester_report_time = current_time
    #         request.test_report_description = data.get("operation_report")
    #         request.tester_report = data.get("operation_result")

    #     request.save()

    # def get_previous_status(self, current_status):
    #     # تابعی برای دریافت وضعیت قبلی بر اساس وضعیت فعلی
    #     status_order = ["DRAFTD", "MANAGE", "COMITE", "EXECUT", "TESTER", "FINISH"]
    #     return status_order[status_order.index(current_status) - 1]

    # def get_priority_title(self, priority_id):
    #     # تابعی برای دریافت عنوان اولویت بر اساس شناسه اولویت
    #     priority_instance = m.ConstValue.objects.get(id=priority_id)
    #     return priority_instance.Caption


    def get_form_data(self):
        """
        این تابع اطلاعات ثابت مربوط به درخواست ها، یعنی مقادیر کومبوها و ... را بازگشت می دهد
        """
        data = {"success": True, "message": ""}

        try:
            # فیلتر کردن رکوردهای مربوط به طبقه بندی
            classification_values = m.ConstValue.objects.filter(
                Code__startswith="Classification_", IsActive=True
            )
            classification_default = "Classification_Normal"
            data["classification_values"] = classification_values
            data["classification_default"] = classification_default

            # فیلتر کردن رکوردهای مربوط به دامنه تغییرات
            change_level_values = m.ConstValue.objects.filter(
                Code__startswith="ChangeLevel_", IsActive=True
            )
            change_level_default = "ChangeLevel_Minor"
            data["change_level_values"] = change_level_values
            data["change_level_default"] = change_level_default

            # فیلتر کردن رکوردهای مربوط به اولویت تغییر
            priority_values = m.ConstValue.objects.filter(
                Code__startswith="Priority_", IsActive=True
            )
            priority_default = "Priority_Standard"
            data["priority_values"] = priority_values
            data["priority_default"] = priority_default

            # فیلتر کردن رکوردهای مربوط به سطح ریسک تغییر
            risk_level_values = m.ConstValue.objects.filter(
                Code__startswith="RiskLevel_", IsActive=True
            )
            risk_level_default = "RiskLevel_Low"
            data["risk_level_values"] = risk_level_values
            data["risk_level_default"] = risk_level_default

            # فیلتر کردن رکوردهای مربوط به تغییرات مرکز داده
            data_center_values = m.ConstValue.objects.filter(
                Code__startswith="DataCenter_", IsActive=True
            )
            data["data_center_values"] = data_center_values

            # فیلتر کردن رکوردهای مربوط به سیستم ها و سرویس ها
            system_services_values = m.ConstValue.objects.filter(
                Code__startswith="SystemServices_", IsActive=True
            )
            data["system_services_values"] = system_services_values

            # فیلتر کردن رکوردهای مربوط به محدوده تغییر
            domain_values = m.ConstValue.objects.filter(
                Code__startswith="Domain_", IsActive=True
            )
            data["domain_values"] = domain_values

            # فیلتر کردن رکوردهای مربوط به نوع پیوست
            attachment_type_values = m.ConstValue.objects.filter(
                Code__startswith="AttachmentType_", IsActive=True
            )
            data["attachment_type_values"] = attachment_type_values

            # فیلتر کردن رکوردهای مربوط به وضعیت
            status_values = m.ConstValue.objects.filter(
                Code__startswith="Status_", IsActive=True
            )
            data["status_values"] = status_values

            committee = m.Committee.objects.filter(is_active=True)
            data["committee"] = committee

            corps = m.Corp.objects.all()
            teams = m.Team.objects.filter(is_active=True)
            data["corps"] = corps
            data["teams"] = teams

            # نوع تغییر را از جدول مربوطه می گیریم
            change_type = m.ChangeType.objects.all()
            data["change_type"] = change_type

            # لیست تسک ها را هم اضافه می کنیم
            data["task_list"] = m.Task.objects.all()

            # لیست گروه های اطلاع رسانی را اضافه می کنیم
            data["notify_group_list"] = m.NotifyGroup.objects.all()
            
            
            user_team_roles = m.UserTeamRole.objects.select_related('national_code', 'role_id', 'team_code')
            data["user_team_roles"] = user_team_roles
            
            # لیست همه کاربرانی که فعال هستند را استخراج می کنیم
            utr_list = m.UserTeamRole.objects.select_related('national_code', 'role_id', 'team_code')
                
            # users_dict = defaultdict(list)
            # for utr in utr_list:
            #     user = utr.national_code
            #     users_dict[user.national_code].append({
            #         'role_id': utr.role_id.role_id if utr.role_id else None,
            #         'role_title': utr.role_id.role_title if utr.role_id else '',
            #         'team_code': utr.team_code.team_code if utr.team_code else '',
            #         'team_name': utr.team_code.team_name if utr.team_code else '',
            #     })
            
            # # حالا all_users را آماده می‌کنیم:
            # all_users = []
            # for nc, roles in users_dict.items():
            #     u = m.User.objects.get(national_code=nc)
            #     all_users.append({
            #         'national_code': u.national_code,
            #         'fullname': u.fullname,
            #         'username': u.username,
            #         'roles': roles,
            #     })
                
            # data['all_users'] = all_users


            # واکشی همه روابط بین کاربر، سمت و تیم
            utr_list = m.UserTeamRole.objects.select_related('national_code', 'role_id', 'team_code').all()
            all_user_roles = []
            for utr in utr_list:
                user = utr.national_code
                if not user:
                    continue
                full_display = f"{user.first_name} {user.last_name}"
                if utr.role_id and utr.team_code:
                    full_display += f" ({utr.role_id.role_title} تیم {utr.team_code.team_name})"
                elif utr.role_id:
                    full_display += f" ({utr.role_id.role_title})"
                elif utr.team_code:
                    full_display += f" (تیم {utr.team_code.team_name})"

                all_user_roles.append({
                    "national_code": user.national_code,
                    "full_display": full_display,
                    "fullname":user.fullname,
                    "username": user.username,
                    "role_id": utr.role_id.role_id if utr.role_id else '',
                    "team_code": utr.team_code.team_code if utr.team_code else '',
                    "team_name": utr.team_code.team_name if utr.team_code else '',
                })            
            data["all_user_roles"] = all_user_roles
            
        except Exception as e:
            return {"success": False, "message": str(e)}

        return data

    def __get_user_data(self, user_natioal_code:str)->dict:
        # اطلاعات کاربر جاری را استخراج می کنیم
        obj_user:m.User = m.User.objects.filter(national_code=user_natioal_code).first()
        user_info = {
            "fullname": obj_user.fullname,
            "username": obj_user.username,
            "national_code": obj_user.national_code,
            "gender": obj_user.gender
        }

        # اطلاعات سمت های کاربر جاری را استخراج می کنیم
        obj_team_role:m.UserTeamRole = m.UserTeamRole.objects.filter(national_code=user_natioal_code)
        team_roles = []
        for tr in obj_team_role:
            team_role = {
                    "role_title": tr.role_id.role_title,
                    "role_id": tr.role_id.role_id,
                    "team_name": tr.team_code.team_name,
                    "team_code":  tr.team_code.team_code,
                    "manager_national_code": tr.manager_national_code.national_code,
                }
            team_roles.append(team_role)
        user_info['team_roles'] = team_roles
        
        return user_info

    def get_user_info(self, national_code:str)->dict:
        """
        این تابع اطلاعات یک کاربر و سمت ها و تیم های وی را بازگشت می دهد

        Args:
            national_code (str): کد ملی کاربری که می خواهیم اطلاعات وی را به دست بیاوریم
        """
        data = {"success":True}        
        user = m.User.objects.filter(national_code=national_code).first()
        if not user:
            return {"success":False, "message":":کاربر مورد نظر یافت نشد"}  
        data["user"] = user
        data["team_roles"] = m.UserTeamRole.objects.filter(national_code=national_code)        
        
        return data

    def get_all_user_data(self):
        """
        این تابع اطلاعات کاربر جاری و سایر کاربران مرتبط را بازگشت می دهد
        """
        data = {"success": True, "message": ""}

        try:
           
            # data["current_user"] = self.__get_user_data(self.current_user_national_code)

            # all_users = []
            # users = m.User.objects.all()
            # for u in users:
            #     user_info = self.__get_user_data(u.national_code)
            #     all_users.append(user_info)

            # data["all_users"] = all_users

            data["current_user"] = m.User.objects.filter(national_code=self.current_user_national_code).first()
            data["current_user_team_roles"] = m.UserTeamRole.objects.filter(national_code=self.current_user_national_code)



        except Exception as e:
            return {"success": False, "message": str(e)}

        return data

    # def get_inbox_owners_national_code(
    #     self, status: str, request_instance: m.ConfigurationChangeRequest
    # ) -> str:
    #     # تابعی برای دریافت کد ملی دریافت‌کنندگان بر اساس وضعیت
    #     if status == "MANAGE":
    #         return request_instance.manager_nationalcode.national_code
    #     elif status == "EXECUT":
    #         return request_instance.executor_nationalcode.national_code
    #     elif status == "COMITE":
    #         return request_instance.committee_user_nationalcode.national_code
    #     elif status == "TESTER":
    #         return request_instance.tester_nationalcode.national_code


    def get_dynamic_checkbox(self, type:str, request):
        # دریافت چک باکس‌های داینامیک برای
        values = m.ConstValue.objects.filter(Code__startswith=type+'_', IsActive=True)

        extra_information = []
        for value in values:
            if (request.POST.get(type+'_items_'+value.Code) == value.Code):  # ذخیره وضعیت چک باکس
                extra_information.append(value.id)

        return extra_information

    def get_selected_items(self, team_corp: str, request):
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


    def notify_group_managment(self, request_id:int, notify_group_id:int, operation_type:str='A', request_change_type:str='R')-> dict:
        """
        این تابع گروه اطلاع رسانی های ذیل یک درخواست (یا نوع درخواست) را مدیریت می کند

        Args:

            notify_group_id (int): شناسه گروه اطلاع رسانی مورد نظر در درخواست و یا نوع درخواست
            operation_type (_type_): یکی از موارد زیر است:
                a: اضافه کردن گروه اطلاع رسانی جدید
                d: حذف گروه اطلاع رسانی مربوطه
            request_changetype (str, optional): مشخص کننده این است که این گروه اطلاع رسانی مربوط به درخواست می شود یا مربوط به نوع درخواست
                R: گروه اطلاع رسانی درخواست
                T: گروه اطلاع رسانی نوع درخواست
                        
        Return value:
            یک  جسیون مشابه به مورد زیر شامل این اطلاعات:
                {'success':, 'message':''}
                success: در صورتی که اجرا موفقیت آمیز باشد برابر با True و در غیر این صورت False خواهد بود
                message پیام مرتبط خصوصا در صورت وقوع خطا نشان می دهد که چه خطایی رخ داده است
        
        """
        # برای اینکه تابع با هر یک از این مقادیر ورودی کار کند
        valid_operation_type_add = ['add','a']
        valid_operation_type_delete = ['delete', 'd']
        
        # برای اینکه مشکلی در مقایسه پیش نیاید همه حروف را کوچک می کنیم
        operation_type = operation_type.lower()
        
        # کنترل می کنیم که نوع عملیات مقدار مجاز داشته باشد
        if operation_type not in valid_operation_type_add+valid_operation_type_delete:
            return {'success': False, 'message': 'نوع عملیات نامعتبر است.'}
        
        # کنترل می کنیم که مقدار متغییر آخر که مشخص می کند این تسک مربوط به درخواست است و یا نوع تغییر، معتبر باشد
        if request_change_type not in ['R', 'T']:
            return {'success': False, 'message': 'نوع تسک (درخواست/نوع درخواست) نامعتبر است.'}
        

        # کنترل می کنیم که چنین گروه اطلاع رسانی ای برای چنین درخواست/نوع درخواستی وجود دارد؟
        if request_change_type == 'R':
            # تسک مربوط به درخواست
            exists = m.RequestNotifyGroup.objects.filter(notify_group_id=notify_group_id, request_id=request_id).exists()
        else:
            # تسک مربوط به نوع درخواست
            exists = m.RequestNotifyGroup_ChangeType.objects.filter(notify_group_id=notify_group_id, changetype=request_id).exists()

       
        # اگر گروه اطلاع رسانی ای با این مشخصات تعریف شده است و هدف اضافه کردن است، خطا داریم
        if operation_type in valid_operation_type_add and exists:
            return {'success': False, 'message': 'این تسک قبلاً به این تسک اضافه شده است.'}
        # اگر گروه اطلاع رسانی ای با این مشخصات تعریف نشده باشد و هدف حذف کردن است، خطا داریم 
        elif operation_type in valid_operation_type_delete and not exists:
            return {'success': False, 'message': 'این تسک برای این تسک تعریف نشده است.'}
        
        # اطلاعات رکورد فعلی را برای درج در سوابق به دست می آوریم
        result = self.get_record_json(request_changetype=request_change_type, id=request_id)
        
        if not result.get('success', False):
            return result
        
        if 'record_data' not in result:
            return {'success':False, 'message': 'امکان واکشی اطلاعات جدید رکورد وجود ندارد'}

        old_data = result['record_data']
                
        
        # اگر تغییر، اضافه کردن باشد آن را درج می کنیم
        if operation_type in valid_operation_type_add:
            try:
                if request_change_type == 'R':
                        
                    request_notify_group = m.RequestNotifyGroup.objects.create(
                        notify_group_id=notify_group_id,
                        request_id=request_id,
                    )
                             
                    # در حال حاضر برای یک درخواست کاربر اطلاع رسانی تعریف نمی شود
                    # یعنی اگر کاربری به گروه اضافه شود، به گروه اصلی اضافه می شود
                    # و از این به بعد هر درخواستی از این گروه اطلاع رسانی استفاده کند، شامل این فرد هم می گردد
                    # در صورتی که بعدا نیاز باشد که مانند تسک ها، کاربر انحصاری برای این درخواست تعریف شود
                    # اینجا باید کاربران پیش فرض را درج کنیم
                    # # حالا باید به ازای هر یک از افرادی که به صورت پیش فرض ذیل این تسک تعریف شده اند، یک رکورد در جدول RequestTaskUser درج کنیم
                    # try:
                    #     task_users = m.TaskUser.objects.filter(task_id=task_id)

                    #     # به ازای هر کاربر عملیات درج در تسک جدید را انجام می دهیم
                    #     for task_user in task_users:
                    #         m.RequestTaskUser.objects.create(
                    #                 request_task=request_task,
                    #                 user_nationalcode=task_user.user_nationalcode,
                    #                 user_role_id=task_user.user_role_id,
                    #                 user_team_code=task_user.user_team_code,
                    #                 user_role_code=task_user.user_role_code
                    #             )

                    # except Exception as e:
                    #     return {"success": False, "message": "امکان درج کاربر برای این تسک وجود ندارد<br/>" + str(e)}
                    


                else:
                    request_notify_group = m.RequestNotifyGroup_ChangeType.objects.create(
                        notify_group_id=notify_group_id,
                        changetype_id=request_id,
                    )
                        

                # لیست کاربران مربوط به این گروه اطلاع رسانی را باید به خروجی ارسال کنیم
                # چون fullname یک property است و فیلد دیتابیس نیست، نمی‌توانیم آن را با values بگیریم.
                # بنابراین باید ابتدا آبجکت‌ها را بگیریم و سپس مقدار property را دستی اضافه کنیم.
                notify_users_qs = m.NotifyGroupUser.objects.filter(
                    notify_group_id = notify_group_id
                ).select_related('user_nationalcode')                                            
                    
                notify_users = []
                for notify_user in notify_users_qs:
                    notify_users.append({
                        'id': notify_user.id,
                        'notify_group_id': notify_user.notify_group.id,
                        'user_nationalcode': notify_user.user_nationalcode_id,
                        'user_role_id': notify_user.user_role_id_id,
                        'user_team_code': notify_user.user_team_code_id,
                        'user_nationalcode__username': notify_user.user_nationalcode.username if notify_user.user_nationalcode else None,
                        'user_nationalcode__fullname': notify_user.user_nationalcode.fullname if notify_user.user_nationalcode else None,
                    })

                user_team_roles = m.UserTeamRole.objects.select_related('national_code', 'team_code', 'role_id').values(
                    'id',
                    'national_code',  # کد ملی کاربر
                    'role_id',        # شناسه سمت
                    'team_code',      # کد تیم
                    'manager_national_code',
                    # فیلدهای اضافه شده:
                    'national_code__username',   # نام کامل کاربر
                    'national_code__first_name',   # نام کامل کاربر
                    'national_code__last_name',   # نام کامل کاربر
                    'team_code__team_name',      # نام تیم
                    'role_id__role_title',       # عنوان سمت
                )

                # اطلاعات جدید را برای ذخیره در سوابق دریافت می کنیم
                result = self.get_record_json(request_changetype=request_change_type, id=request_id)
                
                if not result.get('success', False):
                    return result
                
                if 'record_data' not in result:
                    return {'success':False, 'message': 'امکان واکشی اطلاعات جدید رکورد وجود ندارد'}

                new_data = result['record_data']
                
                # # تبدیل به JSON با حفظ حروف فارسی
                # new_data = json.loads(json.dumps(new_data, ensure_ascii=False))
                # old_data = json.loads(json.dumps(old_data, ensure_ascii=False))
                # حالا اطلاعات سوابق تغییرات را در جدول مربوطه درج می کنیم
                try:
                    m.DataHistory.objects.create(
                        record_type=request_change_type,
                        old_data= old_data or {},
                        new_data= new_data or {},
                        record_id=request_id,
                        creator_user_id=self.current_user_national_code,
                        last_modifier_user_id=self.current_user_national_code
                    )                    

                    return {'success': True, 'message': 'گروه اطلاع رسانی مورد نظر با موفقیت به درخواست اضافه شد.',
                            'request_notify_group_id':request_notify_group.id,
                            'role_title':request_notify_group.notify_group.role_id.role_title if request_notify_group.notify_group.role_id else '-',
                            'role_id':request_notify_group.notify_group.role_id.role_id if request_notify_group.notify_group.role_id else '-',
                            'team_name':request_notify_group.notify_group.team_code.team_name if request_notify_group.notify_group.team_code else None,
                            'team_code':request_notify_group.notify_group.team_code.team_code if request_notify_group.notify_group.team_code else None,
                            'request_id':request_id,
                            'notify_group_id':notify_group_id,
                            'notify_group_title':request_notify_group.notify_group.title,
                            'notify_users':list(notify_users),
                            'user_team_roles':list(user_team_roles),
                            'by_email':request_notify_group.by_email,
                            'by_sms':request_notify_group.by_sms,
                            'by_phone':request_notify_group.by_phone,
                            }

                except Exception as e:
                    return {'success': False, 'message': f'خطا در ثبت سوابق: {str(e)}'}
            except Exception as e:
                return {'success': False, 'message': f'خطا در افزودن گروه اطلاع رسانی: {str(e)}'}
            
        # در صورتی که حذف کاربر باشد، بر مبنای اینکه گروه اطلاع رسانی مربوط به درخواست تغییر است یا نوع تغییر زکوزد مربوطه حذ می شود.
        if operation_type in valid_operation_type_delete:
            try:
                if request_change_type == 'R':
                    m.RequestNotifyGroup.objects.filter(notify_group_id=notify_group_id, request_id=request_id).delete()
                else:
                    m.RequestNotifyGroup_ChangeType.objects.filter(notify_group_id=notify_group_id, changetype=request_id).delete()

            except Exception as e:
                return {'success': False, 'message': f'خطا در حذف گروه اطلاع رسانی: {str(e)}'}        
            result = self.get_record_json(request_changetype=request_change_type, id=request_id)
            
            if not result.get('success', False):
                return result
            
            if 'record_data' not in result:
                return {'success':False, 'message': 'امکان واکشی اطلاعات جدید رکورد وجود ندارد'}

            new_data = result['record_data']
            
            # # تبدیل به JSON با حفظ حروف فارسی
            # new_data = json.loads(json.dumps(new_data, ensure_ascii=False))
            # old_data = json.loads(json.dumps(old_data, ensure_ascii=False))
            # حالا اطلاعات سوابق تغییرات را در جدول مربوطه درج می کنیم
            try:
                m.DataHistory.objects.create(
                    record_type=request_change_type,
                    old_data= old_data or {},
                    new_data= new_data or {},
                    record_id=request_id,
                    creator_user_id=self.current_user_national_code,
                    last_modifier_user_id=self.current_user_national_code
                )                    
            except Exception as e:
                return {'success': False, 'message': f'خطا در ثبت سوابق: {str(e)}'}

                                
            return {'success': True, 'message': 'گروه اطلاع رسانی مورد نظر با موفقیت از درخواست حذف شد.'}


    def task_management(self, request_id:int, task_id:int, operation_type:str='A', request_change_type:str='R')-> dict:
        """
        این تابع تسک های ذیل یک درخواست (یا نوع درخواست) را مدیریت می کند

        Args:

            task_id (int): شناسه تسک مورد نظر در درخواست و یا نوع درخواست
            operation_type (_type_): یکی از موارد زیر است:
                a: اضافه کردن تسک جدید
                d: حذف تسک مربوطه
            request_changetype (str, optional): مشخص کننده این است که این تسک مربوط به درخواست می شود یا مربوط به نوع درخواست
                R: تسک درخواست
                T: تسک نوع درخواست
                        
        Return value:
            یک  جسیون مشابه به مورد زیر شامل این اطلاعات:
                {'success':, 'message':''}
                success: در صورتی که اجرا موفقیت آمیز باشد برابر با True و در غیر این صورت False خواهد بود
                message پیام مرتبط خصوصا در صورت وقوع خطا نشان می دهد که چه خطایی رخ داده است
        
        """
        # برای اینکه تابع با هر یک از این مقادیر ورودی کار کند
        valid_operation_type_add = ['add','a']
        valid_operation_type_delete = ['delete', 'd']
        
        # برای اینکه مشکلی در مقایسه پیش نیاید همه حروف را کوچک می کنیم
        operation_type = operation_type.lower()
        
        # کنترل می کنیم که نوع عملیات مقدار مجاز داشته باشد
        if operation_type not in valid_operation_type_add+valid_operation_type_delete:
            return {'success': False, 'message': 'نوع عملیات نامعتبر است.'}
        
        # کنترل می کنیم که مقدار متغییر آخر که مشخص می کند این تسک مربوط به درخواست است و یا نوع تغییر، معتبر باشد
        if request_change_type not in ['R', 'T']:
            return {'success': False, 'message': 'نوع تسک (درخواست/نوع درخواست) نامعتبر است.'}
        

        # کنترل می کنیم که چنین تسکی برای چنین درخواست/نوع درخواستی وجود دارد؟
        if request_change_type == 'R':
            # تسک مربوط به درخواست
            exists = m.RequestTask.objects.filter(task_id=task_id, request_id=request_id).exists()
        else:
            # تسک مربوط به نوع درخواست
            exists = m.RequestTask_ChangeType.objects.filter(taks_id=task_id, changetype=request_id).exists()

       
        # اگر تسکی با این مشخصات تعریف شده است و هدف اضافه کردن است، خطا داریم
        if operation_type in valid_operation_type_add and exists:
            return {'success': False, 'message': 'این تسک قبلاً به این تسک اضافه شده است.'}
        # اگر تسکی با این مشخصات تعریف نشده باشد و هدف حذف کردن است، خطا داریم 
        elif operation_type in valid_operation_type_delete and not exists:
            return {'success': False, 'message': 'این تسک برای این تسک تعریف نشده است.'}
        
        # اطلاعات رکورد فعلی را جهت درج در سوابق ذخیره می کنیم
        result = self.get_record_json(request_changetype=request_change_type, id=request_id)
        
        if not result.get('success', False):
            return result
        
        if 'record_data' not in result:
            return {'success':False, 'message': 'امکان واکشی اطلاعات جدید رکورد وجود ندارد'}

        old_data = result['record_data']
                
        # اگر هدف اضافه کردن تسک باشد
        if operation_type in valid_operation_type_add:
            try:
                if request_change_type == 'R':
                    # ابتدا آخرین شماره ترتیب را به دست می‌آوریم
                    last_task = m.RequestTask.objects.filter(request_id=request_id).order_by('-order_number').first()
                    if last_task is not None and last_task.order_number:
                        order_number = last_task.order_number + 1
                    else:
                        order_number = 1
                        
                    request_task = m.RequestTask.objects.create(
                        task_id=task_id,
                        request_id=request_id,
                        status_code='DEFINE',
                        order_number=order_number
                    )
                    
                                        
                    # حالا باید به ازای هر یک از افرادی که به صورت پیش فرض ذیل این تسک تعریف شده اند، یک رکورد در جدول RequestTaskUser درج کنیم
                    try:
                        task_users = m.TaskUser.objects.filter(task_id=task_id)

                        # به ازای هر کاربر عملیات درج در تسک جدید را انجام می دهیم
                        for task_user in task_users:
                            m.RequestTaskUser.objects.create(
                                    request_task=request_task,
                                    user_nationalcode=task_user.user_nationalcode,
                                    user_role_id=task_user.user_role_id,
                                    user_team_code=task_user.user_team_code,
                                    user_role_code=task_user.user_role_code
                                )

                    except Exception as e:
                        return {"success": False, "message": "امکان درج کاربر برای این تسک وجود ندارد<br/>" + str(e)}
                    
                    # لیست مجریان و تسترها را باید به خروجی ارسال کنیم
                    # چون fullname یک property است و فیلد دیتابیس نیست، نمی‌توانیم آن را با values بگیریم.
                    # بنابراین باید ابتدا آبجکت‌ها را بگیریم و سپس مقدار property را دستی اضافه کنیم.
                    executors_qs = m.RequestTaskUser.objects.filter(
                        user_role_code="E",
                        request_task__task_id=task_id,
                        request_task__request_id=request_id
                    ).select_related('user_nationalcode')

                    testers_qs = m.RequestTaskUser.objects.filter(
                        user_role_code="T",
                        request_task__task_id=task_id,
                        request_task__request_id=request_id
                    ).select_related('user_nationalcode')


                else:
                    # ابتدا آخرین شماره ترتیب را به دست می‌آوریم
                    last_task = m.RequestTask_ChangeType.objects.filter(changetype_id=request_id).order_by('-order_number').first()
                    if last_task is not None and last_task.order_number:
                        order_number = last_task.order_number + 1
                    else:
                        order_number = 1
                                            
                    executors_qs = m.TaskUser.objects.filter(
                        user_role_code="E",
                        task_id=task_id,
                    ).select_related('user_nationalcode')

                    testers_qs = m.TaskUser.objects.filter(
                        user_role_code="T",
                        task_id=task_id,
                    ).select_related('user_nationalcode')

                    
                executors = []
                for executor in executors_qs:
                    executors.append({
                        'id': executor.id,
                        'request_task_id': executor.request_task_id,
                        'user_nationalcode': executor.user_nationalcode_id,
                        'user_role_id': executor.user_role_id_id,
                        'user_team_code': executor.user_team_code_id,
                        'user_role_code': executor.user_role_code,
                        'user_nationalcode__username': executor.user_nationalcode.username if executor.user_nationalcode else None,
                        'user_nationalcode__fullname': executor.user_nationalcode.fullname if executor.user_nationalcode else None,
                    })

                testers = []
                for tester in testers_qs:
                    testers.append({
                        'id': tester.id,
                        'request_task_id': tester.request_task_id,
                        'user_nationalcode': tester.user_nationalcode_id,
                        'user_role_id': tester.user_role_id_id,
                        'user_team_code': tester.user_team_code_id,
                        'user_role_code': tester.user_role_code,
                        'user_nationalcode__username': tester.user_nationalcode.username if tester.user_nationalcode else None,
                        'user_nationalcode__fullname': tester.user_nationalcode.fullname if tester.user_nationalcode else None,
                    })

                user_team_roles = m.UserTeamRole.objects.select_related('national_code', 'team_code', 'role_id').values(
                    'id',
                    'national_code',  # کد ملی کاربر
                    'role_id',        # شناسه سمت
                    'team_code',      # کد تیم
                    'manager_national_code',
                    # فیلدهای اضافه شده:
                    'national_code__username',   # نام کامل کاربر
                    'national_code__first_name',   # نام کامل کاربر
                    'national_code__last_name',   # نام کامل کاربر
                    'team_code__team_name',      # نام تیم
                    'role_id__role_title',       # عنوان سمت
                )

            
                # وضعیت جدید رکورد را جهت درج در سوابق به دست می آوریم
                result = self.get_record_json(request_changetype=request_change_type, id=request_id)
                
                if not result.get('success', False):
                    return result
                
                if 'record_data' not in result:
                    return {'success':False, 'message': 'امکان واکشی اطلاعات جدید رکورد وجود ندارد'}

                old_data = result['record_data']

                # # تبدیل به JSON با حفظ حروف فارسی
                # new_data = json.loads(json.dumps(new_data, ensure_ascii=False))
                # old_data = json.loads(json.dumps(old_data, ensure_ascii=False))
                # حالا اطلاعات سوابق تغییرات را در جدول مربوطه درج می کنیم
                try:
                    m.DataHistory.objects.create(
                        record_type=request_change_type,
                        old_data= old_data or {},
                        new_data= new_data or {},
                        record_id=request_id,
                        creator_user_id=self.current_user_national_code,
                        last_modifier_user_id=self.current_user_national_code
                    )                    

                    return {'success': True, 'message': 'تسک مورد نظر با موفقیت به درخواست اضافه شد.',
                            'request_task_id':request_task.id,
                            'request_id':request_id,
                            'task_id':task_id,
                            'task_title':request_task.task.title,
                            'executors':list(executors),
                            'testers':list(testers),
                            'user_team_roles':list(user_team_roles),
                            }

                except Exception as e:
                    return {'success': False, 'message': f'خطا در ثبت سوابق: {str(e)}'}
            except Exception as e:
                return {'success': False, 'message': f'خطا در افزودن تسک: {str(e)}'}
            
        # در صورتی که حذف کاربر باشد، بر مبنای اینکه تسک مربوط به درخواست تغییر است یا نوع تغییر زکوزد مربوطه حذ می شود.
        if operation_type in valid_operation_type_delete:
            try:
                if request_change_type == 'R':
                    m.RequestTask.objects.filter(task_id=task_id, request_id=request_id).delete()
                else:
                    m.RequestTask_ChangeType.objects.filter(task_id=task_id, changetype=request_id).delete()

            except Exception as e:
                return {'success': False, 'message': f'خطا در حذف تسک: {str(e)}'}        
            result = self.get_record_json(request_changetype=request_change_type, id=request_id)
            
            if not result.get('success', False):
                return result
            
            if 'record_data' not in result:
                return {'success':False, 'message': 'امکان واکشی اطلاعات جدید رکورد وجود ندارد'}

            new_data = result['record_data']
            
            # # تبدیل به JSON با حفظ حروف فارسی
            # new_data = json.loads(json.dumps(new_data, ensure_ascii=False))
            # old_data = json.loads(json.dumps(old_data, ensure_ascii=False))
            # حالا اطلاعات سوابق تغییرات را در جدول مربوطه درج می کنیم
            try:
                m.DataHistory.objects.create(
                    record_type=request_change_type,
                    old_data= old_data or {},
                    new_data= new_data or {},
                    record_id=request_id,
                    creator_user_id=self.current_user_national_code,
                    last_modifier_user_id=self.current_user_national_code
                )                    
            except Exception as e:
                return {'success': False, 'message': f'خطا در ثبت سوابق: {str(e)}'}

                                
            return {'success': True, 'message': 'تسک مورد نظر با موفقیت از درخواست حذف شد.'}


    def task_user_management(self, task_id:int,  operation_type:str='A', user_national_code:str='', user_role_id:int=-1, user_team_code:str='', user_role_code:str='E', request_change_type:str='R')-> dict:
        """
        این تابع افراد ذیل یک تسک را مدیریت می کند.

        Args:
            request (_type_): درخواست http
            task_id (int): شناسه تسک مورد نظر در درخواست و یا نوع درخواست
            operation_type (_type_): یکی از موارد زیر است:
                a: اضافه کردن کاربر جدید
                d: حذف کاربر مربوطه
            user_national_code (کد ملی کاربر): کد ملی کاربر مورد نظر
            request_changetype (str, optional): مشخص کننده این است که این تسک مربوط به درخواست می شود یا مربوط به نوع درخواست
                R: تسک درخواست
                T: تسک نوع درخواست
                        
        Return value:
            یک  جسیون مشابه به مورد زیر شامل این اطلاعات:
                {'success':, 'message':''}
                success: در صورتی که اجرا موفقیت آمیز باشد برابر با True و در غیر این صورت False خواهد بود
                message پیام مرتبط خصوصا در صورت وقوع خطا نشان می دهد که چه خطایی رخ داده است
        
        """
        # برای اینکه تابع با هر یک از این مقادیر ورودی کار کند
        valid_operation_type_add = ['add','a']
        valid_operation_type_delete = ['delete', 'd']
        
        # برای اینکه مشکلی در مقایسه پیش نیاید همه حروف را کوچک می کنیم
        operation_type = operation_type.lower()
        # کد تیم  کد نوع سمت را بزرگ می کنیم
        user_team_code = user_team_code.upper()
        user_role_code = user_role_code.upper()
        
        # کنترل می کنیم که نوع عملیات مقدار مجاز داشته باشد
        if operation_type not in valid_operation_type_add+valid_operation_type_delete:
            return {'success': False, 'message': 'نوع عملیات نامعتبر است.'}
        
        # کنترل می کنیم که مقدار متغییر آخر که مشخص می کند این تسک مربوط به درخواست است و یا نوع تغییر، معتبر باشد
        if request_change_type not in ['R', 'T']:
            return {'success': False, 'message': 'نوع تسک (درخواست/نوع درخواست) نامعتبر است.'}


        # با توجه به اینکه تسک مربوط به نوع درخواست و یا درخواست است، کنترل می کنیم که شناسه تسک معتبر باشد.
        id = -1 
        try:
            if request_change_type == 'R':
                # تسک مربوط به درخواست
                task_instance = m.RequestTask.objects.get(pk=task_id)
                id = task_instance.request_id
            else:
                # تسک مربوط به نوع درخواست
                task_instance = m.RequestTask_ChangeType.objects.get(pk=task_id)
                id = task_instance.changetype_id
        except Exception:
            return {'success': False, 'message': 'شناسه تسک نامعتبر است.'}
        

        
        # اطلاعات رکورد  فعلی را جهت ثبت در سوابق استخراج می کنیم
        result = self.get_record_json(request_changetype=request_change_type, id=id)
        if not result.get('success', False):
            return result
        
        if 'record_data' not in result:
            return {'success':False, 'message': 'امکان واکشی اطلاعات جدید رکورد وجود ندارد'}

        old_data = result['record_data']        
        
        # کنترل می کنیم که کد ملی معتبر باشد
        try:
            user_instance = m.User.objects.get(national_code=user_national_code)

        except m.User.DoesNotExist:
            return {'success': False, 'message': 'کد ملی کاربر نامعتبر است.'}
        
        # کنترل می کنیم که کاربری با این مشخصات برای این تسک تعریف شده است یا خیر
        if request_change_type == 'R':
            exists = m.RequestTaskUser.objects.filter(request_task=task_instance, user_nationalcode=user_instance, user_role_code=user_role_code).exists()
        else:
            exists = m.TaskUser.objects.filter(request_task=task_instance, user_nationalcode=user_instance, user_role_code=user_role_code).exists()
        
        # اگر کاربری با این مشخصات تعریف شده است و هدف اضافه کردن است، خطا داریم
        if operation_type in valid_operation_type_add and exists:
            return {'success': False, 'message': 'این کاربر قبلاً به این تسک اضافه شده است.'}
        # اگر کاربری با این مشخصات تعریف نشده باشد و هدف حذف کردن است، خطا داریم 
        elif operation_type in valid_operation_type_delete and not exists:
            return {'success': False, 'message': 'این کاربر برای این تسک تعریف نشده است.'}
        
        
        # اگر تغییر اضافه کردن کاربر جدید است، با توجه به اینکه موضوع مربوط به شناسه تسک و نوع تغییر است یا شناسه تسک درخواست، 
        # اگر کد ملی قبلا برای این کاربر درج نشده باشد، عملیات درج را انجام می دهد
        if operation_type in valid_operation_type_add:
            try:
                if request_change_type == 'R':
                    m.RequestTaskUser.objects.create(
                        request_task=task_instance,
                        user_nationalcode=user_instance,
                        user_role_id_id=user_role_id,
                        user_team_code_id=user_team_code,
                        user_role_code=user_role_code,
                    )

                else:
                    m.TaskUser.objects.create(
                        task_id=task_instance,
                        user_nationalcode=user_instance,
                        user_role_id_id=user_role_id,
                        user_team_code_id=user_team_code,
                        user_role_code=user_role_code,
                    )

                # اطلاعات رکورد  جدید را جهت ثبت در سوابق استخراج می کنیم
                result = self.get_record_json(request_changetype=request_change_type, id=id)
                if not result.get('success', False):
                    return result
                
                if 'record_data' not in result:
                    return {'success':False, 'message': 'امکان واکشی اطلاعات جدید رکورد وجود ندارد'}

                new_data = result['record_data']
                
                # # تبدیل به JSON با حفظ حروف فارسی
                # new_data = json.loads(json.dumps(new_data, ensure_ascii=False))
                # old_data = json.loads(json.dumps(old_data, ensure_ascii=False))
                # حالا اطلاعات سوابق تغییرات را در جدول مربوطه درج می کنیم
                try:
                    m.DataHistory.objects.create(
                        record_type=request_change_type,
                        old_data= old_data or {},
                        new_data= new_data or {},
                        record_id=id,
                        creator_user_id=self.current_user_national_code,
                        last_modifier_user_id=self.current_user_national_code
                    )                    
                except Exception as e:
                    return {'success': False, 'message': f'خطا در ثبت سوابق: {str(e)}'}
                    
                    
                return {'success': True, 'message': 'کاربر با موفقیت به تسک اضافه شد.',
                        'request_task':task_id,
                        'nationalcode':user_national_code,
                        'role_id':user_role_id,
                        'team_code':user_team_code,
                        'role_code':user_role_code,  
                        'fullname':user_instance.fullname,
                        'username':user_instance.username                      
                        }
            except Exception as e:
                return {'success': False, 'message': f'خطا در افزودن کاربر: {str(e)}'}


            
        # در صورتی که حذف کاربر باشد، بر مبنای اینکه تسک مربوط به درخواست تغییر است یا نوع تغییر زکوزد مربوطه حذ می شود.
        if operation_type in ['delete', 'd']:
            try:
                if request_change_type == 'R':
                    m.RequestTaskUser.objects.filter(
                        request_task=task_instance,
                        user_nationalcode=user_instance,
                        user_role_code = user_role_code
                   ).delete()
                else:
                    m.TaskUser.objects.filter(
                        task_id=task_instance,
                        user_nationalcode=user_instance,
                        user_role_code = user_role_code
                    ).delete()
                    
              # اطلاعات رکورد  جدید را جهت ثبت در سوابق استخراج می کنیم
                result = self.get_record_json(request_changetype=request_change_type, id=id)
                if not result.get('success', False):
                    return result
                
                if 'record_data' not in result:
                    return {'success':False, 'message': 'امکان واکشی اطلاعات جدید رکورد وجود ندارد'}

                new_data = result['record_data']
                
                # # تبدیل به JSON با حفظ حروف فارسی
                # new_data = json.loads(json.dumps(new_data, ensure_ascii=False))
                # old_data = json.loads(json.dumps(old_data, ensure_ascii=False))
                # حالا اطلاعات سوابق تغییرات را در جدول مربوطه درج می کنیم
                try:
                    m.DataHistory.objects.create(
                        record_type=request_change_type,
                        old_data= old_data or {},
                        new_data= new_data or {},
                        record_id=id,
                        creator_user_id=self.current_user_national_code,
                        last_modifier_user_id=self.current_user_national_code
                    )                    
                except Exception as e:
                    return {'success': False, 'message': f'خطا در ثبت سوابق: {str(e)}'}
                    
                                        
                return {'success': True, 'message': 'کاربر با موفقیت از تسک حذف شد.'}
            except Exception as e:
                return {'success': False, 'message': f'خطا در حذف کاربر: {str(e)}'}        


    def get_record_json(self, request_changetype: str, id: int)->dict:
        """
        این تابع برای تبدیل داده های مرتبط با یک درخواست یا نوع درخواست در قالب جیسون در راستای ذخیره سازی برای سوابق تغییرات استفاده می شود

        Args:
            request_changetype (str): یک کارکتر که مشخص می کند باید اطلاعات رکورد درخواست به روزرسانی شود یا اطلاعات رکورد نوع درخواست
            R: Request
            C: ChangeType
            form_data (dict): داده های فرم است که باید به روزرسانی شود
            id (int): شناسه رکورد مورد نظر است که باید به روزرسانی شود

        Returns:
            dict: یک دیکشنری با قالب زیر است:
            {'success':True, 'message':'با موفقیت انجام شد', 'record_data':record_data}
        """
  
        # مقدار متغییر request_change_type را بررسی می کنیم که معتبر باشد
        # می تواند یکی از این دو مقدار را داشته باشد:
        # R: برای درخواست
        # C: برای نوع تغییرات
        if request_changetype not in ['R', 'C']:
            return {"success": False, "message": "نوع رکورد ارسالی نامعتبر است. مقدار باید یکی از 'R' یا 'C' باشد."}


        # 2- مقدار شناسه ارسالی id را کنترل می کنیم
        # اگر درخواست باشد، باید شناسه در جدول مربوطه وجود داشته باشد
        # اگر نوع تغییر باشد، یا باید -1 باشد که یعنی رکورد جدید درج شود، یا اگر مقدار عددی داشته باشد باید در جدول وجود داشته باشد.
        if request_changetype == 'R':
            try:
                record_instance = m.ConfigurationChangeRequest.objects.get(id=id)
            except m.ConfigurationChangeRequest.DoesNotExist:
                return {"success": False, "message": "درخواست مورد نظر یافت نشد."}
        else:  # 'C'
            if id == -1:
                return {"success": True, "message": "رکورد تازه فاقد اطلاعات است.", 'record_data':{}}
            else:
                try:
                    record_instance = m.ChangeType.objects.get(id=id)
                except m.ChangeType.DoesNotExist:
                    return {"success": False, "message": "نوع تغییر مورد نظر یافت نشد."}

        # 3- مقدار فعلی داده ها باید در یک متغییر به نام old_data ذخیره شود
        # باید داده های رکورد اصلی به صورت json تبدیل شود
        #  سایر جداول وابسته مثل شرکت های مرتبط و ... هم باید به صورت جیسون به داده های قبلی اضافه شود
        import json
        from django.core import serializers

        record_data = {}
        try:
            # داده های رکورد اصلی
            # record_data['main'] = json.loads(serializers.serialize('json', [record_instance]))[0]['fields']
            from django.forms.models import model_to_dict
            record_data['main'] = model_to_dict(record_instance)
            
            # اطلاعات تکمیلی را اضافه می کنیم

            # اطلاعات شرکت های مرتبط
            if request_changetype == 'R':
                corp_records = m.RequestCorp.objects.filter(request=record_instance)
            else:
                corp_records = m.RequestCorp_ChangeType.objects.filter(changetype=record_instance)
            corp_list = [rec['fields'] for rec in json.loads(serializers.serialize('json', corp_records))]
            record_data['corps'] = corp_list

            # تیم های مرتبط
            if request_changetype == 'R':
                team_records = m.RequestTeam.objects.filter(request=record_instance)
            else:
                team_records = m.RequestTeam_ChangeType.objects.filter(changetype=record_instance)
            team_list = [rec['fields'] for rec in json.loads(serializers.serialize('json', team_records))]
            record_data['teams'] = team_list

            # اطلاعات اضافه
            if request_changetype == 'R':
                extra_info_records = m.RequestExtraInformation.objects.filter(request=record_instance)
            else:
                extra_info_records = m.RequestExtraInformation_ChangeType.objects.filter(changetype=record_instance)
            extra_info_list = [rec['fields'] for rec in json.loads(serializers.serialize('json', extra_info_records))]
            record_data['extra_information'] = extra_info_list

            # اطلاعات تسک ها به همراه کاربران هر تسک
            task_list = []
            if request_changetype == 'R':
                task_records = m.RequestTask.objects.filter(request=record_instance)
            else:
                task_records = m.RequestTask_ChangeType.objects.filter(changetype=record_instance)
            for rec in json.loads(serializers.serialize('json', task_records)):
                task_fields = rec['fields']
                task_id = rec['pk']
                # دریافت کاربران مرتبط با هر تسک
                if request_changetype == 'R':
                    user_records = m.RequestTaskUser.objects.filter(request_task_id=task_id)
                else:
                    user_records = m.TaskUser.objects.filter(task_id=task_id)
                user_list = [user_rec['fields'] for user_rec in json.loads(serializers.serialize('json', user_records))]
                task_fields['users'] = user_list
                task_list.append(task_fields)
            record_data['task'] = task_list

            # اطلاعات گروه های اطلاع رسانی
            if request_changetype == 'R':
                notify_group_records = m.RequestNotifyGroup.objects.filter(request=record_instance)
            else:
                notify_group_records = m.RequestNotifyGroup_ChangeType.objects.filter(changetype=record_instance)
            notify_group_list = [rec['fields'] for rec in json.loads(serializers.serialize('json', notify_group_records))]
            record_data['notify_group'] = notify_group_list
        except Exception as e:
            return {"success":False, "error": f"خطا در دریافت داده‌های قبلی: {str(e)}"}
        
        
        return {'success':True, 'message':'با موفقیت واکشی شد','record_data':json.loads(json.dumps(record_data, ensure_ascii=False))}
 
 
    def update_extra_information(self,form_data:dict, code:str,field_value:bool, request_changetype:str, id:int)->dict:
        """
        این تابع اطلاعات اضافی مربوط به محل تغییر را از داده های ورودی استخراج می کند

        Args:
            form_data (dict): اطلاعات ورودی از فرم
            code (str): مشخص می کند که مثلا اطلاعات مربوط به دیتاسنتر، یا سیستم ها و ... را استخراج کنیم
                DataCenter : تغییرات مرکز داده
                SystemsServices : سیستم ها و سرویس ها
                Database : دیتابیس ها
            field_value: در صورتی که این فیلد  در ورودی باشد و مقدار صحیح داشته باشد صحیح و در غیر این صورت مقدار false برمی گرداند
            request_changetype (str): یک کارکتر که مشخص می کند باید اطلاعات رکورد درخواست به روزرسانی شود یا اطلاعات رکورد نوع درخواست
                R: Request
                C: ChangeType
            id (int): شناسه رکورد مورد نظر است که باید به روزرسانی شود
        
        Returns:
            dict: یک دیکشنری با قالب زیر است:
            {'success':True, 'message':'با موفقیت انجام شد'}
        """
        
        if request_changetype == 'R':
            try:
                record_instance = m.ConfigurationChangeRequest.objects.get(id=id)
            except m.ConfigurationChangeRequest.DoesNotExist:
                return {"success": False, "message": "درخواست مورد نظر یافت نشد."}
        else:  # 'C'
            try:
                record_instance = m.ChangeType.objects.get(id=id)
            except m.ChangeType.DoesNotExist:
                return {"success": False, "message": "نوع تغییر مورد نظر یافت نشد."}
                
                        
        # رکوردهای متناظر را از جدول مقادیر ثابت استخراج می کنیم
        # مثلا انواع تغییراتی که در دیتاسنتر می تواند اتفاق بیافتد
        # مثلا اگر مقدار کد برابر با DataCenter 
        # است، رکوردهایی با مقادیر 
        # DataCenter_Telecommunications و DataCenter_Networking 
        # بازگشت داده شوند.
        const_value_records = m.ConstValue.objects.filter(Code__startswith=code + '_', IsActive=True).order_by('OrderNumber')
        # شناسه رکوردهای مربوطه را به دست می آوریم
        const_value_ids = [rec.id for rec in const_value_records]

        # اگر گزینه تغییرات در دیتاسنترها انتخاب شده باشد
        if field_value:
            # به ازای هر یک از شناسه های مقادیر ثابت مربوطه
            for const_id in const_value_ids:
                # اگر در مقادیر ورودی باشد
                if const_id in form_data.get('extra_information',[]):
                    # کنترل می کنیم که آیا در رکوردهای موجود هست یا خیر
                    if request_changetype == 'R':
                        exists = m.RequestExtraInformation.objects.filter(extra_info_id=const_id, request=record_instance)
                        # اگر در رکوردهای موجود نباشد باید درج شود
                        if not exists:
                            m.RequestExtraInformation.objects.create(extra_info_id=const_id, request=record_instance)
                    else:
                        exists = m.RequestExtraInformation_ChangeType.objects.filter(extra_info_id=const_id, change_type=record_instance)
                        # اگر در رکوردهای موجود نباشد باید درج شود
                        if not exists:
                            m.RequestExtraInformation_ChangeType.objects.create(extra_info_id=const_id, change_type=record_instance)
                # اگر در داده های ورودی نباشد
                else:
                    # اگر در داده های موجود هست، آن را حذف می کنیم
                    if request_changetype == 'R':
                        m.RequestExtraInformation.objects.filter(extra_info_id=const_id, request=record_instance).delete()
                    else:
                        exists = m.RequestExtraInformation_ChangeType.objects.filter(extra_info_id=const_id, change_type=record_instance).delete()
        # اگر در داده های ورودی نیست هم باید رکوردها حذف شوند
        else:
            if request_changetype == 'R':
                m.RequestExtraInformation.objects.filter(extra_info_id__in=const_value_ids, request=record_instance).delete()
            else:
                m.RequestExtraInformation_ChangeType.objects.filter(extra_info_id__in=const_value_ids, change_type=record_instance).delete()              
        
        
        return {'success':True, 'message':'با موفقیت انجام شد'}

    def update_record(self, request_changetype: str, form_data: dict, id: int, current_user_nationalcode: str) -> dict:
        """
        این تابع برای به روزرسانی اطلاعات درخواست، یا نوع درخواست استفاده می شود
        چون عملیات مشترک است به جای پیاده سازی تکراری یک تابع عمومی داریم که در هر دو حالت استفاده می شود

        Args:
            request_changetype (str): یک کارکتر که مشخص می کند باید اطلاعات رکورد درخواست به روزرسانی شود یا اطلاعات رکورد نوع درخواست
                R: Request
                C: ChangeType
            form_data (dict): داده های فرم است که باید به روزرسانی شود
            id (int): شناسه رکورد مورد نظر است که باید به روزرسانی شود

        Returns:
            dict: یک دیکشنری با قالب زیر است:
            {'success':True, 'message':'با موفقیت انجام شد'}
        """

        # مقدار متغییر request_change_type را بررسی می کنیم که معتبر باشد
        # می تواند یکی از این دو مقدار را داشته باشد:
        # R: برای درخواست
        # C: برای نوع تغییرات
        if request_changetype not in ['R', 'C']:
            return {"success": False, "message": "نوع رکورد ارسالی نامعتبر است. مقدار باید یکی از 'R' یا 'C' باشد."}

        # 2- مقدار شناسه ارسالی id را کنترل می کنیم
        # اگر درخواست باشد، باید شناسه در جدول مربوطه وجود داشته باشد
        # اگر نوع تغییر باشد، یا باید -1 باشد که یعنی رکورد جدید درج شود، یا اگر مقدار عددی داشته باشد باید در جدول وجود داشته باشد.
        if request_changetype == 'R':
            try:
                record_instance = m.ConfigurationChangeRequest.objects.get(id=id)
            except m.ConfigurationChangeRequest.DoesNotExist:
                return {"success": False, "message": "درخواست مورد نظر یافت نشد."}
        else:  # 'C'
            if id == -1:
                record_instance = m.ChangeType.objects.create()
                id = record_instance.id
            else:
                try:
                    record_instance = m.ChangeType.objects.get(id=id)
                except m.ChangeType.DoesNotExist:
                    return {"success": False, "message": "نوع تغییر مورد نظر یافت نشد."}

        # 3- مقدار فعلی داده ها باید در یک متغییر به نام old_data ذخیره شود
        # باید داده های رکورد اصلی به صورت json تبدیل شود
        #  سایر جداول وابسته مثل شرکت های مرتبط و ... هم باید به صورت جیسون به داده های قبلی اضافه شود
        result = self.get_record_json(request_changetype=request_changetype, id=id)
        
        if not result.get('success', False):
            return result
        
        if 'record_data' not in result:
            return {'success':False, 'message': 'امکان واکشی اطلاعات قبلی رکورد وجود ندارد'}

        old_data = result['record_data']


        # 4- بررسی می کنیم که current_user_national_code مقدار معتبر داشته باشد
        try:
            user_instance = m.User.objects.get(national_code=current_user_nationalcode)
        except m.User.DoesNotExist:
            return {"success": False, "message": "کد ملی کاربر جاری نامعتبر است."}

        
        # 5- حالا به ازای هر فیلد باید بررسی کنیم که اگر اطلاعات آن در داده های ورودی وجود دارد، رکورد مورد نظر را به روز کنیم
        error_message = []
        try:

            # اطلاعات درخواست را از داده های فرم استخراج می کنیم
            # result = self.get_record_data(form_data)
            # if not result.get('success', True):
            #     return {"success": False, "message": "امکان فراخوانی اطلاعات تکمیلی درخواست وجود ندارد\n" + result['message']}
            

            
            #  برخی از اطلاعات باید با توجه به نوع تغییر تکمیل شوند
            # چیزهایی که ممکن است عوض شده باشند، کمیته و مدیر مربوطه است
            # result = self.get_change_type_data(form_data)
            # if not result.get('success', True):
            #     return {"success": False, "message": "امکان فراخوانی اطلاعات بر اساس نوع درخواست وجود ندارد\n" + result['message']}
            # form_data.update(result)                        
            
            # حالا بر اساس داده های ورودی، مقادیر را به روزرسانی می کنیم
            # کد وضعیت
            if 'status_code' in form_data:
                record_instance.status_code = form_data['status_code']
                # همگام‌سازی وضعیت و عنوان متناظر شی جاری
                self.status_code = record_instance.status_code
                self._sync_status_title()
            # عنوان تغییر
            if 'change_title' in form_data:
                record_instance.change_title = form_data['change_title']
            # توضیحات
            if 'change_description' in form_data:
                record_instance.change_description = form_data['change_description']

            # کد ملی مدیر مستقیم
            if 'direct_manager_nationalcode' in form_data:
                record_instance.direct_manager_nationalcode.national_code = form_data['direct_manager_nationalcode']
            
            # کد ملی مدیر مربوطه
            if 'related_manager_nationalcode' in form_data:
                record_instance.related_manager_nationalcode.national_code = form_data['related_manager_nationalcode']
                                
           
            # نیاز به کمیته
            if 'need_committee' in form_data:
                record_instance.need_committee = form_data['need_committee']

                # اگر نیاز به کمیته باشد، باید کمیته مربوطه و دبیر کمیته را به دست بیاوریم
                if record_instance.need_committee:
                    # کد ملی کاربر کمیته
                    if 'committee_user_nationalcode' in form_data:
                        record_instance.committee_user_nationalcode_id = form_data['committee_user_nationalcode']
                
                    # کمیته
                    if 'committee' in form_data:
                        record_instance.committee_id = form_data['committee']
                # در صورتی که نیاز به کمیته نباشد، فیلدهای مربوطه باید نال شوند
                else:
                    record_instance.committee_user_nationalcode = None
                    record_instance.committee = None

            # در صورتی که نیاز به کمیته نباشد، فیلدهای مربوطه باید نال شوند
            else:
                record_instance.committee_user_nationalcode = None
                record_instance.committee = None

                
            # --------------------------ویژگی های تغییر------------------------
            # گستردگی تغییرات
            if 'change_level' in form_data:
                record_instance.change_level_id = form_data['change_level']
            # طبقه‌بندی
            if 'classification' in form_data:
                record_instance.classification_id= form_data['classification']
            # اولویت
            if 'priority' in form_data:
                record_instance.priority_id = form_data['priority']
            # سطح ریسک
            if 'risk_level' in form_data:
                record_instance.risk_level_id = form_data['risk_level']
            
            # --------------------------محل تغییر------------------------
            # محل تغییرات دیتاسنترها باشد
            if 'change_location_DataCenter' in form_data:
                record_instance.change_location_data_center = form_data['change_location_DataCenter']
                self.update_extra_information (form_data=form_data, code='DataCenter', field_value=record_instance.change_location_data_center,request_changetype=request_changetype, id=id)
            else:
                self.update_extra_information (form_data=form_data, code='DataCenter', field_value=False,request_changetype=request_changetype, id=id)
                
            # محل تغییرات دیتابیس ها باشد
            if 'change_location_Database' in form_data:
                record_instance.change_location_database = form_data['change_location_Database']
                self.update_extra_information (form_data=form_data, code='Database', field_value=record_instance.change_location_database,request_changetype=request_changetype, id=id)
            else:
                self.update_extra_information (form_data=form_data, code='Database', field_value=False,request_changetype=request_changetype, id=id)
            
            # محل تغییرات سیستم ها و سرویس ها باشد
            if 'change_location_SystemServices' in form_data:
                record_instance.change_location_system_services = form_data['change_location_SystemServices']
                self.update_extra_information (form_data=form_data, code='SystemServices', field_value=record_instance.change_location_system_services,request_changetype=request_changetype, id=id)

            else:
                self.update_extra_information (form_data=form_data, code='SystemServices', field_value=False,request_changetype=request_changetype, id=id)


            # محل تغییرات سایر محل ها باشد
            if 'change_location_other' in form_data:
                record_instance.change_location_other = form_data['change_location_other']
                # اگر این گزینه انتخاب شده باشد، باید مقدار متناظر را به روز کنیم
                if record_instance.change_location_other:
                    record_instance.change_location_other_description = form_data.get('change_location_other_description','')
                # در صورتی که این گزینه انتخاب نشده باشد باید توضیحات پاک شوند
                else:
                    record_instance.change_location_other_description = ''
            # در صورتی که این گزینه وجود نداشته باشد باید توضیحات پاک شوند
            else:
                record_instance.change_location_other_description = ''
            

            # --------------------------دامنه تغییرات------------------------
            # دامنه تغییر
            if 'domain' in form_data:
                domain_code = form_data.get('domain')
                domain_obj = m.ConstValue.objects.filter(Code=domain_code).first()
                if not domain_obj:
                    return {"success": False, "message": "شناسه دامنه تغییرات نادرست است."}
                domain_id = domain_obj.id

                record_instance.change_domain_id = domain_id
                
                # اگر درون سازمانی باشد، باید اطلاعات شرکت ها حذف شوند
                if domain_code == 'Domain_Inside':
                    if request_changetype =='R':
                        m.RequestCorp.objects.filter(request=record_instance).delete()
                    else:
                        m.RequestCorp_ChangeType.objects.filter(changetype=record_instance).delete()
                
                # اگر برون سازمانی باشد، باید اطلاعات تیم ها حذف شود
                elif domain_code == 'Domain_Outside':
                    if request_changetype =='R':
                        m.RequestTeam.objects.filter(request=record_instance).delete()
                    else:
                        m.RequestTeam_ChangeType.objects.filter(changetype=record_instance).delete()
                    
                # در صورتی که تغییرات برون سازمانی یا بین سازمانی باشد، اطلاعات شرکت ها را به روز می کنیم
                if domain_code in ['Domain_Between','Domain_Outside']:
                    # به‌روزرسانی و درج رکوردهای جداول وابسته مانند RequestCorp
                    error_message = []
                    try:
                        request_corp_data = form_data.get('corps', [])
                        # دریافت همه شرکت‌های مرتبط فعلی با این درخواست
                        existing_corp_qs = None
                        if request_changetype =='R':
                            existing_corp_qs = m.RequestCorp.objects.filter(request=record_instance)
                        else:
                            existing_corp_qs = m.RequestCorp_ChangeType.objects.filter(changetype=record_instance)

                        existing_corp_codes = set(existing_corp_qs.values_list('corp_code', flat=True))
                        # استخراج corp_code های جدید از داده‌های فرم
                        new_corp_codes = set(request_corp_data)
                        # حذف شرکت‌هایی که دیگر در فرم نیستند
                        to_delete_codes = existing_corp_codes - new_corp_codes
                        if to_delete_codes:
                            if request_changetype =='R':
                                m.RequestCorp.objects.filter(request=record_instance, corp_code__in=to_delete_codes).delete()
                            else:
                                m.RequestCorp_ChangeType.objects.filter(changetype=record_instance, corp_code__in=to_delete_codes).delete()
                            
                        # اضافه کردن شرکت‌های جدیدی که قبلاً وجود نداشتند
                        to_add_codes = new_corp_codes - existing_corp_codes
                        for corp_code in to_add_codes:
                            if request_changetype =='R':
                                m.RequestCorp.objects.create(request=record_instance, corp_code_id=corp_code)
                            else:
                                m.RequestCorp_ChangeType.objects.create(changetype=record_instance, corp_code_id=corp_code)


                    except Exception as e:
                        error_message.append(f'خطا در پردازش شرکت‌ها: {str(e)}')
                
                # در صورتی که تغییرات درون سازمانی یا بین سازمانی باشد، اطلاعات تیم ها را به روز می کنیم
                if domain_code in ['Domain_Between','Domain_Inside']:
                    # پردازش اطلاعات تیم ها
                    try:
                        request_team_data = form_data.get('teams', [])
                        # دریافت همه تیم‌های مرتبط فعلی با این درخواست
                        existing_team_qs = None
                        if request_changetype =='R':
                            existing_team_qs = m.RequestTeam.objects.filter(request=record_instance)
                        else:
                            existing_team_qs = m.RequestTeam_ChangeType.objects.filter(changetype=record_instance)
                    
                        existing_team_codes = set(existing_team_qs.values_list('team_code', flat=True))
                        # استخراج team_code های جدید از داده‌های فرم
                        new_team_codes = set(request_team_data)
                        # حذف تیم‌هایی که دیگر در فرم نیستند
                        to_delete_codes = existing_team_codes - new_team_codes
                        if to_delete_codes:
                            if request_changetype =='R':
                                m.RequestTeam.objects.filter(request=record_instance, team_code__in=to_delete_codes).delete()
                            else:
                                m.RequestTeam_ChangeType.objects.filter(changetype=record_instance, team_code__in=to_delete_codes).delete()

                        # اضافه کردن تیم‌های جدیدی که قبلاً وجود نداشتند
                        to_add_codes = new_team_codes - existing_team_codes
                        for team_code in to_add_codes:
                            if request_changetype =='R':
                                m.RequestTeam.objects.create(request=record_instance, team_code_id=team_code)
                            else:
                                m.RequestTeam_ChangeType.objects.create(changetype=record_instance, team_code_id=team_code)

                    except Exception as e:
                        error_message.append(f'خطا در پردازش تیم ها: {str(e)}')

                

            # --------------------------حوزه اثرگذاری------------------------
            # بدترین مدت زمان توقف
            if 'downtime_duration_worstcase' in form_data:
                record_instance.downtime_duration_worstcase = int(form_data['downtime_duration_worstcase']) if form_data['downtime_duration_worstcase'] else None
            # توقف خدمات بحرانی
            if 'stop_critical_service' in form_data:
                record_instance.stop_critical_service = form_data['stop_critical_service']
                # در صورتی که گزینه خدمات بحرانی انتخاب شده باشد و عنوان خدمات بحرانی ارسال شده باشد
                if 'critical_service_title' in form_data and record_instance.stop_critical_service:
                    record_instance.critical_service_title = form_data['critical_service_title']
                else:
                    record_instance.critical_service_title = ''
            else:
                record_instance.critical_service_title = ''
            # توقف خدمات حساس
            if 'stop_sensitive_service' in form_data:
                record_instance.stop_sensitive_service = form_data['stop_sensitive_service']
                # در صورتی که توقف خدمات حساس انتخاب شده باشد و عنوان خدمات حساس هم وجود داشته باشد
                if 'stop_service_title' in form_data and record_instance.stop_sensitive_service:
                    record_instance.stop_service_title = form_data['stop_service_title']
                else:
                    record_instance.stop_service_title = ''
            else:
                record_instance.stop_service_title = ''
                
            # عدم توقف هیچ خدماتی
            if 'not_stop_any_service' in form_data:
                record_instance.not_stop_any_service = form_data['not_stop_any_service']

            # --------------------------بازگشت تغییرات------------------------

            # برنامه بازگشت وجود دارد
            if 'has_role_back_plan' in form_data:
                record_instance.has_role_back_plan = form_data['has_role_back_plan']

                # توضیحات برنامه بازگشت
                if 'role_back_plan_description' in form_data and record_instance.has_role_back_plan:
                    record_instance.role_back_plan_description = form_data['role_back_plan_description']
                else:
                    record_instance.role_back_plan_description = ''
            else:
                record_instance.role_back_plan_description = ''

            # --------------------------الزام به تغییر------------------------

            # الزام قانونی
            if 'reason_regulatory' in form_data:
                record_instance.reason_regulatory = form_data['reason_regulatory']
            # الزام فنی
            if 'reason_technical' in form_data:
                record_instance.reason_technical = form_data['reason_technical']
            # الزام امنیتی
            if 'reason_security' in form_data:
                record_instance.reason_security = form_data['reason_security']
            # الزام کسب و کاری
            if 'reason_business' in form_data:
                record_instance.reason_business = form_data['reason_business']
            # سایر الزامات
            if 'reason_other' in form_data:
                record_instance.reason_other = form_data['reason_other']
                # توضیحات الزامات دیگر
                if 'reason_other_description' in form_data and  record_instance.reason_other:
                    record_instance.reason_other_description = form_data['reason_other_description']
                else: 
                    record_instance.reason_other_description = ''
            else: 
                record_instance.reason_other_description = ''

        except Exception as e:
            return {"success": False, "message": f"خطا در به‌روزرسانی درخواست: {str(e)}"}
        
        # 6- در صورتی که خطایی وجود نداشته باشد، رکورد را ذخیره می کنیم
        if error_message:
            return {'success':False, 'message':error_message}
            
        record_instance.last_modifier_user_id = current_user_nationalcode
        record_instance.save()

        # 7- اطلاعات جدید رکورد را به دست می آوریم
        result = self.get_record_json(request_changetype=request_changetype, id=id)
        
        if not result.get('success', False):
            return result
        
        if 'record_data' not in result:
            return {'success':False, 'message': 'امکان واکشی اطلاعات جدید رکورد وجود ندارد'}

        new_data = result['record_data']
        
        # # تبدیل به JSON با حفظ حروف فارسی
        # new_data = json.loads(json.dumps(new_data, ensure_ascii=False))
        # old_data = json.loads(json.dumps(old_data, ensure_ascii=False))
        # 8- حالا اطلاعات سوابق تغییرات را در جدول مربوطه درج می کنیم
        try:
            m.DataHistory.objects.create(
                record_type=request_changetype,
                old_data= old_data or {},
                new_data= new_data or {},
                record_id=id,
                creator_user_id=current_user_nationalcode,
                last_modifier_user_id=current_user_nationalcode
            )
        except Exception as e:
            return {"success": False, "message": f"خطا ثبت سوابق درخواست: {str(e)}"}

        return {"success": True, "message": "درخواست با موفقیت به‌روزرسانی شد"}        


class Task:
    task_id: int = -1
    task_title:str = ''
    task_instance: m.Task = None
    task_order:int = 0
    
    request_task_id: int = -1
    request_id:int = -1
    status_code: str = ''
    # ('DEFINE', 'تعریف'),
    # ('EXERED', 'آماده انتخاب مجری'),
    # ('EXESEL', 'مجری انتخاب شده'),
    # ('TESRED', 'آماده انتخاب تستر'),
    # ('TESSEL', 'تستر انتخاب شده'),
    # ('FINISH', 'انجام موفق'),
    # ('FAILED', 'انجام ناموفق'),    
    status_title:str = ''
    
    request_task_instance: m.RequestTask = None
    test_required: bool = False
    error_message:str = ''

    # اطلاعات افراد درگیر در تسک
    users: List[m.User] = []

    executors: List[m.User] = []
    executors_names: str = ''
    selected_executor: m.User = None
    executor_done_date:datetime = None
    executor_done_time:str= ''
    executor_report: str=''    
    
    testers: List[m.User] = []
    testers_names:str = ''
    selected_tester: m.User = None
    tester_done_date:datetime = None
    tester_done_time:str= ''
    tester_report: str=''    

    current_user_nationalcode:str = ''

    def __init__(self, request_task_id, current_user:str):
        try:
            # دریافت درخواست بر اساس request_id
            self.request_task_instance = m.RequestTask.objects.get(
                id=request_task_id
            )
            self.request_id = self.request_task_instance.request.id
            self.task_order = self.request_task_instance.order_number
            self.status_code = self.request_task_instance.status_code
            self._sync_status_title()
            self.task_instance = self.request_task_instance.task
            self.task_id = self.task_instance.id
            self.task_title = self.task_instance.title
            self.request_task_id = request_task_id
            self.test_required = self.task_instance.test_required
            self.current_user_nationalcode = current_user
            # مقداردهی لیست ها
            self.get_users_info()

        except m.RequestTask.DoesNotExist:
            self.error_messager = 'شناسه تسک درخواست نامعتبر است'

        except Exception as e:
            self.error_messager = f'در ایجاد نمونه تسک مربوط به درخواست خطایی رخ داد: <br/>{str(e)}'

    def _sync_status_title(self, status_code: str = None):
        code = status_code if status_code is not None else self.status_code
        try:
            self.status_title = dict(
                m.RequestTask.STATUS_CHOICES
            ).get(code, code)
        except Exception:
            self.status_title = code

    def get_users_info(self):
        task_id = self.task_id

        try:
            # دریافت همه کاربران فعال مرتبط با تسک (چه مجری و چه تستر)
            task_users_qs = m.RequestTaskUser.objects.filter(
                request_task__task_id=self.task_id, 
                request_task__request_id = self.request_id
            )

            self.users = [tu.user_nationalcode for tu in task_users_qs]

            # مجریان (کسانی که user_role_code = 'E' دارند)
            self.executors = [tu.user_nationalcode for tu in task_users_qs if tu.user_role_code == 'E']
            # تسترها (کسانی که user_role_code = 'T' دارند)
            self.testers = [tu.user_nationalcode for tu in task_users_qs if tu.user_role_code == 'T']

            # اسامی مجریان به صورت رشته جدا شده با کاما
            self.executors_names = '، '.join([user.fullname_gender for user in self.executors])
            # اسامی تسترها به صورت رشته جدا شده با کاما
            self.testers_names = '، '.join([user.fullname_gender for user in self.testers])

            # مقداردهی مجری منتخب (در صورت وجود)
            selected_executor_obj = m.RequestTaskUserSelected.objects.filter(
                request_task_user__request_task__task_id=self.task_id, 
                request_task_user__request_task__request_id = self.request_id, 
                request_task_user__user_role_code="E"
            ).order_by('id').last()
            
            if selected_executor_obj is not None:
                self.selected_executor = selected_executor_obj.request_task_user.user_nationalcode
                # حالا تاریخ و ساعت و گزارش مربوطه را هم در صورت وجود استخراج می کنیم.user_done_dat
                self.executor_done_date = selected_executor_obj.user_done_date
                self.executor_done_time = selected_executor_obj.user_done_time
                self.executor_report = selected_executor_obj.user_report_description

            # مقداردهی تستر منتخب (در صورت وجود)
            selected_tester_obj = m.RequestTaskUserSelected.objects.filter(
                request_task_user__request_task__task_id=self.task_id, 
                request_task_user__request_task__request_id = self.request_id, 
                request_task_user__user_role_code="T"
            ).order_by('id').last()
            
            if selected_tester_obj is not None:
                self.selected_tester = selected_tester_obj.request_task_user.user_nationalcode
                # حالا تاریخ و ساعت و گزارش مربوطه را هم در صورت وجود استخراج می کنیم
                self.tester_done_date = selected_tester_obj.user_done_date
                self.tester_done_time = selected_tester_obj.user_done_time
                self.tester_report = selected_tester_obj.user_report_description
                

        except m.RequestTaskUser.DoesNotExist:
            self.error_message = 'برای این تسک هیچ کاربری تعریف نشده است'

        except Exception as e:
            self.error_message = f'در واکشی اطلاعات افراد مرتبط با تسک مربوط به درخواست خطایی رخ داد: <br/>{str(e)}'
            


    def next_step(self, action_code: str) -> dict:
        """این تابع تسک را به مرحله بعدی می برد. انواع حالتهای ممکن شامل موارد زیر است:
        ('DEFINE', 'تعریف'): CON->EXERED, RET->FAILED, REJ->FAILED
        ('EXERED', 'آماده انتخاب مجری'): CON->EXESEL
        ('EXESEL', 'مجری انتخاب شده'): CON->(if test_required : TESRED else : FINISH), RET->EXERED, REJ->FAILED        ('EXEFIN', 'اجرای موفق'): CON->(if test_required : TESRED else : FINISH), RET->EXERED, REJ->FAILED
        ('TESRED', 'آماده انتخاب تستر'): CON->TESSEL
        ('TESSEL', 'تستر انتخاب شده'): CON->FINISH, RET->TESRED, REJ->EXESEL
        ('FINISH', 'انجام موفق'):
        ('FAILED', 'انجام ناموفق'):

        Args:
            action_code (str): یک کد سه حرفی است که نوع عملیات انتخاب شده توسط کاربر را مشخص می کند و یکی از مقادیر زیر است:
                CON: تایید
                RET: بازگشت
                REJ: رد
        Returns:
            dict: یک دیکشنری است که عضو اول موفقیت و یا عدم موفقیت و عضو دوم پیام مربوطه را شامل می شود
        """

        status_code = self.status_code
        new_status = None
        message = ''
        if action_code == "CON":
            if status_code == "DEFINE":
                new_status = "EXERED"
                message= f" تسک برای {self.executors_names} جهت انتخاب جهت اجرا ارسال گردید"
                
            elif status_code == "EXERED":
                new_status = "EXESEL"
                u = self.selected_executor.fullname_gender if self.selected_executor else '-'
                message = f'تسک {self.task_title} توسط {u} جهت اجرا انتخاب شد.<br/> وضعیت در انتظار تنظیم گزارش توسط ایشان می باشد'
            elif status_code == "EXESEL":
                message = f'اجرای تسک {self.task_title} با موفقیت خاتمه یافت '
                if self.test_required and self.testers:
                    new_status = "TESRED"
                    message = f' و تسک جهت تست برای {self.testers_names} ارسال شد. <br/> وضعیت در انتظار انتخاب این تسک توسط یکی از تسترها می باشد.'
                else:
                    new_status = "FINISH"                    
            elif status_code == "TESRED":
                new_status = "TESSEL"
                message = f'تسک {self.task_title} توسط {self.selected_tester.fullname_gender} جهت انجام تست انتخاب شد.<br/> وضعیت در انتظار تنظیم گزارش توسط ایشان می باشد'
            elif status_code == "TESSEL":
                new_status = "FINISH"
                message = f'تست تسک {self.task_title} با موفقیت خاتمه یافت '

        # اگر عملیات بازگشت مدرک باشد
        elif action_code == "RET":
            if status_code == "DEFINE":
                new_status = "FAILED"
                message = "انجام این تسک منتفی گردید"
            elif status_code == "EXESEL":
                new_status = "EXERED"
                message= f"کاربر جاری از انجام تسک منصرف شده و تسک برای {self.executors_names} جهت انتخاب برای اجرا ارسال گردید"
            elif status_code == "TESSEL":
                new_status = "TESRED"
                message= f"کاربر جاری از تست تسک منصرف شده و تسک برای {self.testers_names} جهت انتخاب برای تست ارسال گردید"
        elif action_code == "REJ":
            if status_code in ["DEFINE", "EXERED"]:
                new_status = "FAILED"
                message = "انجام این تسک منتفی گردید"
            elif status_code == "TESSEL":
                new_status = "EXESEL"
                message = f'با توجه به ناموفق آمیز بودن تست، تسک جهت اجرای مجدد به {self.executors_names} ارسال شد.'
        else:
            return {"success": False, "message": "نوع عملیات درخواستی معتبر نمی‌باشد"}




        if new_status:
            self.status_code = new_status
            # عنوان وضعیت تسک را به روز می کنیم
            self._sync_status_title()
            # وضعیت جدید را در شی مربوطه به روز می کنیم
            self.request_task_instance.status_code = new_status
            self.request_task_instance.save()
            
            # حالا باید کنترل کنیم که آیا این تسک آخرین تسک بوده است یا خیر؟
            # برای این کار ابتدا یک نمونه شی درخواست را ایجاد می کنیم
            if new_status in ('FINISH','FAILED'):
                request_obj:Request = Request(current_user_national_code=self.current_user_nationalcode,request_id=self.request_id)
                result = request_obj.next_task(self)
                if not result.get('success',True):
                    return result
                elif result.get('message','') != '':
                    message = result.get('message')
                    
                
            return {
                "success": True,
                "message":message,
            }
            
        else:
            return {
                "success": False,
                "message": "تغییر وضعیت برای حالت فعلی این تسک امکان‌پذیر نیست",
            }

    def exit_cartable(self, user_nationalcode: str):
        """
        خارج کردن تسک از کارتابل سایر کاربران به جز کاربر جاری
        """
        # یک نمونه از شی کارتابل را ایجاد می کنیم
        # از این شی برای خارج کردن سند از کارتابل سایر مجریان استفاده می شود
        obj_cartable = Cartable()
        # شناسه سند را از جدول درخواست به دست آورده و در شی کارتابل به روز می کنیم
        obj_cartable.doc_id = self.request_task_instance.request.doc_id
        # به ازای هر کاربر به جز کاربر جاری باید مدرک را از کارتابل آنها خارج کنیم
        for user in self.users:
            if user.national_code != user_nationalcode:
                result = obj_cartable.exit_from_cartable(national_code=user.national_code)
                if not result.get('success'):
                    return result

        return {'success':True}
    
    def select_task(self, user_nationalcode: str) -> dict:
        """
        در این تابع، تسک جاری توسط کاربر جاری (تستر یا مجری) انتخاب می شود
        """
        try:
            # بررسی می کنیم که آیا کاربر جاری مجری یا تستر تسک هست یا خیر
            request_task_user = m.RequestTaskUser.objects.filter(
                request_task=self.request_task_instance,
                user_nationalcode__national_code=user_nationalcode
            ).first()

            if not request_task_user:
                return {"success": False, "message": "شما مجری یا تستر این تسک نیستید"}


            # باید رکوردی در جدول کاربران انتخاب کننده تسک درج کنیم
            task_user_selected = m.RequestTaskUserSelected.objects.create(
                pickup_date = datetime.now(),
                request_task_user = request_task_user
            )


            # خارج کردن از کارتابل سایر کاربران
            result = self.exit_cartable( user_nationalcode)
            if not result.get('success'):
                return result

            # حالا به تسک را به مرحله بعدی می بریم
            result = self.next_step('CON')
            
            # اگر همه چیز اوکی باشد باید ذخیره کنیم
            if result.get('success'):
                task_user_selected.save()
                
            return result

        except Exception as e:
            return {"success": False, "message": f"خطا در انتخاب تسک: {str(e)}"}

    def start_task(self):
        """
        این تابع برای شروع تسک استفاده می شود
        تسک ابتدا به وضعیت انتخاب مجری منتقل می شود
        """
        # self.status_code = 'EXERED'
        # self.request_task_instance.status_code = 'EXERED'
        # self.request_task_instance.save()
        
        return self.next_step('CON')
        

    def finish_task(self, user_natioanl_code:str):
        """
        این تابع برای خاتمه دادن وضعیت یک تسک است
        پس از خاتمه یافتن تسک، باید کنترل شود که آیا تسک دیگری وجود دارد یا خیر
        در صورتی که تسک دیگری وجود ندارد، باید فرآیند خاتمه یابد و اطلاع رسانی انجام شود
        """
        request_obj:Request = Request(self.request_id, user_natioanl_code)
        # حالا باید تابع مربوطه را فراخوانی کنیم که بررسی کند آیا آخرین تسک بوده است یا خیر؟
        request_obj.next_task(self)

    def save_task_report(
        self, request_task_id: int, form_data: dict, user_nationalcode: str
    ) -> dict:
        """
        ذخیره گزارش تسک
        """
        try:
            # به‌روزرسانی اطلاعات تسک
            task_user = m.RequestTaskUserSelected.objects.filter(
                request_task_user__request_task_id=request_task_id, 
                request_task_user__user_nationalcode=user_nationalcode
            ).order_by('id').last()

            if task_user:
                task_user.user_report_result = (
                    form_data.get("operation_result") == "true"
                )

                now = datetime.now()
                task_user.user_report_date = now.date()
                task_user.user_report_time = now.time().strftime("%H:%M")
                task_user.user_report_description = form_data.get("operation_report")
                task_user.user_done_date = form_data.get("done_date")
                task_user.user_done_time = form_data.get("done_time")
                task_user.save()

                return {"success": True, "message": "گزارش تسک با موفقیت ذخیره شد"}
            else:
                return {"success": False, "message": "رکورد مربوطه یافت نشد"}
          
        except Exception as e:
            return {"success": False, "message": f"خطا در ذخیره گزارش تسک: {str(e)}"}

class ChangeType:
    change_type_id:int=-1
    change_type_instance:m.ChangeType=None
    error_message:str = ''
    objform_manager:FormManager = None
    current_user_natioal_code:str= ''
    
    def __init__(self,current_user_natioal_code:str, change_type_id=None):
        
        if change_type_id and change_type_id > 0:
            self.change_type_instance = m.ChangeType.objects.filter(id=change_type_id).first()
            if self.change_type_instance is None:
                self.error_message = 'شناسه نوع تغییر نامعتبر است'
            else:
                self.change_type_id = change_type_id
        self.objform_manager = FormManager(current_user_national_code=current_user_natioal_code, request_id=-1)
        self.current_user_natioal_code = current_user_natioal_code
    
    def validate(self):
        return {'success':True, 'message':''}
    
    
    def create_record(self):
        return {'success':True, 'message':''}


    def get_change_type_data(self):
        """
        این تابع تمامی داده های یک نوع درخواست را بازگشت می دهد
        از این داده ها برای بارگذاری فرم جهت انجام ویرایش استفاده می شود
        """
        data = {"success": True, "message": ""}

        try:
            if self.change_type_instance:
                # اطلاعات نوع درخواست
                data["request"] = self.change_type_instance

                # اضافه کردن اطلاعات نوع درخواست به data
                extra_info = m.RequestExtraInformation_ChangeType.objects.filter(
                    changetype_id=self.change_type_id
                )
                data["data_center_selected"] = list(
                    extra_info.filter(extra_info__Code__startswith='DataCenter_').values_list('extra_info__Code', flat=True)
                )
                data["database_selected"] = list(
                    extra_info.filter(extra_info__Code__startswith='Database_').values_list('extra_info__Code', flat=True)
                )
                data["system_services_selected"] = list(
                    extra_info.filter(extra_info__Code__startswith='SystemServices_').values_list('extra_info__Code', flat=True)
                )

                # اطلاعات تیم های مرتبط
                teams = m.RequestTeam_ChangeType.objects.filter(changetype_id=self.change_type_id).values_list('team_code__team_code',flat=True)
                data["request_teams"] = teams

                # اطلاعات شرکت های مرتبط
                corps = m.RequestCorp_ChangeType.objects.filter(changetype_id=self.change_type_id).values_list('corp_code__corp_code',flat=True)
                data["request_corps"] = corps

                # اطلاعات تسک ها
                tasks = m.RequestTask_ChangeType.objects.filter(changetype_id=self.change_type_id)
                data["request_tasks"] = tasks
                
            else:
                return {"success": False, "message": "نوع درخواست مورد نظر وجود ندارد"}

        except Exception as e:
            return {"success": False, "message": str(e)}

        return data

    
    def load_record_data(self):
        
        objform_manager = self.objform_manager if self.objform_manager else FormManager(current_user_national_code=self.current_user_natioal_code, request_id=-1)
        form_data = {"message": "", "success": True}

        # داده های مقادیر ثابت (مثل کومبوها و ...) را دریافت می کنیم
        result = objform_manager.get_form_data()
        # اگر به هر دلیل امکان بارگذاری اطلاعات فرم وجود نداشته باشد پیام خطا بازگشت داده می شود
        if not result.get("success", False):
            return result

        form_data.update(result)

        # اطلاعات کاربران را دریافت می کنیم
        # کاربر جاری
        result = objform_manager.get_user_info(self.current_user_natioal_code)
        if not result.get("success", False):
            return result
        form_data["current_user"] = result["user"]
        form_data["current_user_role"] = result["team_roles"]
        
        # لازم است اطلاعات مدیر مربوطه و دبیر کمیته (در صورت وجود) به دست بیاوریم
        if self.change_type_instance.related_manager:
            result = objform_manager.get_user_info(self.change_type_instance.related_manager.national_code)
            if not result.get("success", False):
                return result
            form_data["related_manager"] = result["user"]
            form_data["related_manager_role"] = result["team_roles"]
        
        if self.change_type_instance.committee:
            result = objform_manager.get_user_info(self.change_type_instance.committee.administrator_nationalcode.national_code)
            if not result.get("success", False):
                return result
            form_data["committee_user"] = result["user"]
            form_data["committee_user_role"] = result["team_roles"]


        # حالا اطلاعات جانبی (شرکت ها، تیم ها، تسک ها و ...) مربوطه به نوع درخواست را واکشی می کنیم
        result = self.get_change_type_data()
        if not result.get("success", False):
            return result
        form_data.update(result)        

        # سایر اطلاعات مربوط به فرم را دریافت می کنیم
        request_date = jdatetime.datetime.now().strftime("%Y/%m/%d")

        form_data.update(
            {
                "request_id": self.change_type_id,
                "request_date": request_date,
                "request":self.change_type_instance,
                "form_type":"change_type",
            }
        )

        return form_data
        
        
    def update_record_data(self):
        return {'success':True, 'message':''}
    
    
class Request:
    obj_form_manager: FormManager = None
    obj_cartable: Cartable = None

    current_user_national_code: str = ''
    error_message: str = ''

    request_id: int  = -1
    request_instance: m.ConfigurationChangeRequest = None
    change_type_instance: m.ChangeType = None
    status_code: str = ''
    # ('DRAFTD', 'پیش نویس'): CON->DIRMAN, RET->FAILED, REJ->FAILED
    # ('DIRMAN', 'اظهار نظر مدیر مستقیم'): CON->RELMAN, RET->DRAFTD, REJ->FAILED
    # ('RELMAN', 'اظهار نظر مدیر مربوطه'): CON->(if need_committee: COMITE else : DOTASK), RET->DIRMAN, REJ->FAILED
    # ('COMITE', 'اظهار نظر کمیته'): CON->DOTASK, RET->RELMAN, REJ->FAILED
    # ('DOTASK', 'انجام تسک ها'): CON->FINISH, REJ->FAILED
    # ('FINISH', 'خاتمه یافته'):
    # ('FAILED', 'خاتمه ناموفقیت آمیز'):

    
    status_title: str = ''
    need_committee: bool = False

    # اطلاعات افراد درگیر
    user_requestor: m.User = None
    user_requestor_team_code: m.Team = None
    user_requestor_role_id: m.Role = None
    user_direct_manager: m.User = None
    user_related_manager: m.User = None
    user_committee: m.User = None

    # اطلاعات تسک ها
    task_users: List[m.User] = []
    task_executors: List[m.User] = []
    task_selected_executors: List[m.User] = []
    task_testers: List[m.User] = []
    task_selected_testers: List[m.User] = []

    # اطلاعات تسک ها
    tasks: List[Task] = None
    current_task: Task = None
    has_any_task_left: bool = False

    def _sync_status_title(self, status_code: str = None):
        code = status_code if status_code is not None else self.status_code
        try:
            self.status_title = dict(
                m.ConfigurationChangeRequest.STATUS_CHOICES
            ).get(code, code)
        except Exception:
            self.status_title = code

    def __init__(self, current_user_national_code, request_id):
        # یک نمونه از شی FormManager را ایجاد می کنیم
        self.obj_form_manager = FormManager(current_user_national_code, request_id)
        self.obj_cartable = Cartable()

        self.error_message = None

        # مقداردهی لیست ها
        self.tasks = []
        self.task_users = []
        self.task_executors = []
        self.task_selected_executors = []
        self.task_testers = []
        self.task_selected_testers = []

        # پیوند دوطرفه بدون ایجاد وابستگی دوری
        self.obj_form_manager.request_obj = self
        self.obj_form_manager.request_id = request_id
        self.obj_form_manager.error_message = None

        # در صورتی که تازه قصد ایجاد درخواست را داشته باشیم
        if request_id == -1:
            self.request_id = -1
            self.request_instance = None
            self.change_type_instance = None
            self.status_code = None
            self.need_committee = None
            self.error_message = None
        else:
            # در صورتی که یک درخواست ایجاد شده را مدیریت می کنیم
            try:

                # دریافت درخواست بر اساس request_id
                self.request_instance = m.ConfigurationChangeRequest.objects.get(
                    id=request_id
                )
                self.change_type_instance = self.request_instance.change_type
                self.request_id = request_id
                self.status_code = self.request_instance.status_code
                self.need_committee = self.request_instance.need_committee

                # مقداردهی عنوان وضعیت متناسب با کد وضعیت فعلی
                self._sync_status_title()

                # اطلاعات کاربران درگیر را به روزرسانی می کنیم

                # مشخصات کاربر درخواست دهنده
                self.user_requestor = self.request_instance.requestor_nationalcode
                self.user_requestor_role_id = self.request_instance.requestor_role_id
                self.user_requestor_team_code = (
                    self.request_instance.requestor_team_code
                )

                # اطلاعات سایر افراد درگیر
                self.user_direct_manager = (
                    self.request_instance.direct_manager_nationalcode
                )
                self.user_related_manager = (
                    self.request_instance.related_manager_nationalcode
                )

                # در شرایطی ممکن است کاربر کمیته تغییر کرده باشد، بایستی اطلاعات کاربر جدید کمیته را به روز کنیم
                if self.need_committee:
                    committee: m.Committee
                    committee = (
                        self.request_instance.committee
                    )  # فرض بر این است که فیلد committee یک شیء است
                    if committee and committee.is_active:
                        self.request_instance.committee_user_nationalcode = (
                            committee.administrator_nationalcode
                        )
                        self.request_instance.save()
                        self.user_committee = committee.administrator_nationalcode
                    else:
                        self.user_committee = None
                        # این تکه کد برای این است که اگر قبلا نیاز به کمیته داشته و الان حذف شده، کاربر مربوطه نیز حذف شود
                        # یا اینکه کمیته ای انتخاب شده بوده و الان غیرفعال شده که باید حذف شود
                        self.request_instance.committee = None
                        self.request_instance.committee_user_nationalcode = None
                        self.request_instance.save()

                # لیست تسک ها را به دست می آوریم
                # دریافت لیست تسک‌های مربوط به این درخواست
                tasks = list(
                    m.RequestTask.objects.filter(request=self.request_instance)
                )
                # به ازای هر یک از این تسک ها یک نمونه از شی 
                # Task
                # ایجاد می کنیم و در آرایه 
                # self.tasks
                # میریزیم
                for t in tasks:
                    new_task = Task(request_task_id=t.id,current_user=self.current_user_national_code)
                    # اگر در ایجاد تسک به مشکل برخورده باشیم، خطا را باید به درخواست منتقل کنیم
                    # تا در فراخوانی کننده نمایش داده شود
                    if new_task.error_message != '':
                        self.error_message += '<br/>' + new_task.error_message
                    self.tasks.append(new_task)
                    

                # تسک جاری را برابر با نخستین تسکی قرار بده که وضعیت آن FINISH یا FAILED نباشد
                self.current_task = next((t for t in self.tasks if t.status_code not in ("FINISH", "FAILED")), None)

                # آیا هیچ تسکی باقی مانده است؟
                self.has_any_task_left = any(
                    t.status_code != "FINISH" for t in self.tasks
                )
                
            except m.ConfigurationChangeRequest.DoesNotExist as e:
                self.request_instance = None
                self.request_id = None
                self.status_code = None
                self.need_committee = None
                self.error_type = "NotFound"
                self.error_message = "درخواست مورد نظر یافت نشد."
            except Exception as e:
                self.request_instance = None
                self.status_code = None
                self.need_committee = None
                self.error_type = "UnknownError"
                self.error_message = f"خطای غیرمنتظره: {str(e)}"


    def load_record_data(self, user_nationalcode: str):
        form_data = {"message": "", "success": True}

        # یک نمونه از شی مدیریت فرم را ایجاد می کنیم
        obj_form_manager = self.obj_form_manager if self.obj_form_manager else FormManager(self.current_user_national_code, -1)
        # مشخص می کنیم که وضعیت فعلی فرم چیست؟
        form_status = obj_form_manager.check_form_status(
            user_nationalcode=user_nationalcode,
            request_id=self.request_id)
        form_data["mode"] = form_status["mode"]
        form_data["form"] = form_status["form"]

        # اگر کاربر مربوطه مجاز به مشاهده اطلاعات نباشد
        if form_status["mode"] == "INVALID":
            form_data["message"] = "شما مجاز به مشاهده این فرم نیستید"
            return form_data

        # اگر در حالت به روزرسانی و یا مشاهده باشیم باید اطلاعات درخواست را دریافت کنیم
        if form_status["mode"] in ["READONLY", "UPDATE"]:

            # اگر شناسه درخواست معتبر باشد، اطلاعات شناسه درخواست هم ارسال می شود
            result = self.get_request_data()

            # اگر به هر دلیل امکان بارگذاری اطلاعات درخواست وجود نداشته باشد پیام خطا بازگشت داده می شود
            if not result.get("success", False):
                return result

            form_data.update(result)


        # داده های مقادیر ثابت (مثل کومبوها و ...) را دریافت می کنیم
        result = obj_form_manager.get_form_data()
        # اگر به هر دلیل امکان بارگذاری اطلاعات فرم وجود نداشته باشد پیام خطا بازگشت داده می شود
        if not result.get("success", False):
            return result

        form_data.update(result)


        # اطلاعات کاربران را دریافت می کنیم
        result = obj_form_manager.get_all_user_data()
        # اگر به هر دلیل امکان بارگذاری اطلاعات افراد وجود نداشته باشد پیام خطا بازگشت داده می شود
        if not result.get("success", False):
            return result

        form_data.update(result)

        # سایر اطلاعات مربوط به فرم را دریافت می کنیم
        request_date = request_date = jdatetime.datetime.now().strftime("%Y/%m/%d")

        form_data.update(
            {
                "request_number": self.request_id,
                "request_date": request_date,
            }
        )

        return form_data


    def get_record_data(self, form_data:json):
        """
        در این تابع اطلاعات تکمیلی رکورد درخواست برای عملیات درج و یا به روزرسانی آورده می شود
        این اطلاعات شامل برخی موارد مانند مدیر درخواست دهنده و یا موارد دیگری که بر اساس نوع تغییر
        باید مقدار بگیرند (مانند اطلاعات تسک ها) می شود
        البته مهم است که در چه مرحله ای هستیم، مثلا اگر مرحله مدیر به بعد هستیم
        اطلاعات مدیر درخواست دهنده (هر چند در واقعیت عوض شده باشد) نباید تغییر کند
        """
        form_data['success'] = True
        # اگر شناسه درخواست معتبر نباشد یعنی در حالت درج هستیم
        if not self.request_id or self.request_id <= 0:
            # اطلاعات را از ورودی دریافت می کنیم
            user_requestor =  form_data.get('requestor_user_nationalcode')
            team_code = form_data.get('requestor_team_code')
            role_id = form_data.get('requestor_role_id')
            
            # اگر تیم و سمت درخواست دهنده قبلا استخراج نشده باشند
            if (team_code == '' or team_code == None or role_id == None or role_id <= 0):
                # استخراج تیم و سمت کاربر
                result = self.obj_form_manager.get_user_team_role(form_data.get('user_team_role'))
                if not result.get('success'):
                    return result
                
                form_data['requestor_team_code'] = result['team_code']
                form_data['requestor_role_id'] = int(result['role_id'])
            
                team_code = result['team_code']
                role_id =  int(result['role_id'])

            # پیدا کردن مدیر مستقیم
            manager_obj = None
            user_team_role_obj: m.UserTeamRole = m.UserTeamRole.objects.filter(
                national_code=user_requestor,
                team_code=team_code,
                role_id=role_id,
            ).first()
            if user_team_role_obj:
                manager_obj = user_team_role_obj.manager_national_code
            else:
                return {'success':False, 'message':'امکان پیدا کردن مدیر مستقیم کاربر وجود ندارد'}
            
            # مقداردهی متغییرهای مربوطه
            self.user_direct_manager = manager_obj.national_code
            # پیدا کردن شی درخواست دهنده
            self.user_requestor:m.User = m.User.objects.filter(
                national_code = form_data.get('requestor_user_nationalcode')
            ).first()
            self.user_requestor_role_id = role_id
            self.user_requestor_team_code = team_code
        # در صورتی که در حالت درج نباشیم، اطلاعات تیم درخواست کننده و مدیر مستقیم را از رکورد درخواست استخراج می کنیم
        else:
            team_code = self.request_instance.requestor_team_code.team_code
            role_id = self.request_instance.requestor_role_id.role_id
            manager_obj = self.request_instance.direct_manager_nationalcode
            user_requestor = self.request_instance.requestor_nationalcode.national_code
        
        # در صورتی که کاربر جاری درخواست دهنده نباشد، از کاربر جاری استفاده می کنیم
        # این اتفاق زمانی رخ می دهد که کاربر جاری مدیر مستقیم، مدیر مربوطه یا کاربر کمیته و ... باشد
        user_requestor = self.user_requestor.national_code if self.user_requestor else form_data.get("user_nationalcode", "")
        
        # اگر نتوانسته باشیم مدیر مستقیم را پیدا کنیم.
        if not manager_obj or not manager_obj.national_code:
            return {"success": False, "message": "مدیر مستقیم کاربر پیدا نشد"}
        form_data['direct_manager_nationalcode'] = manager_obj.national_code
        
        # پیدا کردن نوع تغییر
        change_type_id = int(form_data.get("change_type", -1))
        change_type_obj: m.ChangeType
        change_type_obj = m.ChangeType.objects.filter(
            id=change_type_id
        ).first()

        # اگر نوع تغییر معتبر نباشد
        if not change_type_obj:
            return {"success": False, "message": "نوع درخواست معتبر نیست"}

        form_data['change_type'] = change_type_obj
        form_data['change_type_id'] = change_type_id
        # داده ها را بازگشت می دهیم
        return form_data


    def get_change_type_data(self, form_data):
        """
        این تابع اطلاعات مربوط به نوع تغییر را دریافت کرده بازگشت می دهد
        این اطلاعات تقریبا شامل تمامی اقلام اطلاعاتی فرم می شود
        
        Args:
            form_data (dict): اطلاعات مربوط به درخواست
        """
        change_type_id = form_data.get('change_type_id')
        
        # اگر نوع تغییر مقدار نداشته باشد
        if not self.change_type_instance:
            #  بررسی می کنیم که آیا چنین رکوردی در جدول نوع تغییرات وجود دارد یا خیر
            change_type_obj = m.ChangeType.objects.filter(id=change_type_id).first() 
            self.change_type_instance = change_type_obj
        else:
            change_type_obj = self.change_type_instance
            
        # اگر نوع تغییر معتبر نباشد
        if not change_type_obj:
            return {"success": False, "message": "نوع درخواست معتبر نیست"}
        
        form_data['related_manager_nationalcode'] = (  # کد ملی مدیر مربوطه
            change_type_obj.related_manager.national_code
            if change_type_obj.related_manager is not None
            else m.ConfigurationChangeRequest._meta.get_field(
                "related_manager_nationalcode"
            ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
        )
                
        # این فیلدها بر اساس نوع تغییر تکمیل می شوند
        # در تمامی موارد اگر مقدار در نوع تغییر مشخص نشده باشد، مقدار پیش فرض جدول در نظر گرفته می شود
        try:
            if ('change_location_data_center' not in form_data and
                # تغییر اطلاعات مدیر مربوطه تنها در صورتی قابل انجام است که در مراحل اولیه باشیم
                (self.status_code in ('DIRMAN','DRAFTD'))):
                form_data['related_manager_nationalcode'] = (  # کد ملی مدیر مربوطه
                    change_type_obj.related_manager.national_code
                    if change_type_obj.related_manager is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "related_manager_nationalcode"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            
            # برای تمامی اقلام اطلاعاتی، اگر اطلاعات مذکور در داده های ورودی وجود نداشته باشد
            # با توجه به نوع تغییر آنها را از دیتابیس می خوانیم
            if 'change_location_data_center' not in form_data:
                form_data['change_location_data_center'] = (  # محل تغییر: دیتاسنتر
                    change_type_obj.change_location_data_center
                    if change_type_obj.change_location_data_center is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "change_location_data_center"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'change_location_database' not in form_data:
                form_data['change_location_database'] = (  # محل تغییر: پایگاه داده
                    change_type_obj.change_location_database
                    if change_type_obj.change_location_database is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "change_location_database"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'change_location_system_services' not in form_data:
                form_data['change_location_system_services'] = (  # محل تغییر: سامانه‌ها
                    change_type_obj.change_location_system_services
                    if change_type_obj.change_location_system_services is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "change_location_system_services"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'change_location_other' not in form_data:
                form_data['change_location_other'] = (  # محل تغییر: سایر
                    change_type_obj.change_location_other
                    if change_type_obj.change_location_other is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "change_location_other"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'change_location_other_description' not in form_data:
                form_data['change_location_other_description'] = (  # توضیحات محل تغییر: سایر
                    change_type_obj.change_location_other_description
                    if change_type_obj.change_location_other_description is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "change_location_other_description"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'need_committee' not in form_data:
                form_data['need_committee'] = (  # نیاز به کمیته
                    change_type_obj.need_committee
                    if change_type_obj.need_committee is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "need_committee"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'committee' not in form_data:
                form_data['committee'] = (  # کمیته
                    change_type_obj.committee
                    if change_type_obj.committee is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "committee"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'committee_user_nationalcode' not in form_data:
                form_data['committee_user_nationalcode'] = (  # کد ملی کاربر کمیته
                    change_type_obj.committee.administrator_nationalcode
                    if change_type_obj.committee is not None
                    else None
                )
            if 'change_level' not in form_data:
                form_data['change_level'] = (  # سطح تغییر
                    change_type_obj.change_level
                    if change_type_obj.change_level is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "change_level"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'classification' not in form_data:
                form_data['classification'] = (  # طبقه‌بندی
                    change_type_obj.classification
                    if change_type_obj.classification is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "classification"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'priority' not in form_data:
                form_data['priority'] = (  # اولویت
                    change_type_obj.priority
                    if change_type_obj.priority is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "priority"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'risk_level' not in form_data:
                form_data['risk_level'] = (  # سطح ریسک
                    change_type_obj.risk_level
                    if change_type_obj.risk_level is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "risk_level"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'change_domain' not in form_data:
                form_data['change_domain'] = (  # حوزه تغییر
                    change_type_obj.change_domain
                    if change_type_obj.change_domain is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "change_domain"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'stop_critical_service' not in form_data:
                form_data['stop_critical_service'] = (  # توقف خدمات بحرانی
                    change_type_obj.stop_critical_service
                    if change_type_obj.stop_critical_service is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "stop_critical_service"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'critical_service_title' not in form_data:
                form_data['critical_service_title'] = (  # عنوان خدمت بحرانی
                    change_type_obj.critical_service_title
                    if change_type_obj.critical_service_title is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "critical_service_title"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'stop_sensitive_service' not in form_data:
                form_data['stop_sensitive_service'] = (  # توقف خدمات حساس
                    change_type_obj.stop_sensitive_service
                    if change_type_obj.stop_sensitive_service is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "stop_sensitive_service"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'stop_service_title' not in form_data:
                form_data['stop_service_title'] = (  # عنوان خدمت حساس
                    change_type_obj.stop_service_title
                    if change_type_obj.stop_service_title is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "stop_service_title"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'not_stop_any_service' not in form_data:
                form_data['not_stop_any_service'] = (  # توقف هیچ خدمتی وجود ندارد
                    change_type_obj.not_stop_any_service
                    if change_type_obj.not_stop_any_service is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "not_stop_any_service"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'has_role_back_plan' not in form_data:
                form_data['has_role_back_plan'] = (  # وجود برنامه بازگشت
                    change_type_obj.has_role_back_plan
                    if change_type_obj.has_role_back_plan is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "has_role_back_plan"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'role_back_plan_description' not in form_data:
                form_data['role_back_plan_description'] = (  # توضیحات برنامه بازگشت
                    change_type_obj.role_back_plan_description
                    if change_type_obj.role_back_plan_description is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "role_back_plan_description"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'reason_regulatory' not in form_data:
                form_data['reason_regulatory'] = (  # دلیل: الزامات قانونی
                    change_type_obj.reason_regulatory
                    if change_type_obj.reason_regulatory is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "reason_regulatory"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'reason_technical' not in form_data:
                form_data['reason_technical'] = (  # دلیل: الزامات فنی
                    change_type_obj.reason_technical
                    if change_type_obj.reason_technical is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "reason_technical"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'reason_security' not in form_data:
                form_data['reason_security'] = (  # دلیل: الزامات امنیتی
                    change_type_obj.reason_security
                    if change_type_obj.reason_security is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "reason_security"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'reason_business' not in form_data:
                form_data['reason_business'] = (  # دلیل: الزامات کسب‌وکار
                    change_type_obj.reason_business
                    if change_type_obj.reason_business is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "reason_business"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'reason_other' not in form_data:
                form_data['reason_other'] = (  # دلیل: سایر
                    change_type_obj.reason_other
                    if change_type_obj.reason_other is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "reason_other"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
            if 'reason_other_description' not in form_data:
                form_data['reason_other_description'] = (  # توضیحات دلیل: سایر
                    change_type_obj.reason_other_description
                    if change_type_obj.reason_other_description is not None
                    else m.ConfigurationChangeRequest._meta.get_field(
                        "reason_other_description"
                    ).get_default()#در صورتی که مقداری وجود نداشته باشد، مقدار پیش فرض تعریف شده در مدل را در نظر می گیریم
                )
        except Exception as e:
            return {"success": False, "message": f"خطا در دریافت اطلاعات نوع تغییر: {str(e)}"}

        return form_data

    def insert_change_type_records(self):
        """
        در این تابع برخی از اطلاعات اضافه مثل شرکت ها و تیم های مرتبط، تسک ها و ...
        که بر اساس نوع تغییر مشخص می شوند درج می شود
        """
        
        # ابتدا بررسی می کنیم که آیا چنین رکوردی در جدول نوع تغییرات وجود دارد یا خیر
        change_type_obj = self.change_type_instance
        # اگر نوع تغییر معتبر نباشد
        if not change_type_obj:
            return {"success": False, "message": "نوع درخواست معتبر نیست"}
                

        # حالا باید اطلاعات سایر جداول مرتبط را اضافه کنیم
        # ایجاد رکوردهای مرتبط بر اساس نوع تغییر
        try:
            # 1. RequestCorp_ChangeType -> RequestCorp
            request_corp_changetype_records: QuerySet[m.RequestCorp_ChangeType] = (
                m.RequestCorp_ChangeType.objects.filter(changetype=change_type_obj)
            )
            for record in request_corp_changetype_records:
                m.RequestCorp.objects.create(
                    request=self.request_instance, corp_code=record.corp_code
                )

            # 2. RequestTeam_ChangeType -> RequestTeam
            request_team_changetype_records: QuerySet[m.RequestTeam_ChangeType] = (
                m.RequestTeam_ChangeType.objects.filter(changetype=change_type_obj)
            )
            for record in request_team_changetype_records:
                m.RequestTeam.objects.create(
                    request=self.request_instance, team_code=record.team_code
                )

            # 3. RequestExtraInformation_ChangeType -> RequestExtraInformation
            request_extra_info_changetype_records: QuerySet[
                m.RequestExtraInformation_ChangeType
            ] = m.RequestExtraInformation_ChangeType.objects.filter(
                change_type=change_type_obj
            )
            for record in request_extra_info_changetype_records:
                m.RequestExtraInformation.objects.create(
                    request=self.request_instance, extra_info=record.extra_info
                )

            # 4. RequestTask_ChangeType -> RequestTask
            request_task_changetype_records: QuerySet[m.RequestTask_ChangeType] = (
                m.RequestTask_ChangeType.objects.filter(changetype=change_type_obj).order_by('order_number')
            )
            for record in request_task_changetype_records:
                # ابتدا رکورد RequestTask را ایجاد و نگهداری می‌کنیم
                request_task = m.RequestTask.objects.create(
                    request=self.request_instance,
                    task=record.task,
                    order_number=record.order_number,
                    status_code="DEFINE",  # وضعیت پیش‌فرض
                )
                # 5. TaskUser -> RequestTaskUser
                # برای هر کاربر مرتبط با این تسک، رکورد RequestTaskUser ایجاد کن
                task_user_records: QuerySet[m.TaskUser] = (
                    m.TaskUser.objects.filter(task=record.task, is_active=True)
                )
                for task_user in task_user_records:
                    m.RequestTaskUser.objects.create(
                        request_task=request_task,
                        user_nationalcode=task_user.user_nationalcode,
                        user_role_id=task_user.user_role_id,
                        user_team_code=task_user.user_team_code,
                        user_role_code=task_user.user_role_code,
                    )


            # 6. RequestNotifyGroup_ChangeType -> RequestNotifyGroup
            request_notify_group_changetype_records: QuerySet[
                m.RequestNotifyGroup_ChangeType
            ] = m.RequestNotifyGroup_ChangeType.objects.filter(
                changetype=change_type_obj
            )
            for record in request_notify_group_changetype_records:
                m.RequestNotifyGroup.objects.create(
                    request=self.request_instance,
                    notify_group=record.notify_group,
                    by_email=record.by_email,
                    by_sms=record.by_sms,
                )

        except Exception as e:
            # اگر خطایی در ایجاد رکوردهای مرتبط رخ داد، درخواست را حذف می‌کنیم
            self.request_instance.delete()
            return {
                "success": False,
                "message": f"خطا در ایجاد رکوردهای مرتبط: {str(e)}",
            }
        
        return {'success':True}
    

    def create_request(self, form_data: dict, user_nationalcode: str) -> dict:
        """
        این تابع برای ایجاد یک نسخه جدید از درخواست مورد استفاده قرار می گیرد

        Args:
            form_data (dict): این متغییر دربردارنده کلیه اطلاعات فرم در زمان ایجاد است
            user_nationalcode (str): کد ملی کاربر درخواست دهنده

        Returns:
            dict: نتیجه عملیات
        """
        try:
            # این تابع اطلاعات تکمیلی درخواست مانند مدیردرخواست دهنده و شی نوع درخواست را استخراج می کند
            result = self.get_record_data(form_data)
            if not result.get('success', True):
                return {"success": False, "message": "امکان فراخوانی اطلاعات تکمیلی درخواست وجود ندارد\n" + result['message']}
            
            form_data.update(result)
            
            # چون زمان تغییر است، برخی از اطلاعات باید با توجه به نوع تغییر تکمیل شوند
            result = self.get_change_type_data(form_data)
            if not result.get('success', True):
                return {"success": False, "message": "امکان فراخوانی اطلاعات بر اساس نوع درخواست وجود ندارد\n" + result['message']}
            
            form_data.update(result)        
            
            
            # یک سری اطلاعات بر اساس نوع تغییر تکمیل می شود
            # بخشی از این اطلاعات باید قبل از ذخیره رکورد درخواست ثبت شوند
            # این موارد شامل فیلدهای اجباری مانند مدیر مربوطه می شود.
            # برخی از موارد هم مانند تسک ها، باید بعد از درج رکورد مشخص شوند

            # ایجاد درخواست
            try:
                self.request_instance = m.ConfigurationChangeRequest.objects.create(
                    change_title=form_data.get("change_title"),
                    change_type=form_data.get("change_type"),
                    change_description=form_data.get("change_description"),
                    requestor_nationalcode_id=user_nationalcode,
                    requestor_team_code_id=form_data.get("requestor_team_code"),
                    requestor_role_id_id=form_data.get("requestor_role_id"), 
                    direct_manager_nationalcode_id=form_data.get("direct_manager_nationalcode"),
                    status_code="DRAFTD",
                    creator_user_id = user_nationalcode,
                    last_modifier_user_id = user_nationalcode,
                    # این فیلدها بر اساس نوع تغییر تکمیل می شوند
                    # در تمامی موارد اگر مقدار در نوع تغییر مشخص نشده باشد، مقدار پیش فرض جدول در نظر گرفته می شود
                    # کد ملی مدیر مربوطه
                    related_manager_nationalcode_id=form_data.get('related_manager_nationalcode'),
                    # محل تغییر: مرکز داده
                    change_location_data_center=form_data.get('change_location_data_center'),
                    # محل تغییر: پایگاه داده
                    change_location_database=form_data.get('change_location_database'),
                    # محل تغییر: سیستم‌ها
                    change_location_system_services=form_data.get('change_location_system_services'),
                    # محل تغییر: سایر
                    change_location_other=form_data.get('change_location_other'),
                    # توضیحات محل تغییر
                    change_location_other_description=form_data.get('change_location_other_description'),
                    # نیاز به کمیته
                    need_committee=form_data.get('need_committee'),
                    # کمیته
                    committee=form_data.get('committee'),
                    # کد ملی کاربر کمیته
                    committee_user_nationalcode=form_data.get('committee_user_nationalcode'),
                    # گستردگی تغییرات
                    change_level=form_data.get('change_level'),
                    # طبقه‌بندی
                    classification=form_data.get('classification'),
                    # اولویت
                    priority=form_data.get('priority'),
                    # سطح ریسک
                    risk_level=form_data.get('risk_level'),
                    # دامنه تغییر
                    change_domain=form_data.get('change_domain'),
                    # توقف خدمات بحرانی
                    stop_critical_service=form_data.get('stop_critical_service'),
                    # عنوان خدمات بحرانی
                    critical_service_title=form_data.get('critical_service_title'),
                    # توقف خدمات حساس
                    stop_sensitive_service=form_data.get('stop_sensitive_service'),
                    # عنوان خدمات حساس
                    stop_service_title=form_data.get('stop_service_title'),
                    # عدم توقف هیچ خدمتی
                    not_stop_any_service=form_data.get('not_stop_any_service'),
                    # وجود برنامه بازگشت
                    has_role_back_plan=form_data.get('has_role_back_plan'),
                    # توضیحات برنامه بازگشت
                    role_back_plan_description=form_data.get('role_back_plan_description'),
                    # الزامات قانونی
                    reason_regulatory=form_data.get('reason_regulatory'),
                    # الزامات فنی
                    reason_technical=form_data.get('reason_technical'),
                    # الزامات امنیتی
                    reason_security=form_data.get('reason_security'),
                    # الزامات کسب‌وکار
                    reason_business=form_data.get('reason_business'),
                    # سایر الزامات
                    reason_other=form_data.get('reason_other'),
                    # توضیحات سایر الزامات
                    reason_other_description=form_data.get('reason_other_description'),
                )
            except Exception as e:
                return {
                    "success": False,
                    "message": f"خطا در ایجاد درخواست: {str(e)}",
                }


            # شناسه درخواست را مقداردهی می کنیم
            self.request_id = self.request_instance.id
            self.change_type_instance = self.request_instance.change_type
            
            # سایر رکوردهایی که مربوط به نوع تغییر هستند، مانند شرکتها، تیم ها، تسک ها و ... را درج می کنیم
            self.insert_change_type_records()
            
            # اطلاعات کاربران را مقداردهی می کنیم
            self.extract_request_users()

            # با استفاده از این تابع، عملیات رفتن به مرحله بعد و ارسال به کارتابل مدیر و اطلاع رسانی های لازم انجام می شود
            result = self.next_step(
                action_code="CON", user_nationalcode=user_nationalcode
            )

            if result["success"]:
                return {
                    "success": True,
                    "request_id": self.request_instance.id,
                    "mode":'READONLY',
                    "message": f"درخواست با موفقیت ایجاد و جهت بررسی برای {self.user_direct_manager.fullname_gender} ارسال شد",
                }
            else:
                # اگر next_step با خطا مواجه شد، درخواست را حذف می‌کنیم
                self.request_instance.delete()
                return result

        except Exception as e:
            # اگر درخواست ایجاد شده بود، آن را حذف می‌کنیم
            if hasattr(self, "request_instance") and self.request_instance:
                try:
                    self.request_instance.delete()
                except:
                    pass
            return {"success": False, "message": f"خطا در ایجاد درخواست: {str(e)}"}

    # def next_status(self):
    #     self.status_code

    def update_request(self, form_data: dict, current_user_nationalcode:str) -> dict:
        """
        به‌روزرسانی درخواست موجود
        """
        result = self.obj_form_manager.update_record(request_changetype='R', form_data=form_data, id=self.request_id, current_user_nationalcode=current_user_nationalcode)
        if not result.get('success',False):
            return result
        
        # باید نسخه جاری را با نسخه ذخیره شده عوض کنیم
        self.request_instance.refresh_from_db() 
        
        return {"success": True, "message": "اطلاعات با موفقیت به روزرسانی شد"}

    def send_cartable(self, from_user: str, to_user: str, doc_state: str):
        """
        ارسال به کارتابل کاربر
        """
        # این تابع dummy است
        # ابتدا کنترل می کنیم که آیا سند برای این درخواست ثبت شده است؟
        # اگر سند ثبت نشده باشد، باید ابتدا آن را ثبت کنیم
        if not self.obj_cartable.doc_id or self.obj_cartable.doc_id < 0:
            # رکورد متناظر درخواست را به دست می اوریم
            request_title = self.request_instance.change_title
            priority = (
                self.request_instance.priority
                if self.request_instance.priority
                else "NORMAL"
            )

            # حالا سند را ایجاد می کنیم
            self.obj_cartable.create_doc(
                request_title,
                self.request_id,
                self.user_requestor.national_code,
                priority,
            )

            # حالا شناسه سند را در رکورد متناظر درخواست به روزرسانی می کنیم
            self.request_instance.doc_id = self.obj_cartable.doc_id
            self.request_instance.save()

        # در صورتی که سند موجود باشد آن را ارسال می کنیم
        self.obj_cartable.send_cartable(
            receiver=to_user, sender=from_user, new_doc_state=doc_state
        )


    def extract_request_users(self):
        """
        این تابع اطلاعات افراد درگیر در درخواست شامل، درخواست دهنده، مدیر مستیم، مدیر مربوطه، کاربر کمیته
        """
        self.user_requestor = self.request_instance.requestor_nationalcode
        self.user_direct_manager = self.request_instance.direct_manager_nationalcode
        self.user_related_manager = self.request_instance.related_manager_nationalcode
        self.user_committee = self.request_instance.committee_user_nationalcode

    def extract_task_users(self):
        if not self.tasks:
            self.get_all_tasks()

        for t in self.tasks:
            t: Task
            t.get_users_info()
            self.task_users.extend(t.users)
            self.task_executors.extend(t.executors)
            if t.selected_executor:
                self.task_selected_executors.append(t.selected_executor)
            self.task_testers.extend(t.testers)
            if t.selected_tester:
                self.task_selected_testers.append(t.selected_tester)

    def get_all_users(self):
        self.extract_request_users()
        self.extract_task_users()

    def validate(self) -> dict:
        errors = []
        # کد ملی درخواست کننده
        if (
            self.user_requestor
            and not m.User.objects.filter(national_code=self.user_requestor).exists()
        ):
            errors.append("کد ملی درخواست کننده نامعتبر است.")


    def next_step(
        self, action_code: str, user_nationalcode: str, form_data: dict = None
    ) -> dict:
        """این تابع وضعیت درخواست را بر اساس نوع عملیات، به مرحله بعدی منتقل می کند. انواع وضعیت های ممکن در زیر آورده شده است:
        ('DRAFTD', 'پیش نویس'): CON->DIRMAN, RET->FAILED, REJ->FAILED
        ('DIRMAN', 'اظهار نظر مدیر مستقیم'): CON->RELMAN, RET->DRAFTD, REJ->FAILED
        ('RELMAN', 'اظهار نظر مدیر مربوطه'): CON->(if need_committee: COMITE else : DOTASK), RET->DIRMAN, REJ->FAILED
        ('COMITE', 'اظهار نظر کمیته'): CON->DOTASK, RET->RELMAN, REJ->FAILED
        ('DOTASK', 'انجام تسک ها'): CON->FINISH, REJ->FAILED
        ('FINISH', 'خاتمه یافته'):
        ('FAILED', 'خاتمه ناموفقیت آمیز'):

        Args:
            action_code (str): یک کد سه حرفی است که نوع عملیات انتخاب شده توسط کاربر را مشخص می کند و یکی از مقادیر زیر است:
                CON: تایید
                RET: بازگشت
                REJ: رد
            user_nationalcode (str): کد ملی کاربر جاری
            form_data (dict): داده‌های فرم (اختیاری)

        Returns:
            dict: یک دیکشنری است که عضو اول موفقیت و یا عدم موفقیت و عضو دوم پیام مربوطه را شامل می شود
        """
        try:
            current_status = self.request_instance.status_code
            new_status = None
            next_user = None
            message = ''
            if action_code == "CON":
                
                if current_status == "DRAFTD":
                    new_status = "DIRMAN"
                    next_user:m.User = (
                        self.request_instance.direct_manager_nationalcode
                    )
                    message = f'فرم با موفقیت برای {next_user.fullname_gender} جهت بررسی مدیر مستقیم ارسال شد'
                elif current_status == "DIRMAN":
                    new_status = "RELMAN"
                    next_user = (
                        self.request_instance.related_manager_nationalcode
                    )
                    message = f'فرم با موفقیت برای {next_user.fullname_gender} جهت بررسی مدیر مربوطه ارسال شد'

                elif current_status == "RELMAN":
                    if self.request_instance.need_committee:
                        new_status = "COMITE"
                        next_user = (
                            self.request_instance.committee_user_nationalcode
                        )
                        message = f'فرم با موفقیت برای {next_user.fullname_gender} جهت بررسی دبیر کمیته ارسال شد'

                    else:
                        new_status = "DOTASK"
                        # ارسال به کارتابل مجریان
                        result = self.do_task()
                        if not result.get('success',True):
                            return result                        
                        next_user = self.current_task.executors

                elif current_status == "COMITE":
                    new_status = "DOTASK"
                    # ارسال به کارتابل مجریان
                    result= self.do_task()
                    if not result.get('success',True):
                        return result
                    next_user = self.current_task.executors

                elif current_status == "DOTASK":
                    new_status = "FINISH"
                    message = 'فرآیند با موفقیت خاتمه یافت'
            elif action_code == "RET":
                if current_status == "DIRMAN":
                    new_status = "DRAFTD"
                    next_user = (
                        self.request_instance.requestor_nationalcode
                    )
                    message = f'فرم به {next_user.fullname_gender} جهت بررسی بازگشت داده شد'
                    
                elif current_status == "RELMAN":
                    new_status = "DIRMAN"
                    next_user = (
                        self.request_instance.direct_manager_nationalcode
                    )
                    message = f'فرم به {next_user.fullname_gender} جهت بررسی مدیر مستقیم بازگشت داده شد'
                elif current_status == "COMITE":
                    new_status = "RELMAN"
                    next_user = (
                        self.request_instance.related_manager_nationalcode
                    )
                    message = f'فرم به {next_user.fullname_gender} جهت بررسی مدیر مربوطه بازگشت داده شد'

            elif action_code == "REJ":
                if current_status in ["DRAFTD", "DIRMAN", "RELMAN", "COMITE", "DOTASK"]:
                    new_status = "FAILED"
                    message = 'این نسخه از فرآیند باطل گردید'
            else:
                return {"success": False, "message": "کد عملیات معتبر نمی‌باشد."}

            if new_status:
                # به‌روزرسانی وضعیت
                self.request_instance.status_code = new_status
                self.request_instance.save()

                self.status_code = new_status
                # عنوان وضعیت بر اساس STATUS_CHOICES مدل
                self._sync_status_title(new_status)

                # ارسال به کارتابل کاربر بعدی
                if next_user:
                    if isinstance(next_user, (list, tuple)):
                        for user in next_user:
                            self.send_cartable(
                                self.request_instance.id, user.national_code, self.status_title
                            )
                    else:
                        self.send_cartable(
                            self.request_instance.id, next_user.national_code, self.status_title
                        )

                # ذخیره اطلاعات اضافی
                if form_data:
                    self.save_step_data(
                        current_status, action_code, form_data, user_nationalcode
                    )

                return {
                    "success": True,
                    "message": message
                }
            else:
                return {
                    "success": False,
                    "message": "تغییر وضعیت برای حالت فعلی امکان‌پذیر نیست.",
                }

        except Exception as e:
            return {"success": False, "message": f"خطا در تغییر وضعیت: {str(e)}"}


    def do_task(self):
        """
        اجرای آخرین تسک فعال
        """
        try:
            # اگر تسک جاری نداریم نخستین تسک را انتخاب می کنیم
            if not self.current_task:
                self.current_task = self.tasks[0]
            
            # اگر وضعیت تسک تعریف باشد، باید آن را شروع کنیم
            if self.current_task.status_code == "DEFINE":
                result = self.current_task.start_task()
                return result
            
            # حالا تسک را به مرحله بعدی می بریم
            result = self.current_task.next_step('CON')
            return result

        except Exception as e:
            return {'success':False, 'message':f'امکان اجرای تسک مربوطه وجود ندارد{str(e)}'}

    def next_task(self, task_obj:Task):
        """
        این تابع پس از خاتمه یک تسک فراخوانی می شود
        و به سراغ تسک بعدی می رود
        اگر این تسک آخرین تسک باشد، باید فرآیند درخواست خاتمه یابد
        """
        
        # حالا باید به سراغ تسک بعدی برویم
        # ابتدا شماره ترتیب تسک جاری را به دست می آوریم 
        order_number = task_obj.task_order 
        
        # حالا تسکی که شماره ترتیب بعدی را دارد پیدا می کنیم
        next_task = m.RequestTask.objects.filter(
            request=self.request_instance,
            order_number__gt=order_number
        ).order_by('order_number').first()
        
        # حالا بررسی می کنیم که آیا تسکی وجود دارد یا خیر
        if next_task is None:
            return self.finish_request(True)
        
        # حالا یک شی تسک می سازیم
        task_obj = Task(request_task_id=next_task.id, current_user=task_obj.current_user_nationalcode)
        if task_obj.error_message != '':
            return  {'success':False,'message':task_obj.error_message}
        
        result = task_obj.start_task()
        return result

    def finish_request(self, success_finish:bool=True):
        """
        این تابع درخواست را مختومه می کند
        کارهای زیر باید انجام شود:
        1- وضعیت رکورد درخواست خاتمه یافته شود
        2- در صورتی که تسک بازی وجود دارد باید خاتمه یابد
        3- درخواست از کارتابل همه خارج می شود
        4- به گروه های اطلاع رسانی، اطلاع رسانی انجام می شود

        Args:        
            finish_type:: bool
                True: خاتمه موفقیت آمیز
                False : خاتمه ناموفق
        """
        # وضعیت خاتمه موفقیت آمیز
        status_code = 'FINISH'
        
        # در صورتی که وضعیت خاتمه ناموفق باشد
        if not success_finish:
            status_code = 'FAILED'
        
        # 1- وضعیت رکورد درخواست را به روز می کنیم
        self.request_instance.status_code = status_code
        self.request_instance.save()
        
        # 2- بررسی می کنیم اگر تسک بازی وجود داشته باشد وضعیت آن را هم مختومه می کنیم
        # رکوردهایی که وضعیت آنها خاتمه نیست را پیدا می کنیم
        unfinished_tasks = m.RequestTask.objects.filter(
            request=self.request_instance
        ).exclude(status_code__in=('FINISH', 'FAILED'))
        for task in unfinished_tasks:
            task.status_code = status_code
            task.save()
            
        # 3- باید درخواست از کارتابل همه خارج شود
        self.obj_cartable.exit_from_all_cartables()
        
        # 4- اطلاع رسانی انجام شود
        self.notify(status_code=status_code)
        
    def notify(self, status_code):
        """
        این تابع به تمامی گروه های اطلاع رسانی، اطلاع رسانی را بر حسب کانال های تعیین شده انجام می دهد

        Args:
            status_code (: str): مشخص می کند که اطلاع رسانی در چه مرحله ای باید انجام شود
                # ('DRAFTD', 'پیش نویس'): Code : SLM.CCR.DRAFTD : اطلاع رسانی به درخواست کننده
                # ('DIRMAN', 'اظهار نظر مدیر مستقیم'): Code : SLM.CCR.DIRMAN : اطلاع رسانی به مدیر درخواست کننده
                # ('RELMAN', 'اظهار نظر مدیر مربوطه'): Code : SLM.CCR.RELMAN : اطلاع رسانی به مدیر مربوطه
                # ('COMITE', 'اظهار نظر کمیته'): Code : SLM.CCR.COMITE : اطلاع رسانی به دبیر کمیته
                # ('DOTASK', 'انجام تسک ها'): 
                    # ('EXERED', 'آماده انتخاب مجری'): Code: SLM.CCR.TASEXS : اطلاع رسانی به مجریان
                    # ('EXESEL', 'مجری انتخاب شده'): Code: SLM.CCR.TASEXR : اطلاع رسانی به مجری منتخب
                    # ('TESRED', 'آماده انتخاب تستر'): Code: SLM.CCR.TASTES : اطلاع رسانی به تسترها
                    # ('TESSEL', 'تستر انتخاب شده'): Code: SLM.CCR.TASTER : اطلاع رسانی به تستر منتخب
                    # ('FINISH', 'انجام موفق'): Code: SLM.CCR.TASFIN : اطلاع رسانی به مجری منتخب، مدیر مربوطه
                    # ('FAILED', 'انجام ناموفق'): Code: SLM.CCR.TASFAL :  اطلاع رسانی به مجری منتخب، مدیر مربوطه
                # ('FINISH', 'خاتمه یافته'): Code: SLM.CCR.FINISH : اطلاع رسانی به درخواست کننده، مدیر مستقیم، مدیر مربوطه، دبیرکمیته، گروه های اطلاع رسانی
                # ('FAILED', 'خاتمه ناموفقیت آمیز'): Code : SLM.CCR.FAILED : اطلاع رسانی به درخواست کننده، مدیر مستقیم، مدیر مربوطه، دبیرکمیته، گروه های اطلاع رسانی
                    """
        code = None
        users = []

        if status_code == 'DRAFTD':
            code = 'SLM.CCR.DRAFTD'
            users = [self.user_requestor]
        elif status_code == 'DIRMAN':
            code = 'SLM.CCR.DIRMAN'
            users = [self.user_direct_manager]
        elif status_code == 'RELMAN':
            code = 'SLM.CCR.RELMAN'
            users = [self.user_related_manager]
        elif status_code == 'COMITE':
            code = 'SLM.CCR.COMITE'
            users = [self.user_committee]
        # اگر در وضعیت انجام تسک باشد، اطلاع رسانی بر اساس وضعیت تسک جاری انجام می شود
        elif status_code == 'DOTASK':
            if status_code == 'EXERED':
                code = 'SLM.CCR.TASEXS'
                users = self.current_task.executors
            elif status_code == 'EXESEL':
                code = 'SLM.CCR.TASEXR'
                users = [self.current_task.selected_executor]
            elif status_code == 'TESRED':
                code = 'SLM.CCR.TASTES'
                users = self.current_task.testers
            elif status_code == 'TESSEL':
                code = 'SLM.CCR.TASTER'
                users = [self.current_task.selected_tester]
            elif status_code == 'FINISH':
                code = 'SLM.CCR.TASFIN'
                users = [self.user_related_manager, self.current_task.selected_executor]
            elif status_code == 'FINISH':
                code = 'SLM.CCR.TASFAL'
                users = [self.user_related_manager, self.current_task.selected_executor]
        elif status_code == 'FINISH':
            code = 'SLM.CCR.FINISH'
            users = []
            if self.user_requestor:
                users.append(self.user_requestor)
            if self.user_direct_manager:
                users.append(self.user_direct_manager)
            if self.user_related_manager:
                users.append(self.user_related_manager)
            if self.user_committee:
                users.append(self.user_committee)
            group_users = self.get_notification_group_user('email')
            if group_users.get('users'):
                users += group_users.get('users', [])
        elif status_code == 'FAILED':
            code = 'SLM.CCR.FAILED'
            users = []
            if self.user_requestor:
                users.append(self.user_requestor)
            if self.user_direct_manager:
                users.append(self.user_direct_manager)
            if self.user_related_manager:
                users.append(self.user_related_manager)
            if self.user_committee:
                users.append(self.user_committee)
            group_users = self.get_notification_group_user('email')
            if group_users.get('users'):
                users += group_users.get('users', [])
                
                
        if code and users:
            return self.send_email(template_code=code, users=users)
        
        return {'sucess':False, 'message':'امکان اطلاع رسانی وجود ندارد'}
    
    def get_notification_group_user(self, notify_type: str)->dict:
        """
        این تابع لیستی از کاربران را بر حسب اطلاع رسانی تعیین شده در انتهای فرآیند بازگشت می دهد
        
        پارامتر notify_type باید یکی از مقادیر 'email'، 'sms' یا 'phone' باشد.
        """
        if notify_type not in ('email', 'sms', 'phone'):
            return {"sucess":False,"message":"نوع اطلاع رسانی نامعتبر است"}
        
        # رکوردهای اطلاع رسانی مربوط به این درخواست را استخراج می کنیم
        notification_group = m.RequestNotifyGroup.objects.filter(request=self.request_instance)
        # در صورتی که نوع اطلاع رسانی با استفاده از ایمیل باشد
        if notify_type == 'email':
            notification_group = notification_group.filter(by_email=True)
        # در صورتی نوع اطلاع رسانی با استفاده از پیامک باشد
        if notify_type == 'sms':
            notification_group = notification_group.filter(by_sms=True)
        # در صورتی که نوع اطلاع رسانی با استفاده از تلفن گویا باشد
        if notify_type == 'phone':
            notification_group = notification_group.filter(by_phone=True)
        
        users:[m.User] = []
        # به ازای هر رکورد اطلاع رسانی باید کاربران مربوطه را استخراج کنیم و به لیست اضافه کنیم
        for ng in notification_group:
            # رکورد گروه اطلاع رسانی را به دست می آوریم
            notify_group = ng.notifygroup
            # مقدار فیلد سمت و تیم را به دست می آوریم
            role_id = notify_group.role_id
            team_code = notify_group.team_code 
            # اگر هم سمت و هم تیم مقدار داشته باشد، 
            # همه کاربرانی که آن سمت و تیم را دارند را استخراج می کنیم
            # مثلا برنامه نویسان تیم خودرو
            if role_id and team_code:
                u = m.UserTeamRole.objects.filter(role_id = role_id, team_code = team_code).values_list('national_code')
                if u:
                    # افراد استخراج شده را به لیست اضافه می کنیم
                    users += u
            # اگر فقط سمت مقدار داشته باشد
            # باید برای تمامی کاربرانی که این سمت را دارند ارسال شود
            # مثلا برای تمامی مدیران پروژه
            elif role_id:
                u = m.UserTeamRole.objects.filter(role_id = role_id).values_list('national_code')
                if u:
                    # افراد استخراج شده را به لیست اضافه می کنیم
                    users += u
            # اگر فقط تیم مقدار داشته باشد
            # باید برای تمامی کاربرانی که در آن تیم هستند ارسال شود
            # مثلا برای تمامی اعضای تیم ادمین
            elif team_code:
                u = m.UserTeamRole.objects.filter(team_code = team_code).values_list('national_code')
                if u:
                    # افراد استخراج شده را به لیست اضافه می کنیم
                    users += u
            # در غیر این صورت باید اطلاع رسانی برای افرادی که در این گروه تعریف شده اند انجام شود
            else:
                u = m.NotifyGroupUser.objects.filter(notification_group=notify_group).values_list('user_nationalcode')
                if u:
                    # افراد استخراج شده را به لیست اضافه می کنیم
                    users += u
        
        return {'success':True, 'users':users, 'message':''}
        
    
    def send_email(self, template_code:str, users:[m.User]):
        """
        این تابع به افرادی که در لیست هستند اطلاع رسانی از طریق ایمیل را انجام می دهد
        برای این کار آدرس ایمیل افراد را استخراج می کند
        داده های مربوط به درخواست را در متغییر مربوطه قرار می دهد
        سرویس ایمیل را صدا می زند

        Args:
            template_code (str): کد الگوی اطلاع رسانی. این کد در دیتابیس سیستم اطلاع رسانی تعریف شده است
            user (m.User]): آرایه ای از افرادی که باید اطلاع رسانی برای آنها انجام شود
        """
        variable_values = {}
        to_users_emails = [str]
        
        # آدرس ایمیل افراد را استخراج می کنیم 
        for user in users:
            # ادرس ایمیل را باید اصلاح کنیم
            email = user.usermame.split('@')[0] + '@iraneit.com'
            to_users_emails.append(email)
        
        # حالا متغییرها را به روز می کنیم
        # عنوان درخواست
        variable_values['title'] = self.request_instance.change_title
        # عنوان نوع درخواست
        variable_values['change_type'] = self.request_instance.change_type.change_type_title
        # وضعیت درخواست
        variable_values['request_status'] = self.status_title
        # اطلاعات درخواست دهنده
        variable_values['creator_fullname_gender'] = self.user_requestor.fullname_gender 
        variable_values['creator_fullname_title'] = self.user_requestor.fullname_title
        # اطلاعات مدیر مستقیم
        variable_values['direct_manager_gender'] = self.user_direct_manager.fullname_gender 
        variable_values['direct_manager_title'] = self.user_direct_manager.fullname_title
        # اطلاعات مدیر مربوطه
        variable_values['related_manager_gender'] = self.user_related_manager.fullname_gender 
        variable_values['related_manager_title'] = self.user_related_manager.fullname_title
        # اطلاعات دبیر کمیته
        variable_values['committe_user_gender'] = self.user_committee.fullname_gender
        variable_values['committe_user_title'] = self.user_committee.fullname_title
        # نام کمیته
        variable_values['committe'] = self.request_instance.committee
        # عنوان تسک
        variable_values['task_title'] = self.current_task.task_title
        # مجریان تسک
        variable_values['executors_names'] = self.current_task.executors_names
        # تسترهای تسک
        variable_values['testers_names'] = self.current_task.testers_names
        # مجری منتخب
        variable_values['selected_executor_gender'] = self.current_task.selected_executor.fullname_gender
        variable_values['selected_executor_title'] = self.current_task.selected_executor.fullname_title
        # تستر منتخب
        variable_values['selected_tester_gender'] = self.current_task.selected_tester.fullname_gender
        variable_values['selected_tester_title'] = self.current_task.selected_tester.fullname_title
        # وضعیت تسک
        variable_values['task_status'] = self.current_task.status_title
        
        # فراخوانی را انجام می دهیم
        result = send_email(template_code=template_code, variable_value=variable_values, to=to_users_emails, cc=None, bcc=None)
        
        # رکورد متناظر را در جدول سوابق اطلاع رسانی درج می کنیم
        nl = m.NotificationLog.objects.create(
            request=self.request_instance,
            request_status=self.status_title,
            template_code=template_code,
            email_to=to_users_emails,
            variables=variable_values,
            service_data=result,
            service_return_val=result.get('return_code',-1)
        )
        nl.creator_user = self.current_user_national_code
        nl.last_modifier_user = self.current_user_national_code
        nl.save()
        
    
    def save_step_data(
        self,
        current_status: str,
        action_code: str,
        form_data: dict,
        user_nationalcode: str,
    ):
        """
        ذخیره اطلاعات مرحله
        """
        try:
            # دریافت تاریخ و زمان فعلی به صورت شمسی
            current_date = jdatetime.datetime.now()
            current_time = current_date.strftime("%H:%M")

            # اگر وضعیت فعلی مدیر باشد
            if current_status == "DIRMAN":
                # ثبت نظر مدیر (تایید یا رد)
                self.request_instance.manager_opinion = action_code == "CON"
                # ثبت تاریخ و زمان نظر مدیر
                self.request_instance.manager_opinion_date = current_date.strftime(
                    "%Y/%m/%d"
                )
                self.request_instance.manager_opinion_time = current_time
                # اگر عملیات رد باشد، توضیح رد را ذخیره کن
                if action_code == "REJ":
                    self.request_instance.manager_reject_description = form_data.get(
                        "reject_reason"
                    )

            # اگر وضعیت فعلی مربوط به مرحله تکمیل اطلاعات باشد
            elif current_status == "RELMAN":
                # ذخیره اطلاعات کامل درخواست
                for field, value in form_data.items():
                    # اگر فیلد در مدل وجود داشته باشد، مقدار آن را به‌روزرسانی کن
                    if hasattr(self.request_instance, field):
                        setattr(self.request_instance, field, value)

            # اگر وضعیت فعلی کمیته باشد
            elif current_status == "COMITE":
                # ثبت نظر کمیته (تایید یا رد)
                self.request_instance.committee_opinion = action_code == "CON"
                # ثبت تاریخ و زمان نظر کمیته
                self.request_instance.committee_opinion_date = current_date.strftime(
                    "%Y/%m/%d"
                )
                self.request_instance.committee_opinion_time = current_time
                # اگر عملیات رد باشد، توضیح رد را ذخیره کن
                if action_code == "REJ":
                    self.request_instance.committee_reject_description = form_data.get(
                        "reject_reason"
                    )

            # ذخیره تغییرات در پایگاه داده
            self.request_instance.save()

        except Exception as e:
            # در صورت بروز خطا، هیچ اقدامی انجام نده
            pass

    def task_action(
        self,
        task_id: int,
        action_code: str,
        user_nationalcode: str,
        form_data: dict = None,
    ) -> dict:
        """
        عملیات روی تسک
        """
        try:
            task = self.get_task(task_id)
            if not task:
                return {"success": False, "message": "تسک پیدا نشد"}

            result = task.next_step(action_code)
            if result["success"]:
                # ذخیره اطلاعات تسک
                if form_data:
                    task.save(form_data)

                # ارسال به مرحله بعدی
                self.handle_task_completion(task_id)

            return result

        except Exception as e:
            return {"success": False, "message": f"خطا در عملیات تسک: {str(e)}"}

    def handle_task_completion(self, task_id: int):
        """
        مدیریت تکمیل تسک
        """
        try:
            # بررسی اینکه آیا همه تسک‌ها تکمیل شده‌اند
            request_tasks = m.RequestTask.objects.filter(request=self.request_instance)
            completed_tasks = request_tasks.filter(status_code="FINISH")

            if completed_tasks.count() == request_tasks.count():
                # همه تسک‌ها تکمیل شده‌اند
                self.request_instance.status_code = "FINISH"
                self.request_instance.save()
                # همگام‌سازی وضعیت و عنوان متناظر
                self.status_code = "FINISH"
                self._sync_status_title()

        except Exception as e:
            pass

    def get_request_data(self):
        """
        این تابع تمامی داده های یک درخواست را بازگشت می دهد
        از این داده ها برای بارگذاری فرم جهت انجام ویرایش استفاده می شود
        """
        data = {"success": True, "message": ""}

        try:
            if self.request_instance:
                # اطلاعات درخواست
                data["request"] = self.request_instance

                # اضافه کردن اطلاعات درخواست به data
                extra_info = m.RequestExtraInformation.objects.filter(
                    request_id=self.request_id
                )
                data["data_center_selected"] = list(
                    extra_info.filter(extra_info__Code__startswith='DataCenter_').values_list('extra_info__Code', flat=True)
                )
                data["database_selected"] = list(
                    extra_info.filter(extra_info__Code__startswith='Database_').values_list('extra_info__Code', flat=True)
                )
                data["system_services_selected"] = list(
                    extra_info.filter(extra_info__Code__startswith='SystemServices_').values_list('extra_info__Code', flat=True)
                )

                # اطلاعات تیم های مرتبط
                teams = m.RequestTeam.objects.filter(request_id=self.request_id).values_list('team_code__team_code',flat=True)
                data["request_teams"] = teams

                # اطلاعات شرکت های مرتبط
                corps = m.RequestCorp.objects.filter(request_id=self.request_id).values_list('corp_code__corp_code',flat=True)
                data["request_corps"] = corps

                # اطلاعات تسک ها
                tasks = m.RequestTask.objects.filter(request_id=self.request_id)
                data["request_tasks"] = tasks
                
                data["status_title"] = self.status_title
            else:
                return {"success": False, "message": "درخواست مورد نظر وجود ندارد"}

        except Exception as e:
            return {"success": False, "message": str(e)}

        return data

    def get_all_tasks(self):
        """
        این تابع تمامی تسک های تعریف شده ذیل یک درخواست را بازگشت می دهد
        """
        request_tasks = m.RequestTask.objects.filter(
            request=self.request_instance
        ).order_by("task__ordernumber")
        for request_task in request_tasks:
            t = Task(request_task, self.current_user_national_code)
            self.tasks.append(t)

    def get_task(self, request_task_id: int) -> Task:
        """این تابع شناسه تسک درخواست مربوطه را گرفته و آن را پیدا کرده و بازگشت می دهد

        Args:
            request_task_id (int): شناسه درخواست تسک

        Returns:
            Task: در صورتی که تسک مربوطه پیدا شود شناسه آن بازگشت داده می شود در غیر این صورت مقدار None بازگشت داده می شود
        """
        # اگر تسک ها قبلا بارگذاری نشده باشند بایستی بارگذاری شوند
        if not self.tasks:
            self.get_all_tasks()

        # حالا آرایه را بررسی می کنیم که اگر تسک مربوطه پیدا شود آن را بازگشت دهیم
        for t in self.tasks:
            t: Task
            if t.request_task_id == request_task_id:
                return t
        return None

    # # این تابع بررسی می کند که با توجه به وضعیت فعلی سیستم، کدام فرم و در چه حالتی برای این کاربر باید به چه صورتی نمایش داده شود؟
    # def check_form_status(self, user_nationalcode: str) -> dict:
    #     """
    #     این تابع با توجه به کاربر جاری و شناسه درخواست، مشخص می کند که کدام فرم و در چه حالتی باید باز شود

    #     Args:
    #         user_nationalcode (str): کد ملی کاربر جاری

    #     Returns:
    #         _type_: دو مقدار را بازگشت می دهد، اولی کد وضعیت و دومی فرمی که باید باز شود قالب مقدار بازگشتی به این صورت است
    #         {'status':'form_status','form':'form_name'}
    #     """

    #     # بررسی اعتبار request_id
    #     request_instance = self.request_instance
    #     status_code = self.status_code

    #     # اگر شناسه درخواست نامعتبر باشد  در حالت درج باید باز شود
    #     if not request_instance:
    #         return {"status": "INSERT", "form": "RequestSimple"}
    #     # مقادیر پیش فرض
    #     status = "READONLY"
    #     form = "RequestSimple"

    #     if user_nationalcode == self.user_requestor.national_code:
    #         form = "RequestSimple"
    #         if status_code == "DRAFTD":
    #             status = "UPDATE"
    #     elif user_nationalcode == self.user_direct_manager.national_code:
    #         form = "RequestSimple"
    #         if status_code == "DIRMAN":
    #             status = "UPDATE"
    #     elif user_nationalcode == self.user_related_manager.national_code:
    #         form = "RequestFull"
    #         if status_code == "RELMAN":
    #             status = "UPDATE"
    #     elif user_nationalcode == self.user_committee.national_code:
    #         form = "RequestFull"
    #         if status_code == "COMITE":
    #             status = "UPDATE"
    #     # اگر تسک را داشته باشیم باید کاربران تسک را کنترل کنیم
    #     elif self.task:
    #         # ابتدا کنترل می کنیم که

    #         # به دست آوردن لیست مجریان
    #         executor_list = task_user_list(self.request_id, -1, "E", False)
    #         # به دست آوردن لیست تسترها
    #         tester_list = task_user_list(self.request_id, -1, "T", False)
    #         if user_nationalcode in executor_list + tester_list:
    #             form = "TaskSelect"
    #             if request_instance.status_code == "DOTASK":
    #                 # اگر شماره تسک مشخص شده باشد
    #                 if request_task_id > 0:
    #                     # تسک مربوطه را به دست می آوریم
    #                     request_task = m.RequestTask.objects.filter(
    #                         id=request_task_id
    #                     ).first()
    #                     request_task_user = m.TaskUserSelected.objects.filter(
    #                         request_task=request_task_id
    #                     )
    #                     if request_task:
    #                         # اگر وضعیت تسک انتخاب شده باشد
    #                         if (
    #                             request_task.status_code == "EXESEL"
    #                             and request_task_user.filter()
    #                         ):
    #                             ...
    #                     # در صورتی که شناسه تسک درخواست نامعتبر باشد
    #                     else:
    #                         status = "INVALID"
    #                     status = "UPDATE"

    #         elif user_nationalcode in tester_list:
    #             form = "TaskSelect"
    #             if request_instance.status_code == "TESREP":
    #                 status = "UPDATE"

    #         # به دست آوردن لیست مجریان منتخب
    #         executor_list = task_user_list(self.request_id, -1, "E", True)
    #         # به دست آوردن لیست تسترهای منتخب
    #         tester_list = task_user_list(self.request_id, -1, "T", True)
    #         if user_nationalcode in executor_list:
    #             form = "TaskReport"
    #             if request_instance.status_code == "EXEREP":
    #                 status = "UPDATE"
    #         elif user_nationalcode in tester_list:
    #             form = "TaskReport"
    #             if request_instance.status_code == "TESREP":
    #                 status = "UPDATE"

    #     return {"status": status, "form": form}

    ############################################################################
    # این توابع مربوط به نسخه قدیمی است
    ############################################################################


# # این تابع شناسه درخواست را گرفته و در صورت وجود مقدار رکورد درخواست را برمی گرداند
# def get_request_instance(request_id:int):
#     try:
#         # دریافت درخواست بر اساس request_id
#         request_instance = m.ConfigurationChangeRequest.objects.get(id=request_id)
#     except m.ConfigurationChangeRequest.DoesNotExist:
#         return None
#     return request_instance

# # این تابع شناسه تسک مربوط به درخواست را گرفته و در صورت وجود مقدار رکورد درخواست را برمی گرداند
# def get_request_task_instance(request_task_id:int)->dict:
#     request_task_instance = None
#     task_users = None
#     executor_users = None
#     tester_users = None
#     executor_user = None
#     tester_user = None
#     try:
#         # دریافت درخواست بر اساس request_id
#         request_task_instance = m.RequestTask.objects.get(id=request_task_id)

#         # اطلاعات کلیه افراد مربوط به تسک
#         task_user = m.TaskUser.objects.filter(task=request_task_instance.task).values_list('user_nationalcode')
#         task_users = m.User.objects.filter(national_code__in=task_user)

#         # دریافت اطلاعات مجریان تسک
#         task_user = m.TaskUser.objects.filter(task=request_task_instance.task,user_role_code='E').values_list('user_nationalcode')
#         executor_users = m.User.objects.filter(national_code__in=task_user)

#         # دریافت اطلاعات تسترهای تسک
#         task_user = m.TaskUser.objects.filter(task=request_task_instance.task,user_role_code='T').values_list('user_nationalcode')
#         tester_users = m.User.objects.filter(national_code__in=task_user)

#         # دریافت اطلاعات مجری منتخب
#         selected_user = m.TaskUserSelected.objects.filter(request_task=request_task_instance, task_user__user_role_code='E').first()
#         if selected_user is not None:
#             executor_user = m.User.objects.filter(national_code=selected_user.task_user.user_nationalcode).first()

#         # دریافت اطلاعات تستر منتخب
#         selected_user = m.TaskUserSelected.objects.filter(request_task=request_task_instance, task_user__user_role_code='T').first()
#         if selected_user is not None:
#             tester_user = m.User.objects.filter(national_code=selected_user.task_user.user_nationalcode).first()

#     except m.ConfigurationChangeRequest.DoesNotExist:
#         request_task_instance = None

#     return {'request_task_instance':request_task_instance,
#             'task_users':task_users,
#             'executor_users':executor_users,
#             'tester_users':tester_users,
#             'executor_user':executor_user,
#             'tester_user':tester_user
#             }

# def task_user_list(request_id: int, request_task_id: int, role_code: str, selected_user: bool = False) -> list:
#     user_list = []

#     # اگر کد سمت معتبر نباشد
#     if role_code not in ('E', 'T', 'A'):
#         return user_list

#     request = get_request_instance(request_id)
#     # اگر شناسه درخواست معتبر باشد
#     if request:
#         # اگر تسک مربوطه مشخص شده باشد
#         if request_task_id > 0:
#             request_task_info = get_request_task_instance(request_task_id)
#             # اگر کاربر انتخاب شده باشد
#             if not selected_user:
#                 if role_code == 'E':
#                     user_list = request_task_info['executor_user']
#                 elif role_code == 'T':
#                     user_list = request_task_info['tester_user']
#             else:
#                 if role_code == 'E':
#                     user_list = request_task_info['executor_users']
#                 elif role_code == 'T':
#                     user_list = request_task_info['tester_users']
#                 else:
#                     user_list = request_task_info['task_users']
#         # در صورتی که شماره تسک ارسال نشده باشد تمامی مجریان تسک ها باید ارسال شود
#         else:
#             request_tasks = m.RequestTask.objects.filter(request=request).values_list('task_id')
#             if role_code == 'E':
#                 user_list = m.RequestTaskUser.objects.filter(task_id__in=request_tasks, user_role_code='E')
#             elif role_code == 'T':
#                 user_list = m.RequestTaskUser.objects.filter(task_id__in=request_tasks, user_role_code='T')
#             else:
#                 user_list = m.RequestTaskUser.objects.filter(task_id__in=request_tasks)

#     # بازگشت لیستی از اشیاء User
#     return [user.user_nationalcode for user in user_list]

# def get_request_user_information(request_id:int)->str:
#     """این تابع اطلاعات کاربر جاری درخواست را بازگشت می دهد

#     Args:
#         request_id (int): شناسه درخواست

#     Returns:
#         str: یک رشته که شامل نام و نام خانوادگی، سمت و تیم فرد مربوطه و عملیات مورد نظر می باشد
#         مثلا آقای رضا احمدی دبیر کمیته امنیت، جهت اعلام نظر
#         در صورتی که شناسه درخواست نامعتبر باشد،  مقدار رشته "نامشخص" بازگشت داده می شود
#     """
#     user_info = None
#     operation_info = None
#     team_info = None
#     role_info = None

#     request_instance = get_request_instance(request_id)
#     if not request_instance:
#         return 'نامشخص'

#     # برای اینکه بتوانیم اطلاعات کاربر را به دست بیاوریم، بایستی آخرین رکورد جدول گردش مدرک را بخوانیم
#     request_flow = m.RequestFlow.objects.filter(request = request_instance).last()
#     user_info = request_flow.user_nationalcode
#     role_info = request_flow.user_role_id.role_title
#     team_info = request_flow.user_team_code.team_name

#     # جهت مشخص شدن عملیات، باید وضعیت را به دست بیاوریم
#     status_code = request_instance.status_code

#     if status_code == 'DRAFTD':
#         operation_info = "تکمیل اطلاعات فرم"
#     elif status_code == 'DIRMAN' or 'RELMAN':
#         operation_info = "بررسی و اعلام نظر"
#     elif status_code == 'COMITE':
#         operation_info = "اعلام نظر کمیته"
#     elif status_code == 'DOTASK':
#         # اگر وضعیت درخواست مربوط به اجرای تسک باشد، باید آخرین تسک اجرا نشده را پیدا کنیم
#         request_task = m.RequestTask.object.filter(request=request_id, status_code__not_in=['FINISH','FAILED']).first()
#         return get_task_user_information(request_task.id)
#     # در صورتی که برای فردی ارسال شده باشد، مشخصات وی بازگشت داده می شود
#     if user_info and operation_info:
#         salutation = "آقای" if user_info.gender or user_info.gender is None else "خانم"
#         role_info = role_info if role_info is not None else ""
#         if team_info:
#             return f"{salutation} {user_info.first_name} {user_info.last_name} {role_info} تیم {team_info} جهت {operation_info}"
#         else:
#             return f"{salutation} {user_info.first_name} {user_info.last_name} {role_info} جهت {operation_info}"
#     else:
#         return "نامشخص"


# def get_task_user_information(request_task_id:int)->str:
#     """این تابع اطلاعات کاربر جاری فعالیت را بازگشت می دهد

#     Args:
#         request_id (int): شناسه تسک درخواست
#         status_code (str): کد وضعیت درخواست

#     Returns:
#         str: یک رشته که شامل نام و نام خانوادگی، سمت و تیم فرد مربوطه و عملیات مورد نظر می باشد
#         مثلا آقای رضا احمدی تستر تیم عمر جهت تست فعالیت
#         در صورتی که شناسه تسک درخواست نامعتبر باشد،  مقدار رشته "نامشخص" بازگشت داده می شود
#     """
#     user_info = None
#     operation_info = None
#     team_info = None
#     role_info = None

#     task_info = get_request_task_instance(request_task_id)
#     request_task_instance = task_info['request_task_instance']
#     if not request_task_instance:
#         return 'نامشخص'

#     # برای اینکه بتوانیم اطلاعات کاربر را به دست بیاوریم، بایستی آخرین رکورد جدول گردش مدرک را بخوانیم
#     request_flow = m.RequestFlow.objects.filter(request = request_task_instance.request).last()
#     user_info = request_flow.user_nationalcode
#     role_info = request_flow.user_role_id.role_title
#     team_info = request_flow.user_team_code.team_name

#     # جهت مشخص شدن عملیات، باید وضعیت را به دست بیاوریم
#     status_code = request_task_instance.status_code

#     if status_code == 'EXERED':
#         operation_info = "انتخاب مجری"
#     elif status_code == 'EXESEL' :
#         operation_info = "اجرای فعالیت"
#     elif status_code == 'TESRED':
#         operation_info = "انتخاب تستر"
#     elif status_code == 'TESSEL':
#         operation_info = "انجام تست"

#     # در صورتی که برای فردی ارسال شده باشد، مشخصات وی بازگشت داده می شود
#     if user_info and operation_info:
#         salutation = "آقای" if user_info.gender or user_info.gender is None else "خانم"
#         role_info = role_info if role_info is not None else ""
#         if team_info:
#             return f"{salutation} {user_info.first_name} {user_info.last_name} {role_info} تیم {team_info} جهت {operation_info}"
#         else:
#             return f"{salutation} {user_info.first_name} {user_info.last_name} {role_info} جهت {operation_info}"
#     else:
#         return "نامشخص"


# # این تابع درصورتی که کد درخواستی وجود داشته باشد، اطلاعات آن را به روز می کند و اگر وجود نداشته باشد آن را ایجاد می کند
# def save_form(form_data) -> int:
#     # بررسی وجود شناسه درخواست
#     request_id = form_data.get('request_id')


#     # کلیدهای خارجی را باید به معادل آن تبدیل کنیم چون برای مقداردهی به نمونه مربوطه احتیاج دارد و مقدار کلید را قبول نمی کند
#     executor_nationalcode = form_data.get('executor_user_nationalcode')
#     if executor_nationalcode:
#         executor_nationalcode = m.User.objects.get(national_code=executor_nationalcode)

#     tester_nationalcode = form_data.get('tester_user_nationalcode')
#     if tester_nationalcode:
#         tester_nationalcode = m.User.objects.get(national_code=tester_nationalcode)

#     requestor_nationalcode = form_data.get('requestor_user_nationalcode')
#     if requestor_nationalcode:
#         requestor_nationalcode = m.User.objects.get(national_code=requestor_nationalcode)

#     executor_role = None
#     executor_role_id = form_data.get('executor_user_role')
#     if executor_role_id:
#         try:
#             executor_role = m.Role.objects.get(role_id=executor_role_id)
#         except m.Role.DoesNotExist:
#             executor_role = None

#     tester_role = None
#     tester_role_id = form_data.get('tester_user_role')
#     if tester_role_id:
#         try:
#             tester_role = m.Role.objects.get(role_id=tester_role_id)
#         except m.Role.DoesNotExist:
#             tester_role = None

#     requestor_role = None
#     requestor_role_id = form_data.get('requestor_user_role')
#     if requestor_role_id:
#         try:
#             requestor_role = m.Role.objects.get(role_id=requestor_role_id)
#         except m.Role.DoesNotExist:
#             requestor_role = None

#     executor_team_code = form_data.get('executor_user_team')
#     if executor_team_code:
#         executor_team = m.Team.objects.get(team_code=executor_team_code)

#     tester_team_code = form_data.get('tester_user_team')
#     if tester_team_code:
#         tester_team = m.Team.objects.get(team_code=tester_team_code)

#     requestor_team_code = form_data.get('requestor_user_team')
#     if requestor_team_code:
#         requestor_team = m.Team.objects.get(team_code=requestor_team_code)


#     committee_user_nationalcode = form_data.get('committee_user_nationalcode')
#     if committee_user_nationalcode:
#         committee_user_nationalcode = m.User.objects.get(national_code=committee_user_nationalcode)

#     manager_nationalcode = form_data.get('manager_nationalcode')
#     if manager_nationalcode:
#         manager_nationalcode = m.User.objects.get(national_code=manager_nationalcode)


#     if request_id:
#         # به‌روزرسانی اطلاعات درخواست موجود
#         request = m.ConfigurationChangeRequest.objects.filter(id=request_id).first()
#         if request:
#             # نقش های درگیر
#             request.executor_nationalcode = executor_nationalcode
#             request.tester_nationalcode = tester_nationalcode
#             request.requestor_nationalcode = requestor_nationalcode

#             request.executor_team_code = executor_team
#             request.tester_team_code = tester_team
#             request.requestor_team_code = requestor_team

#             request.executor_role_id = executor_role
#             request.tester_role_id = tester_role
#             request.requestor_role_id = requestor_role

#             request.committee_user_nationalcode = committee_user_nationalcode

#             committee_id = form_data.get('committee')
#             if committee_id:
#                 request.committee_id = committee_id

#             request.need_committee = form_data.get('need_committee')

#             request.manager_nationalcode = manager_nationalcode

#             request.test_required = form_data.get('need_test')

#             # ویژگی های تغییر
#             request.change_level_id = form_data.get('change_level')
#             request.classification_id = form_data.get('classification')
#             request.priority_id = form_data.get('priority')
#             request.risk_level_id = form_data.get('risk_level')

#             # اطلاعات تغییر
#             request.change_title = form_data.get('change_title')
#             request.change_description = form_data.get('change_description')
#             request.change_type_id = form_data.get('change_type')

#             # محل تغییر
#             request.change_location_data_center_id = form_data.get('change_location_data_center')
#             request.change_location_database_id = form_data.get('change_location_database')
#             request.change_location_system_services_id = form_data.get('change_location_system_services')
#             request.change_location_other_id = form_data.get('change_location_other')
#             request.change_location_other_description_id = form_data.get('change_location_other_description')

#             # حوزه تغییر
#             request.change_domain_id = form_data.get('change_domain')

#             # زمانبندی تغییرات
#             request.changing_date = form_data.get('change_date')
#             request.changing_time = form_data.get('change_time')
#             request.changing_date_actual = form_data.get('changing_date_actual')
#             request.changing_duration = form_data.get('changing_duration')
#             request.changing_duration_actual = form_data.get('changing_duration_actual')
#             request.downtime_duration = form_data.get('downtime_duration')
#             request.downtime_duration_worstcase = form_data.get('downtime_duration_worstcase')
#             request.downtime_duration_actual = form_data.get('downtime_duration_actual')

#             # اثر گذاری تغییر
#             request.stop_critical_service = form_data.get('stop_critical_service')
#             request.critical_service_title = form_data.get('critical_service_title')
#             request.stop_sensitive_service = form_data.get('stop_sensitive_service')
#             request.stop_service_title = form_data.get('stop_service_title')
#             request.not_stop_any_service = form_data.get('not_stop_any_service')

#             # طرح بازگشت
#             request.has_role_back_plan = form_data.get('has_role_back_plan')
#             request.role_back_plan_description = form_data.get('role_back_plan_description')

#             # الزامات تغییر
#             request.reason_regulatory = form_data.get('reason_regulatory')
#             request.reason_technical = form_data.get('reason_technical')
#             request.reason_security = form_data.get('reason_security')
#             request.reason_business = form_data.get('reason_business')
#             request.reason_other = form_data.get('reason_other')
#             request.reason_other_description = form_data.get('reason_other_description')

#             # اطلاعات تکمیلی سایر مراحل
#             # نظر مدیر
#             request.manager_opinion = form_data.get('manager_opinion')
#             request.manager_opinion_date = form_data.get('manager_opinion_date')
#             request.manager_reject_description = form_data.get('manager_reject_description')

#             # نظر کمیته
#             request.committee_opinion = form_data.get('committee_opinion')
#             request.committee_opinion_date = form_data.get('committee_opinion_date')
#             request.committee_reject_description = form_data.get('committee_reject_description')

#             # گزارش اجرا
#             request.executor_report = form_data.get('executor_report')
#             request.executor_report_date = form_data.get('executor_report_date')
#             request.execution_description = form_data.get('execution_description')

#             # گزارش تست
#             request.test_date = form_data.get('test_date')
#             request.tester_report = form_data.get('tester_report')
#             request.tester_report_date = form_data.get('tester_report_date')
#             request.test_report_description = form_data.get('test_report_description')

#             request.save()
#     else:
#         # ایجاد درخواست جدید
#         request = m.ConfigurationChangeRequest.objects.create(
#             # نقش های درگیر

#             executor_nationalcode = executor_nationalcode
#             ,tester_nationalcode = tester_nationalcode
#             ,requestor_nationalcode = requestor_nationalcode

#             ,executor_team_code = executor_team
#             ,tester_team_code = tester_team
#             ,requestor_team_code = requestor_team

#             ,executor_role_id = executor_role
#             ,tester_role_id = tester_role
#             ,requestor_role_id = requestor_role

#             ,committee_user_nationalcode = committee_user_nationalcode
#             ,committee_id = form_data.get('committee')
#             ,need_committee = form_data.get('need_committee')

#             ,manager_nationalcode = manager_nationalcode
#             ,test_required = form_data.get('need_test')

#             # ویژگی های تغییر
#             ,change_level_id = form_data.get('change_level')
#             ,classification_id = form_data.get('classification')
#             ,priority_id = form_data.get('priority')
#             ,risk_level_id = form_data.get('risk_level')

#             # اطلاعات تغییر
#             ,change_title = form_data.get('change_title')
#             ,change_description = form_data.get('change_description')
#             ,change_type_id = form_data.get('change_type')

#             # محل تغییر
#             ,change_location_data_center = form_data.get('change_location_data_center')
#             ,change_location_database = form_data.get('change_location_database')
#             ,change_location_system_services = form_data.get('change_location_system_services')
#             ,change_location_other = form_data.get('change_location_other')
#             ,change_location_other_description = form_data.get('change_location_other_description')

#             # حوزه تغییر
#             ,change_domain_id = form_data.get('change_domain')

#             # زمانبندی تغییرات
#             ,changing_date = form_data.get('change_date')
#             ,changing_time = form_data.get('change_time')
#             ,changing_duration = form_data.get('changing_duration')
#             ,downtime_duration = form_data.get('downtime_duration')
#             ,downtime_duration_worstcase = form_data.get('downtime_duration_worstcase')

#             # اثر گذاری تغییر
#             ,stop_critical_service = form_data.get('stop_critical_service')
#             ,critical_service_title = form_data.get('critical_service_title')
#             ,stop_sensitive_service = form_data.get('stop_sensitive_service')
#             ,stop_service_title = form_data.get('stop_service_title')
#             ,not_stop_any_service = form_data.get('not_stop_any_service')

#             # طرح بازگشت
#             ,has_role_back_plan = form_data.get('has_role_back_plan')
#             ,role_back_plan_description = form_data.get('role_back_plan_description')

#             # الزامات تغییر
#             ,reason_regulatory = form_data.get('reason_regulatory')
#             ,reason_technical = form_data.get('reason_technical')
#             ,reason_security = form_data.get('reason_security')
#             ,reason_business = form_data.get('reason_business')
#             ,reason_other = form_data.get('reason_other')
#             ,reason_other_description = form_data.get('reason_other_description')
#         )

#     # حذف رکوردهای موجود و درج رکوردهای جدید
#     # تیم‌ها
#     # مواردی که هم اکنون در دیتابیس وجود دارد را استخراج می کنیم
#     existing_teams = m.RequestTeam.objects.filter(request=request)
#     for team_code in form_data.get('teams', []):
#         if team_code not in existing_teams:
#             # اگر موردی در لیست باشد که در دیتابیس وجود نداشته باشد آن را اضافه می کنیم
#             m.RequestTeam.objects.create(request=request, team_code_id=team_code)
#     # مواردی که در لیست نیستند ولی در دیتابیس هستند را حذف می کنیم
#     existing_teams.exclude(team_code_id__in=form_data.get('teams', [])).delete()

#     # شرکت‌ها
#     # مواردی که هم اکنون در دیتابیس وجود دارد را استخراج می کنیم
#     existing_corps = m.RequestCorp.objects.filter(request=request)
#     for corp_code in form_data.get('corps', []):
#         if corp_code not in existing_corps:
#             # اگر موردی در لیست باشد که در دیتابیس وجود نداشته باشد آن را اضافه می کنیم
#             m.RequestCorp.objects.create(request=request, corp_code_id=corp_code)
#     # مواردی که در لیست نیستند ولی در دیتابیس هستند را حذف می کنیم
#     existing_corps.exclude(corp_code_id__in=form_data.get('corps', [])).delete()

#     # اطلاعات تکمیلی
#     # مواردی که هم اکنون در دیتابیس وجود دارد را استخراج می کنیم
#     existing_extra_info = m.RequestExtraInformation.objects.filter(request=request)
#     for extra_info_id in form_data.get('extra_information', []):
#         if extra_info_id not in existing_extra_info:
#             # اگر موردی در لیست باشد که در دیتابیس وجود نداشته باشد آن را اضافه می کنیم
#             m.RequestExtraInformation.objects.create(request=request, extra_info_id=extra_info_id)
#     # مواردی که در لیست نیستند ولی در دیتابیس هستند را حذف می کنیم
#     existing_extra_info.exclude(extra_info_id__in=form_data.get('extra_information', [])).delete()

#     return request.id

# # این تابع صحت سنجی فرم را انجام می دهد در صورتی که خطا داشته باشد مقدار بازگشتی برابر با پیام های خطا خواهد بود
# def form_validation(form_data):
#     errors = []

#     # اعتبارسنجی فیلدهای الزامی
#     required_fields = {
#         'requestor_user_nationalcode': "کد ملی درخواست دهنده الزامی است.",
#         'requestor_user_role': "سمت درخواست‌دهنده الزامی است.",
#         'requestor_user_team': "تیم درخواست‌دهنده الزامی است.",
#         'executor_user_nationalcode': "کد ملی مجری الزامی است.",
#         'executor_user_role': "سمت مجری الزامی است.",
#         'executor_user_team': "تیم مجری الزامی است.",
#         'tester_user_nationalcode': "کد ملی تستر الزامی است.",
#         'tester_user_role': "سمت تستر الزامی است.",
#         'tester_user_team': "تیم تستر الزامی است.",
#         'change_title': "عنوان تغییر الزامی است.",
#         'change_description': "توضیحات تغییر الزامی است.",
#         'change_type': "نوع تغییر الزامی است.",
#     }

#     # اگر تست نیازی ندارد، نباید شناسه آن وجود داشته باشد
#     if form_data.get('need_test') == 0:
#         form_data.pop('tester_user_nationalcode', None)
#     else:
#         required_fields['tester_user_nationalcode'] = 'انتخاب تستر الزامی است.'

#     # اگر نیاز به کمیته ندارد، باید شناسه مربوطه حذف شود
#     if form_data.get('need_committee') == 0:
#         form_data.pop('committee', None)
#     else:
#         required_fields['committee'] = 'انتخاب کمیته الزامی است.'

#     # بررسی فیلدهای الزامی
#     for field, error_message in required_fields.items():
#         if not form_data.get(field):
#             errors.append(error_message)

#     # فیلدهای تاریخ
#     date_fields = [
#         ('change_date','تاریخ تغییرات'),
#         ('change_date_actual','تاریخ واقعی انجام تغییرات'),
#         ('test_date', 'تاریخ انجام تست'),
#         ('tester_report_date','تاریخ گزارش تست'),
#         ('manager_opinion_date','تاریخ اظهار نظر مدیر مستقیم'),
#         ('committee_opinion_date','تاریخ اظهار نظر کمیته'),
#     ]


#     for field, description in date_fields:
#         date = form_data.get(field)
#         if date:
#             try:
#                 # بررسی اینکه آیا ورودی از نوع رشته است
#                 if isinstance(date, str):
#                     # تبدیل به تاریخ شمسی
#                     date = jdatetime.datetime.strptime(date, '%Y/%m/%d')
#                 else:
#                     errors.append(f"فرمت تاریخ برای '{description}' نامعتبر است.")
#             except ValueError:
#                 errors.append(f"'{description}' باید در فرمت 'YYYY-MM-DD' باشد.")

#     time_fields = [
#         ('change_time','ساعت تغییرات'),
#         ('change_time_actual','ساعت واقعی انجام تغییرات'),
#         ('test_time', 'ساعت انجام تست'),
#         ('tester_report_time','ساعت گزارش تست'),
#         ('manager_opinion_time','ساعت اظهار نظر مدیر مستقیم'),
#         ('committee_opinion_time','ساعت اظهار نظر کمیته'),
#     ]

#     for field, description in time_fields:
#         time = form_data.get(field)
#         if time:
#             try:
#                 # بررسی اینکه آیا ورودی از نوع رشته است
#                 if isinstance(time, str):
#                     # بررسی اینکه آیا فرمت زمان صحیح است
#                     hours, minutes = map(int, time.split(':'))
#                     if 0 <= hours <= 24 and 0 <= minutes <= 59:
#                         pass
#                     else:
#                         errors.append(f"فرمت ساعت برای '{description}' نامعتبر است. ساعت باید بین 00:00 تا 23:59 باشد.")
#                 else:
#                     errors.append(f"فرمت ساعت برای '{description}' نامعتبر است.")
#             except ValueError:
#                 errors.append(f"'{description}' باید در فرمت 'HH:MM' باشد.")


#     # کد ملی درخواست کننده
#     if form_data.get('requestor_user_nationalcode') and not m.User.objects.filter(national_code=form_data['requestor_user_nationalcode']).exists():
#         errors.append("کد ملی درخواست کننده نامعتبر است.")

#     # تیم درخواست‌دهنده
#     if form_data.get('requestor_user_team') and not m.Team.objects.filter(team_code=form_data['requestor_user_team']).exists():
#         errors.append("تیم درخواست‌دهنده نامعتبر است.")

#     # کد ملی مجری
#     if form_data.get('executor_user_nationalcode') and not m.User.objects.filter(national_code=form_data['executor_user_nationalcode']).exists():
#         errors.append("کد ملی مجری نامعتبر است.")

#     # تیم مجری
#     if form_data.get('executor_user_team') and not m.Team.objects.filter(team_code=form_data['executor_user_team']).exists():
#         errors.append("تیم مجری نامعتبر است.")

#     # کد ملی تستر
#     if form_data.get('tester_user_nationalcode') and not m.User.objects.filter(national_code=form_data['tester_user_nationalcode']).exists():
#         errors.append("کد ملی تستر نامعتبر است.")

#     # تیم تستر
#     if form_data.get('tester_user_team') and not m.Team.objects.filter(team_code=form_data['tester_user_team']).exists():
#         errors.append("تیم تستر نامعتبر است.")

#     # کد ملی مدیر
#     if not form_data.get('manager_nationalcode'):
#         manager_nationalcode = m.UserTeamRole.objects.filter(team_code=form_data['requestor_user_team'], role_id=form_data['requestor_user_role']).values('manager_national_code').first()
#         if manager_nationalcode:
#             form_data['manager_nationalcode'] = manager_nationalcode['manager_national_code']
#         # حالتی است که مدیر کاربر پیدا نشده است
#         else:
#             errors.append("امکان تشخیص دادن مدیر کاربر درخواست دهنده وجود ندارد")
#     elif not m.User.objects.filter(national_code=form_data['manager_nationalcode']).exists():
#         errors.append("کد ملی مدیر نامعتبر است.")


#     # شناسه کمیته
#     if form_data.get('committee') and not m.Committee.objects.filter(id=form_data['committee']).exists():
#         errors.append("شناسه کمیته نامعتبر است.")

#     # کد ملی کاربر کمیته
#     if form_data.get('committee_user_nationalcode') and not m.User.objects.filter(national_code=form_data['committee_user_nationalcode']).exists():
#         errors.append("کد ملی کاربر کمیته نامعتبر است.")

#     if not form_data.get('committee_user_nationalcode'):
#         committee_user_nationalcode = m.Committee.objects.filter(id=form_data['committee']).values('administrator_nationalcode').first()
#         if committee_user_nationalcode:
#             form_data['committee_user_nationalcode'] = committee_user_nationalcode['administrator_nationalcode']
#         # حالتی است که مدیر کاربر پیدا نشده است
#         else:
#             errors.append("امکان تشخیص دادن کاربر کمیته وجود ندارد")
#     elif not m.User.objects.filter(national_code=form_data['committee_user_nationalcode']).exists():
#         errors.append("کد ملی کاربر کمیته نامعتبر است.")


#     # گستردگی تغییرات
#     if form_data.get('change_level') and not m.ConstValue.objects.filter(id=form_data['change_level']).exists():
#         errors.append("گستردگی تغییرات نامعتبر است.")

#     # طبقه‌بندی
#     if form_data.get('classification') and not m.ConstValue.objects.filter(id=form_data['classification']).exists():
#         errors.append("طبقه‌بندی نامعتبر است.")

#     # اولویت
#     if form_data.get('priority') and not m.ConstValue.objects.filter(id=form_data['priority']).exists():
#         errors.append("اولویت نامعتبر است.")

#     # سطح ریسک
#     if form_data.get('risk_level') and not m.ConstValue.objects.filter(id=form_data['risk_level']).exists():
#         errors.append("سطح ریسک نامعتبر است.")

#     # دامنه تغییر
#     if form_data.get('change_domain') and not m.ConstValue.objects.filter(id=form_data['change_domain']).exists():
#         errors.append("دامنه تغییر نامعتبر است.")


#     # نوع تغییر
#     if form_data.get('change_type') and not m.ChangeType.objects.filter(id=form_data['change_type']).exists():
#         errors.append("نوع تغییر نامعتبر است.")


#     # اعتبارسنجی محل تغییر: سایر
#     try:
#         validator.Validator.validate_change_location_other(
#             form_data.get('change_location_other'),
#             form_data.get('change_location_other_description')
#         )
#     except ValidationError as e:
#         errors.append(str(e))

#     # اعتبارسنجی توقف خدمات بحرانی و حساس
#     try:
#         validator.Validator.validate_critical_service(
#             form_data.get('stop_critical_service'),
#             form_data.get('critical_service_title')
#         )
#     except ValidationError as e:
#         errors.append(str(e))

#     try:
#         validator.Validator.validate_sensitive_service(
#             form_data.get('stop_sensitive_service'),
#             form_data.get('stop_service_title')
#         )
#     except ValidationError as e:
#         errors.append(str(e))

#     # اعتبارسنجی سایر الزامات
#     try:
#         validator.Validator.validate_reason_other(
#             form_data.get('reason_other'),
#             form_data.get('reason_other_description')
#         )
#     except ValidationError as e:
#         errors.append(str(e))

#     # اعتبارسنجی نظر مدیر
#     try:
#         validator.Validator.validate_manager_opinion(
#             form_data.get('manager_opinion'),
#             form_data.get('manager_reject_description')
#         )
#     except ValidationError as e:
#         errors.append(str(e))

#     # اعتبارسنجی فیلدهای کمیته
#     try:
#         validator.Validator.validate_committee_fields(
#             form_data.get('need_committee'),
#             form_data.get('committee_user_nationalcode'),
#             form_data.get('committee_opinion_date'),
#             form_data.get('committee_opinion'),
#             form_data.get('committee_reject_description')
#         )
#     except ValidationError as e:
#         errors.append(str(e))

#     # اعتبارسنجی تاریخ تست و گزارش تست
#     try:
#         validator.Validator.validate_test_date(
#             form_data.get('test_date'),
#             form_data.get('changing_date_actual')
#         )
#     except ValidationError as e:
#         errors.append(str(e))

#     try:
#         validator.Validator.validate_tester_report_date(
#             form_data.get('tester_report_date'),
#             form_data.get('test_date')
#         )
#     except ValidationError as e:
#         errors.append(str(e))

#     # اعتبارسنجی کلیدهای خارجی برای تیم‌ها
#     for team_code in form_data.get('teams', []):
#         if not m.Team.objects.filter(team_code=team_code).exists():
#             errors.append(f"کد تیم '{team_code}' نامعتبر است.")

#     # اعتبارسنجی کلیدهای خارجی برای شرکت‌ها
#     for corp_code in form_data.get('corps', []):
#         if not m.Corp.objects.filter(corp_code=corp_code).exists():
#             errors.append(f"کد شرکت '{corp_code}' نامعتبر است.")

#     # اعتبارسنجی مقادیر اطلاعات تکمیلی
#     for extra_info_id in form_data.get('extra_information', []):
#         if not m.ConstValue.objects.filter(id=extra_info_id).exists():
#             errors.append(f"مقدار اطلاعات تکمیلی با شناسه '{extra_info_id}' نامعتبر است.")

#     return errors
