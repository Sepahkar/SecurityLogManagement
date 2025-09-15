from django.core.management.base import BaseCommand
from ConfigurationChangeRequest.models import ConstValue

class Command(BaseCommand):
    help = 'Insert default const values into the database'

    def handle(self, *args, **kwargs):
        # تابع برای ایجاد رکوردها در صورت عدم وجود
        def create_if_not_exists(caption, code, parent=None):
            if not ConstValue.objects.filter(Code=code).exists():
                return ConstValue.objects.create(Caption=caption, Code=code, Parent=parent)
            return None

        # طبقه بندی تغییرات
        classification_parent = create_if_not_exists('طبقه بندی تغییرات', 'Classification')
        create_if_not_exists('عادی', 'Classification_Normal', classification_parent)
        create_if_not_exists('محرمانه', 'Classification_Confidential', classification_parent)

        # دامنه تغییرات
        scope_parent = create_if_not_exists('گستردگی تغییرات', 'ChangeLevel')
        create_if_not_exists('جزئی', 'ChangeLevel_Minor', scope_parent)
        create_if_not_exists('بخشی', 'ChangeLevel_Partial', scope_parent)
        create_if_not_exists('کلان', 'ChangeLevel_Major', scope_parent)

        # اولویت تغییر
        priority_parent = create_if_not_exists('اولویت تغییر', 'Priority')
        create_if_not_exists('استاندارد', 'Priority_Standard', priority_parent)
        create_if_not_exists('فوری', 'Priority_Urgent', priority_parent)
        create_if_not_exists('اضطراری', 'Priority_Emergency', priority_parent)

        # سطح ریسک تغییر
        risk_level_parent = create_if_not_exists('سطح ریسک تغییر', 'RiskLevel')
        create_if_not_exists('پایین', 'RiskLevel_Low', risk_level_parent)
        create_if_not_exists('متوسط', 'RiskLevel_Moderate', risk_level_parent)
        create_if_not_exists('بالا', 'RiskLevel_High', risk_level_parent)

        # تغییرات مرکز داده
        data_center_parent = create_if_not_exists('تغییرات مرکز داده', 'DataCenter')
        create_if_not_exists('ارتباطات مخابراتی', 'DataCenter_Telecommunications', data_center_parent)
        create_if_not_exists('ارتباطات شبکه ای', 'DataCenter_Networking', data_center_parent)
        create_if_not_exists('تجهیزات پردازشی و ذخیره سازی', 'DataCenter_ProcessingStorage', data_center_parent)
        create_if_not_exists('برق', 'DataCenter_Power', data_center_parent)
        create_if_not_exists('سیستم های خنک کننده', 'DataCenter_CoolingSystems', data_center_parent)

        # سیستم ها و سرویس ها
        systems_services_parent = create_if_not_exists('سیستم ها و سرویس ها', 'SystemsServices')
        create_if_not_exists('API Manager', 'SystemsServices_APIManager', systems_services_parent)
        create_if_not_exists('Core', 'SystemsServices_Core', systems_services_parent)

        # محدوده تغییر
        change_scope_parent = create_if_not_exists('حوزه تغییر', 'Domain')
        create_if_not_exists('درون سازمانی', 'Domain_Inside', change_scope_parent)
        create_if_not_exists('بین سازمانی', 'Domain_Between', change_scope_parent)
        create_if_not_exists('برون سازمانی', 'Domain_Outside', change_scope_parent)

        # نوع پیوست
        attachment_type_parent = create_if_not_exists('نوع پیوست', 'AttachmentType')
        create_if_not_exists('طرح تغییرات', 'AttachmentType_ChangePlan', attachment_type_parent)
        create_if_not_exists('طرح بازگشت', 'AttachmentType_ReturnPlan', attachment_type_parent)

        # وضعیت
        status_parent = create_if_not_exists('وضعیت', 'Status')
        create_if_not_exists('پیش نویس', 'Status_DRAFTD', status_parent)
        create_if_not_exists('بررسی مدیر مستقیم', 'Status_DIRMAN', status_parent)
        create_if_not_exists('بررسی مدیر مربوطه', 'Status_RELMAN', status_parent)
        create_if_not_exists('بررسی کمیته', 'Status_COMITE', status_parent)
        create_if_not_exists('اجرای تسک ها', 'Status_EXESEL', status_parent)
        create_if_not_exists('خاتمه یافته', 'Status_FINISH', status_parent)
        create_if_not_exists('خاتمه ناموفقیت آمیز', 'Status_FAILED', status_parent)
        create_if_not_exists('خاتمه با خطا', 'Status_ERRORF', status_parent)

        # سمت
        role_parent = create_if_not_exists('سمت', 'Role')
        create_if_not_exists('تکمیل کننده', ' Role_Requestor',  role_parent)
        create_if_not_exists('مدیر مستقیم', ' Role_DirectManager',  role_parent)
        create_if_not_exists('مدیر مربوطه', ' Role_RelatedManager',  role_parent)
        create_if_not_exists('دبیر کمیته', ' Role_Committe',  role_parent)
        create_if_not_exists('مجری', ' Role_Executor',  role_parent)
        create_if_not_exists('تستر', ' Role_Tester',  role_parent)

        # وضعیت تسک ها
        status_parent = create_if_not_exists('وضعیت', 'TaskStatus')
        create_if_not_exists('تعریف', 'TaskStatus_DEFINE', status_parent)
        create_if_not_exists('آماده انتخاب مجری', 'TaskStatus_EXERED', status_parent)
        create_if_not_exists('انتخاب شده مجری', 'TaskStatus_EXESEL', status_parent)
        create_if_not_exists('اجرای موفق', 'TaskStatus_EXEFIN', status_parent)
        create_if_not_exists('اجرای ناموفق', 'TaskStatus_EXEFAL', status_parent)
        create_if_not_exists('آماده انتخاب تستر', 'TaskStatus_TESRED', status_parent)
        create_if_not_exists('انتخاب شده تستر', 'TaskStatus_TESSEL', status_parent)
        create_if_not_exists('تست موفق', 'TaskStatus_TESFIN', status_parent)
        create_if_not_exists('تست ناموفق', 'TaskStatus_TESFAL', status_parent)
        create_if_not_exists('خاتمه موفق', 'TaskStatus_FINISH', status_parent)
        create_if_not_exists('خاتمه ناموفق', 'TaskStatus_FAILED', status_parent)


        self.stdout.write(self.style.SUCCESS('Default const values inserted successfully.'))
