import re
from datetime import datetime
from django.core.exceptions import ValidationError
from django.apps import apps

class Validator:
    @staticmethod
    def NationalCode_Validator(value):
        if not re.search(r'^\d{10}$', value):
            raise ValidationError("کد ملی صحیح نیست")
        check = int(value[9])
        s = sum(int(value[x]) * (10 - x) for x in range(9)) % 11

        if (s < 2 and check == s) or (check + s == 11):
            return True
        else:
            raise ValidationError("کد ملی صحیح نیست")
        return False


    @staticmethod
    def ConstValue_Validator(value, prefix):
        # from .models import ConstValue as cv
        if value is not None:
            cv = apps.get_model('ConfigurationChangeRequest', 'ConstValue')
            # بررسی اینکه آیا مقدار با الگوی مشخص شده مطابقت دارد
            if not value.code.startswith(prefix):
                # دریافت مقادیر مجاز از جدول ConstValue
                valid_values = cv.objects.filter(
                    code__startswith=prefix,
                    isactive=True
                ).order_by('ordernumber').values_list('caption', flat=True)

                # تبدیل مقادیر به رشته‌ای جدا شده با کاما
                valid_values_str = ', '.join(valid_values)

                raise ValidationError(f"مقدار وارد شده معتبر نیست. مقادیر مجاز: {valid_values_str}")
        return value

    
    @staticmethod
    def validate_change_location_other(change_location_other, change_location_other_description):
        if change_location_other and not change_location_other_description:
            raise ValidationError("اگر محل تغییر: سایر انتخاب شده است، باید توضیحات مربوطه وارد شود.")    
    @staticmethod
    def validate_critical_service(stop_critical_service, critical_service_title):
        if stop_critical_service and not critical_service_title:
            raise ValidationError("اگر سرویس های بحرانی متوقف می‌شود، باید عنوان آن سرویس ها وارد شود.")

    @staticmethod
    def validate_sensitive_service(stop_sensitive_service, stop_service_title):
        if stop_sensitive_service and not stop_service_title:
            raise ValidationError("اگر سرویس های حساس متوقف می‌شود، باید عنوان آن سرویس ها وارد شود.")

    @staticmethod
    def validate_reason_other(reason_other, reason_other_description):
        if reason_other and not reason_other_description:
            raise ValidationError("اگر سایر الزامات انتخاب شده است، باید توضیحات مربوطه وارد شود.")

    @staticmethod
    def validate_manager_opinion(manager_opinion, manager_reject_description):
        if manager_opinion != None:
            if not manager_opinion and not manager_reject_description:
                raise ValidationError("اگر نظر مدیر منفی است، توضیحات رد باید وارد شود.")

    @staticmethod
    def validate_committee_fields(need_committee, committee_user_nationalcode, committee_opinion_date, committee_opinion, committee_reject_description):
        if not need_committee:
            if committee_user_nationalcode or committee_opinion_date or committee_opinion is not None or committee_reject_description:
                raise ValidationError("اگر نیازی به کمیته نیست، هیچ یک از فیلدهای مربوط به کمیته نباید مقدار داشته باشند.")
            

    @staticmethod
    def validate_committee_opinion(committee_opinion, committee_reject_description):
        if committee_opinion is False and not committee_reject_description:
            raise ValidationError("اگر نظر کمیته منفی است، توضیحات رد باید وارد شود.")

    @staticmethod
    def validate_test_date(test_date, changing_date_actual):
        # بررسی اینکه هر دو تاریخ مقدار دارند
        if test_date and changing_date_actual:
            if test_date <= changing_date_actual:
                raise ValidationError("تاریخ انجام تست باید بزرگتر از تاریخ تغییرات باشد.")

    @staticmethod
    def validate_tester_report_date(tester_report_date, test_date):
        if tester_report_date and test_date:
            if tester_report_date <= test_date:
                raise ValidationError("تاریخ گزارش تست باید بزرگتر از تاریخ انجام تست باشد.")
                
                    
class DefaultValue:

    statuscode_draft = 'DRAFTD'

    