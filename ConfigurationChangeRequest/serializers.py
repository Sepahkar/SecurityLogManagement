from rest_framework import serializers
from .models import ConfigurationChangeRequest, User
from rest_framework.exceptions import ValidationError
from .validator import Validator as v

class ConfigurationChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigurationChangeRequest
        fields = '__all__'  # یا می‌توانید فیلدهای خاصی را مشخص کنید 

    def validate_requestor_nationalcode(self, value):
        if not value:
            raise ValidationError("کد ملی درخواست کننده الزامی است.")
        if not User.objects.filter(national_code=value).exists():
            raise ValidationError("کد ملی درخواست کننده در سیستم وجود ندارد.")
        return value

    def validate_executor_nationalcode(self, value):
        if not value:
            raise ValidationError("کد ملی مجری الزامی است.")
        if not User.objects.filter(national_code=value).exists():
            raise ValidationError("کد ملی مجری در سیستم وجود ندارد.")
        return value

    def validate_tester_nationalcode(self, value):
        if not value:
            raise ValidationError("کد ملی تستر الزامی است.")
        if not User.objects.filter(national_code=value).exists():
            raise ValidationError("کد ملی تستر در سیستم وجود ندارد.")
        return value

    def validate(self, data):
        # اعتبارسنجی عمومی
        if not data.get('requestor_nationalcode'):
            raise ValidationError("کد ملی درخواست کننده الزامی است.")
        
        if not data.get('change_title'):
            raise ValidationError("عنوان تغییر الزامی است.")
        
        if not data.get('change_description'):
            raise ValidationError("توضیحات تغییر الزامی است.")

        if data.get('test_required') and not data.get('tester_nationalcode'):
            raise ValidationError("اگر نیاز به تست وجود دارد، کد ملی تستر الزامی است.")

        # اعتبارسنجی تاریخ‌ها
        if data.get('test_date') and data.get('changing_date_actual'):
            v.validate_test_date(data['test_date'], data['changing_date_actual'])

        if data.get('tester_report_date') and data.get('test_date'):
            v.validate_tester_report_date(data['tester_report_date'], data['test_date'])

        # اعتبارسنجی با استفاده از توابع Validator
        v.validate_change_location_other(data.get('change_location_other'), data.get('change_location_other_description'))
        v.validate_critical_service(data.get('stop_critical_service'), data.get('critical_service_title'))
        v.validate_sensitive_service(data.get('stop_sensitive_service'), data.get('stop_service_title'))
        v.validate_reason_other(data.get('reason_other'), data.get('reason_other_description'))
        v.validate_manager_opinion(data.get('manager_opinion'), data.get('manager_reject_description'))

        # بررسی تاریخ تست و تاریخ اجرا
        if data.get('test_date') and data.get('changing_date_actual'):
            if data['test_date'] <= data['changing_date_actual']:
                raise ValidationError("تاریخ انجام تست باید بزرگتر از تاریخ اجرا باشد.")

        return data