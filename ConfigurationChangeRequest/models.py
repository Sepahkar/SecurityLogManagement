from django.db import models
import jdatetime
from django.core.validators import MinValueValidator
from ConfigurationChangeRequest.validator import Validator as v, DefaultValue as d
from django.core.exceptions import ValidationError
# Create your models here.

class User(models.Model):
    national_code = models.CharField(max_length=10, primary_key=True, verbose_name='کد ملی', 
                                    null=False, help_text='لطفاً کد ملی خود را وارد کنید.',
                                    validators=[v.NationalCode_Validator])
    first_name = models.CharField(max_length=100, verbose_name='نام', null=False, help_text='لطفاً نام خود را وارد کنید.')
    last_name = models.CharField(max_length=100, verbose_name='نام خانوادگی', null=False, help_text='لطفاً نام خانوادگی خود را وارد کنید.')
    username = models.CharField(max_length=100, verbose_name='نام کاربری', null=False, help_text='لطفاً نام کاربری خود را وارد کنید.')
    gender = models.BooleanField(default=True, verbose_name='جنسیت', help_text='در صورتی که مرد باشد مقدار صحیح و در غیر این صورت مقدار غلط خواهد داشت')
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        managed = True

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"


    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.national_code})"

class UserTeamRole(models.Model):
    national_code = models.ForeignKey(to='user', db_column='national_code', verbose_name='کد ملی کاربر', related_name='user', on_delete=models.CASCADE)    
    role_id = models.IntegerField(verbose_name="شناسه سمت")
    role_title = models.CharField(max_length=100, verbose_name='سمت کاربر', null=False, help_text='لطفاً سمت خود را وارد کنید.')
    team_code = models.ForeignKey('Team', on_delete=models.SET_NULL, verbose_name='تیم کاربر', null=True, blank=True, help_text='تیم مربوط به کاربر را انتخاب کنید.', db_column='team_code')
    manager_national_code = models.ForeignKey(to='user', db_column='manager_national_code', null=True, verbose_name='کد ملی مدیر مستقیم', related_name='direct_manager',on_delete=models.SET_NULL)    

    class Meta:
        verbose_name = 'سمت کاربر'
        verbose_name_plural = 'سمت های کاربران'

    def __str__(self) -> str:
        return f"{self.role_title} {self.team_code.team_name}"

class ConstValue(models.Model):
    class Meta:
        verbose_name = "مقدار ثابت"
        verbose_name_plural = "مقادیر ثابت"
        ordering = ["Parent_id", "OrderNumber"]

    Caption = models.CharField(max_length=50, verbose_name="عنوان")
    Code = models.CharField(max_length=100, verbose_name="کد")
    Parent = models.ForeignKey("ConstValue", verbose_name="شناسه پدر", on_delete=models.CASCADE, null=True, blank=True)
    IsActive = models.BooleanField(verbose_name="فعال است؟", default=True)
    OrderNumber = models.PositiveSmallIntegerField(verbose_name="شماره ترتیب", null=True, blank=True, default=1)
    ConstValue = models.IntegerField(verbose_name="مقدار مربوطه"  # , validators=[jv.MinValueValidator(1)]
                                    , null=True,
                                    blank=True)

    def __str__(self):
        return self.Caption

class Corp(models.Model):
    corp_code = models.CharField(max_length=3, primary_key=True, verbose_name='کد شرکت', null=False, help_text='کد منحصر به فرد شرکت را وارد کنید.')
    corp_name = models.CharField(max_length=100, verbose_name='نام شرکت', null=False, help_text='نام شرکت را وارد کنید.')

    class Meta:
        verbose_name = 'شرکت'
        verbose_name_plural = 'شرکت‌ها'
        managed = True

    def __str__(self):
        
        return self.corp_name

class Team(models.Model):
    team_code = models.CharField(max_length=3, primary_key=True, verbose_name='کد تیم', null=False, help_text='کد منحصر به فرد تیم را وارد کنید.')
    team_name = models.CharField(max_length=100, verbose_name='نام تیم', null=False, help_text='نام تیم را وارد کنید.')

    class Meta:
        verbose_name = 'تیم'
        verbose_name_plural = 'تیم‌ها'
        managed = True

    def __str__(self):
        return self.team_name

class Role(models.Model):
    role_id = models.IntegerField(primary_key=True, verbose_name='شناسه سمت')
    role_title = models.CharField(max_length=150, verbose_name='عنوان سمت')

    class Meta:
        verbose_name = 'سمت'
        verbose_name_plural = 'سمت‌ها'
        managed = True

    def __str__(self):
        return self.role_title

class Committee(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان کمیته', null=False)
    administrator_nationalCode = models.ForeignKey(to='User', on_delete=models.SET_NULL, 
                                            related_name='administrator', null=True,
                                            db_column='administrator_nationalcode',
                                            verbose_name='کد ملی دبیر کمیته')
    is_active = models.BooleanField(verbose_name='کمیته فعال است؟', default=True)
    
    class Meta:
        verbose_name = 'کمیته'
        verbose_name_plural = 'کمیته ها'

    def __str__(self) -> str:
        return self.Title    

class ChangeType(models.Model):
    code = models.CharField(max_length=6, verbose_name='کد نوع تغییر', db_column='code',
                            null=True, help_text='لطفاً کد نوع تغییر را وارد کنید.')
    change_type_title = models.CharField(max_length=255, verbose_name='عنوان نوع تغییر', null=True)
    change_title = models.CharField(max_length=255, verbose_name='عنوان تغییر', null=True, 
                                    help_text='لطفاً عنوان تغییر را وارد کنید.')
    change_description = models.TextField(max_length=1000, verbose_name='توضیحات تغییر', 
                                        null=True, blank=True, help_text='توضیحات مربوط به تغییر را وارد کنید.')
    change_location_data_center = models.BooleanField(default=False, verbose_name='محل تغییر: مرکز داده', null=True,
                                                    help_text='آیا تغییر در مرکز داده انجام می‌شود؟')
    change_location_database = models.BooleanField(default=False, verbose_name='محل تغییر: پایگاه داده', null=True,
                                                help_text='آیا تغییر در پایگاه داده انجام می‌شود؟')
    change_location_systems = models.BooleanField(default=False, verbose_name='محل تغییر: سیستم‌ها', null=True,
                                                help_text='آیا تغییر در سیستم‌ها انجام می‌شود؟')
    change_location_other = models.BooleanField(default=False, verbose_name='محل تغییر: سایر', null=True,
                                                help_text='آیا تغییر در محل دیگری انجام می‌شود؟')
    change_location_other_description = models.CharField(
        max_length=500, 
        verbose_name='توضیحات محل تغییر', 
        null=True, 
        blank=True, 
        help_text='توضیحات مربوط به محل تغییر را وارد کنید.',)

    # اطلاعات افراد درگیر
    executor_nationalcode = models.ForeignKey(User, on_delete=models.CASCADE, 
                                            related_name='executors', 
                                            db_column='executor_nationalcode',
                                            verbose_name='کد ملی کاربر مجری', 
                                            null=True, blank=True)
    tester_nationalcode = models.ForeignKey(User, on_delete=models.CASCADE, 
                                            related_name='testers', 
                                            db_column='tester_nationalcode',
                                            verbose_name='کد ملی کاربر تست کننده', 
                                            null=True, blank=True)
    test_required = models.BooleanField(verbose_name='نیازمند تست است؟', 
                                        default=False, 
                                        null=True,
                                        help_text='در صورتی که نیاز به تست داشته باشد مقدار یک و در غیر این صورت مقدار صفر خواهد داشت')
    need_committee = models.BooleanField(default=False, 
                                        verbose_name='نیاز به کمیته',
                                        null=True,
                                        help_text='آیا نیاز به کمیته وجود دارد؟')
    committee = models.ForeignKey(to='Committee', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='کمیته' )

    # ویژگی های تغییر
    change_level = models.ForeignKey(to="ConstValue",
                                    on_delete=models.SET_NULL, 
                                    verbose_name='گستردگی تغییرات', 
                                    null=True, 
                                    related_name= "change_level",
                                    help_text='تغییرات می تواند جزئی، بخشی و یا کلان باشد.')
    classification = models.ForeignKey(to="ConstValue", 
                                    on_delete=models.SET_NULL,
                                    verbose_name='طبقه‌بندی', 
                                    null=True, 
                                    related_name= "classification",
                                    help_text='طبقه‌بندی می تواند عادی یا محرمانه باشد.' )
    priority = models.ForeignKey(to="ConstValue", 
                                on_delete=models.SET_NULL,
                                verbose_name='اولویت',
                                null=True,
                                related_name= "priority",
                                help_text='اولویت می تواند استاندارد، فوری و اضطراری باشد.')
    risk_level = models.ForeignKey(to="ConstValue", 
                                on_delete=models.SET_NULL, 
                                verbose_name='سطح ریسک',
                                null=True, 
                                related_name= "risk_level",
                                help_text='سطح ریسک می تواند بالا، متوسط و پایین باشد.')
    change_domain = models.ForeignKey(to="ConstValue", 
                                    on_delete=models.SET_NULL, 
                                    verbose_name='دامنه تغییر',
                                    null=True, 
                                    related_name= "change_domain",
                                    help_text='دامنه تغییرات می تواند درون سازمانی، برون سازمانی و یا بین سازمانی باشد.')
    
    changing_duration = models.PositiveIntegerField(verbose_name='مدت زمان تغییرات', 
                                            null=True, blank=True, help_text='مدت زمان تغییرات بر حسب دقیقه.')
    downtime_duration = models.PositiveIntegerField(verbose_name='مدت زمان توقف', 
                                            null=True, blank=True, help_text='مدت زمان توقف بر حسب دقیقه.')
    downtime_duration_worstcase = models.PositiveIntegerField(verbose_name='بدترین مدت زمان توقف', 
                                            null=True, blank=True, help_text='مدت زمان توقف بر حسب دقیقه.')
    
    
    stop_critical_service = models.BooleanField(default=False, verbose_name='توقف خدمات بحرانی', null=True,
                                                help_text='آیا خدمات بحرانی متوقف می‌شود؟')
    critical_service_title = models.CharField(max_length=50,verbose_name='خدمات بحرانی', 
                                            null=True, blank=True, help_text='عنوان خدمات بحرانی را وارد کنید.')
    stop_sensitive_service = models.BooleanField(default=False, verbose_name='توقف خدمات حساس', null=True,   
                                                help_text='آیا خدمات حساس متوقف می‌شود؟')
    stop_service_title = models.CharField(max_length=200, verbose_name='عنوان خدمات متوقف شده', 
                                        null=True, blank=True, help_text='عنوان خدمات متوقف شده را وارد کنید.')
    not_stop_any_service = models.BooleanField(default=False, verbose_name='عدم توقف هیچ خدماتی', null=True,
                                            help_text='آیا هیچ خدماتی متوقف نمی‌شود؟')
    has_role_back_plan = models.BooleanField(default=False, verbose_name='برنامه بازگشت وجود دارد', null=True,
                                            help_text='آیا برنامه بازگشت وجود دارد؟')
    role_back_plan_description = models.CharField(max_length=1000, verbose_name='توضیحات برنامه بازگشت',
                                                null=True, blank=True, help_text='توضیحات مربوط به برنامه بازگشت را وارد کنید.')
    reason_regulatory = models.BooleanField(default=False, verbose_name='الزام قانونی', null=True,
                                            help_text='آیا الزام قانونی وجود دارد؟')
    reason_technical = models.BooleanField(default=False, verbose_name='الزام فنی', null=True,
                                        help_text='آیا الزام فنی وجود دارد؟')
    reason_security = models.BooleanField(default=False, verbose_name='الزام امنیتی', null=True,
                                        help_text='آیا الزام امنیتی وجود دارد؟')
    reason_business = models.BooleanField(default=False, verbose_name='الزام کسب و کاری', null=True,
                                        help_text='آیا الزام کسب و کاری وجود دارد؟')
    reason_other = models.BooleanField(default=False, verbose_name='سایر الزامات', null=True,
                                    help_text='آیا الزامات دیگری وجود دارد؟')
    reason_other_description = models.CharField(max_length=500, verbose_name='توضیحات الزامات دیگر', 
                                                null=True, blank=True, 
                                                help_text='توضیحات مربوط به الزامات دیگر را وارد کنید.')


    class Meta:
        verbose_name = 'نوع تغییر'
        verbose_name_plural = 'انواع تغییرات'
        managed = True

    def __str__(self):
        return self.Code
    
    def clean(self) -> None:
        v.ConstValue_Validator(prefix="change_level")
        v.ConstValue_Validator(prefix="classification")
        v.ConstValue_Validator(prefix="priority")
        v.ConstValue_Validator(prefix="risk_level")
        v.ConstValue_Validator(prefix="change_domain")
        return super().clean()

class ConfigurationChangeRequest(models.Model):
    # اطلاعات درخواست

    doc_id = models.IntegerField(verbose_name='کد سند', null=True, 
                                help_text='لطفاً کد سند را وارد کنید.')
    STATUS_CHOICES = [
        ('DRAFTD', 'پیش نویس'),
        ('MANAGE', 'اظهار نظر مدیر مستقیم'),
        ('COMITE', 'اظهار نظر کمیته'),
        ('EXECUT', 'اجرا توسط مجری'),
        ('TESTER', 'تست توسط تستر'),
        ('FINISH', 'خاتمه یافته'),
        ('FAILED', 'خاتمه ناموفقیت آمیز'),
    ]

    status_code = models.CharField(
        max_length=6,
        choices=STATUS_CHOICES,
        verbose_name='کد وضعیت',
        default='DRAFTD',
        help_text='لطفاً کد وضعیت را وارد کنید.'
    )
    
    # اطلاعات تغییر
    change_type = models.ForeignKey(ChangeType, on_delete=models.CASCADE, verbose_name='کد نوع تغییر',
                                        null=False)
    # اطلاعات افراد درگیر
    
    # ویژگی های تغییر
    change_level = models.ForeignKey(to="ConstValue",
                                    on_delete=models.SET_NULL, 
                                    verbose_name='گستردگی تغییرات', 
                                    null=True, 
                                    related_name= "request_change_level",
                                    help_text='تغییرات می تواند جزئی، بخشی و یا کلان باشد.')
    classification = models.ForeignKey(to="ConstValue", 
                                    on_delete=models.SET_NULL,
                                    verbose_name='طبقه‌بندی', 
                                    null=True, 
                                    related_name= "request_classification",
                                    help_text='طبقه‌بندی می تواند عادی یا محرمانه باشد.' )
    priority = models.ForeignKey(to="ConstValue", 
                                on_delete=models.SET_NULL,
                                verbose_name='اولویت',
                                null=True,
                                related_name= "request_priority",
                                help_text='اولویت می تواند استاندارد، فوری و اضطراری باشد.')
    risk_level = models.ForeignKey(to="ConstValue", 
                                on_delete=models.SET_NULL, 
                                verbose_name='سطح ریسک',
                                null=True, 
                                related_name= "request_risk_level",
                                help_text='سطح ریسک می تواند بالا، متوسط و پایین باشد.')
    
    # حوزه و ارتباطات تغییر
    change_domain = models.ForeignKey(to="ConstValue", 
                                    on_delete=models.SET_NULL, 
                                    verbose_name='دامنه تغییر',
                                    null=True, 
                                    related_name= "request_change_domain",
                                    help_text='دامنه تغییرات می تواند درون سازمانی، برون سازمانی و یا بین سازمانی باشد.')
    
    # اطلاعات تغییر
    change_title = models.CharField(max_length=255, verbose_name='عنوان تغییر', null=False, 
                                    help_text='لطفاً عنوان تغییر را وارد کنید.')
    change_description = models.TextField(max_length=1000, verbose_name='توضیحات تغییر', 
                                        null=True, blank=True, help_text='توضیحات مربوط به تغییر را وارد کنید.')
    # محل تغییر
    change_location_data_center = models.BooleanField(default=False, verbose_name='محل تغییر: مرکز داده', 
                                                    help_text='آیا تغییر در مرکز داده انجام می‌شود؟')
    change_location_database = models.BooleanField(default=False, verbose_name='محل تغییر: پایگاه داده', 
                                                help_text='آیا تغییر در پایگاه داده انجام می‌شود؟')
    change_location_systems = models.BooleanField(default=False, verbose_name='محل تغییر: سیستم‌ها', 
                                                help_text='آیا تغییر در سیستم‌ها انجام می‌شود؟')
    change_location_other = models.BooleanField(default=False, verbose_name='محل تغییر: سایر', 
                                                help_text='آیا تغییر در محل دیگری انجام می‌شود؟')
    change_location_other_description = models.CharField(
        max_length=500, 
        verbose_name='توضیحات محل تغییر', 
        null=True, 
        blank=True, 
        help_text='توضیحات مربوط به محل تغییر را وارد کنید.',
        validators=[v.validate_change_location_other]
    )
    
    # زمانبندی تغییرات
    changing_date = models.CharField(max_length=10, 
                                        verbose_name='تاریخ تغییرات', null=False,
                                        help_text='تاریخ تغییرات به شمسی.')
    changing_time = models.CharField(max_length=5, 
                                        verbose_name='ساعت تغییرات', null=False,
                                        help_text=' ساعت تغییرات به فرمت HH:MM.')
    changing_date_actual = models.CharField(max_length=10,
                                                verbose_name='تاریخ و ساعت واقعی تغییرات',
                                                null=True, help_text='تاریخ واقعی تغییرات به شمسی.')
    changing_time_actual = models.CharField(max_length=5,
                                                verbose_name='تاریخ و ساعت واقعی تغییرات',
                                                null=True, help_text=' ساعت واقعی تغییرات در قالب HH:MM.')
    changing_duration = models.PositiveIntegerField(verbose_name='مدت زمان تغییرات', 
                                            null=True, blank=True, help_text='مدت زمان تغییرات به دقیقه.')
    changing_duration_actual = models.PositiveIntegerField(verbose_name='مدت زمان واقعی تغییرات',
                                                    null=True, blank=True, help_text='مدت زمان واقعی تغییرات به دقیقه.')
    downtime_duration = models.PositiveIntegerField(verbose_name='مدت زمان توقف', 
                                            null=True, blank=True, help_text='مدت زمان توقف به دقیقه.')
    downtime_duration_worstcase = models.PositiveIntegerField(verbose_name='بدترین مدت زمان توقف', 
                                            null=True, blank=True, help_text='بدترین مدت زمان توقف به دقیقه.')
    downtime_duration_actual = models.PositiveIntegerField(verbose_name='مدت زمان توقف واقعی', 
                                                    null=True, blank=True, help_text='مدت زمان توقف واقعی به دقیقه.')
    
    # حوزه اثرگذاری تغییر
    stop_critical_service = models.BooleanField(default=False, verbose_name='توقف خدمات بحرانی',
                                                help_text='آیا خدمات بحرانی متوقف می‌شود؟')
    critical_service_title = models.CharField(max_length=200, verbose_name='عنوان خدمات بحرانی', 
                                            null=True, blank=True, help_text='عنوان خدمات بحرانی را وارد کنید.')
    stop_sensitive_service = models.BooleanField(default=False, verbose_name='توقف خدمات حساس', 
                                                help_text='آیا خدمات حساس متوقف می‌شود؟')
    stop_service_title = models.CharField(max_length=200, verbose_name='عنوان خدمات متوقف شده', 
                                        null=True, blank=True, help_text='عنوان خدمات متوقف شده را وارد کنید.')
    not_stop_any_service = models.BooleanField(default=False, verbose_name='عدم توقف هیچ خدماتی', 
                                            help_text='آیا هیچ خدماتی متوقف نمی‌شود؟')
    
    # طرح بازگشت
    has_role_back_plan = models.BooleanField(default=False, verbose_name='برنامه بازگشت وجود دارد', 
                                            help_text='آیا برنامه بازگشت وجود دارد؟')
    role_back_plan_description = models.CharField(max_length=1000, verbose_name='توضیحات برنامه بازگشت',
                                                null=True, blank=True, help_text='توضیحات مربوط به برنامه بازگشت را وارد کنید.')
    
    # الزام تغییرات
    reason_regulatory = models.BooleanField(default=False, verbose_name='الزام قانونی', 
                                            help_text='آیا الزام قانونی وجود دارد؟')
    reason_technical = models.BooleanField(default=False, verbose_name='الزام فنی', 
                                        help_text='آیا الزام فنی وجود دارد؟')
    reason_security = models.BooleanField(default=False, verbose_name='الزام امنیتی', 
                                        help_text='آیا الزام امنیتی وجود دارد؟')
    reason_business = models.BooleanField(default=False, verbose_name='الزام کسب و کاری', 
                                        help_text='آیا الزام کسب و کاری وجود دارد؟')
    reason_other = models.BooleanField(default=False, verbose_name='سایر الزامات', 
                                    help_text='آیا الزامات دیگری وجود دارد؟')
    reason_other_description = models.CharField(max_length=500, verbose_name='توضیحات الزامات دیگر', 
                                                null=True, blank=True, 
                                                help_text='توضیحات مربوط به الزامات دیگر را وارد کنید.',)
    
    # افراد درگیر
    requestor_nationalcode = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='درخواست کننده',
                                            null=False, db_column='requestor_nationalcode',
                                            related_name='requestor')
    requestor_role_id = models.ForeignKey(to=Role, db_column='requestor_role_id' ,verbose_name='سمت درخواست‌دهنده', null=True, related_name='requestor_role_id',
                                            help_text='لطفاً سمت فرد درخواست‌دهنده را وارد کنید.', on_delete=models.SET_NULL)
    requestor_team_code = models.ForeignKey('Team', on_delete=models.SET_NULL, verbose_name='تیم درخواست‌دهنده', 
                                            null=True, blank=True, help_text='تیم مربوط به درخواست‌دهنده را انتخاب کنید.',
                                            db_column='requestor_team_code')
    
    manager_nationalcode = models.ForeignKey(User, on_delete=models.CASCADE, 
                                            db_column='manager_nationalcode',
                                            verbose_name='کد ملی مدیر', 
                                            related_name='manager',
                                            null=False)
    manager_opinion = models.BooleanField(null=True, 
                                        help_text='در صورت موافقت مدیر مقدار 1 و در غیر این صورت مقدار صفر دارد')
    manager_opinion_date = models.CharField(null=True, max_length=10, verbose_name='تاریخ اعلام نظر مدیر',
                                                help_text='تاریخ اظهار نظر مدیر به شمسی.')
    manager_opinion_time = models.CharField(null=True, max_length=5, verbose_name='ساعت اعلام نظر مدیر',
                                                help_text=' ساعت اظهار نظر مدیر در قالب HH:MM.')
    manager_reject_description = models.CharField(max_length=500, verbose_name='توضیحات رد مدیر', 
                                                null=True, blank=True, 
                                                help_text='توضیحات مربوط به رد مدیر را وارد کنید.')

    need_committee = models.BooleanField(default=False, verbose_name='نیاز به کمیته', 
                                        help_text='آیا نیاز به کمیته وجود دارد؟')
    committee = models.ForeignKey(to='Committee', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='کمیته' )
    committee_user_nationalcode = models.ForeignKey(User, on_delete=models.CASCADE, 
                                                    db_column='committee_user_nationalcode',
                                                    verbose_name='کد ملی کاربر کمیته', 
                                                    related_name='committee',
                                                    null=True, blank=True)
    committee_opinion_date = models.CharField(null=True, max_length=10, verbose_name='تاریخ اعلام نظر کمیته',
                                            help_text='تاریخ اظهار نظر کمیته به شمسی.')
    committee_opinion_time = models.CharField(null=True, max_length=5, verbose_name='ساعت اعلام نظر کمیته',
                                            help_text='ساعت اظهار نظر کمیته در قالب HH:MM.')
    committee_opinion = models.BooleanField(null=True, help_text='در صورتی که نظر کمیته مثبت است مقدار 1 و در غیر این صورت مقدار صفر خواهد داشت')
    committee_reject_description = models.CharField(max_length=500, verbose_name='توضیحات رد کمیته', 
                                                    null=True, blank=True, help_text='توضیحات مربوط به رد کمیته را وارد کنید.',
                                                    )
    executor_nationalcode = models.ForeignKey(User, on_delete=models.CASCADE, 
                                            db_column='executor_nationalcode',
                                            related_name='executor',
                                            verbose_name='کد ملی مجری', null=False)
    executor_role_id = models.ForeignKey(to=Role, db_column='executor_role_id', verbose_name='سمت مجری', null=True, related_name='executor_role_id',
                                            help_text='لطفاً سمت فرد مجری را وارد کنید.', on_delete=models.SET_NULL)
    executor_team_code = models.ForeignKey('Team', on_delete=models.SET_NULL, verbose_name='تیم مجری', 
                                            null=True, blank=True, help_text='تیم مربوط به مجری را انتخاب کنید.',
                                            db_column='executor_team_code', related_name='executor_team_code')

    executor_report_date = models.CharField(null=True, max_length=10, verbose_name='تاریخ گزارش مجری',
                                                help_text='تاریخ گزارش مجری به شمسی.')
    executor_report_time = models.CharField(null=True, max_length=5, verbose_name='ساعت گزارش مجری',
                                            help_text='ساعت گزارش مجری به شمسی در قالب HH:MM.')
    executor_report = models.BooleanField(null=True, help_text='در صورتی که اجرا موفقیت آمیز باشد مقدار 1 و در غیر این صورت مقدار صفر خواهد داشت')
    execution_description = models.CharField(max_length=1000, verbose_name='گزارش انجام', 
                                            null=True, blank=True, help_text='گزارش انجام را وارد کنید.')

    test_required = models.BooleanField(verbose_name='نیازمند تست است؟', default=0,
                                    help_text='در صورتی که نیاز به تست داشته باشد مقدار یک و در غیر این صورت مقدار صفر خواهد داشت')
    tester_nationalcode = models.ForeignKey(User, on_delete=models.CASCADE, 
                                            db_column='tester_nationalcode',
                                            related_name='tester',
                                            verbose_name='کد ملی تستر', null=False)
    tester_role_id = models.ForeignKey(to=Role, db_column='tester_role_id', verbose_name='سمت تستر', null=True,related_name='tester_role_id',
                                            help_text='لطفاً سمت فرد تستر را وارد کنید.', on_delete=models.SET_NULL)
    tester_team_code = models.ForeignKey('Team', on_delete=models.SET_NULL, verbose_name='تیم تستر', 
                                            null=True, blank=True, help_text='تیم مربوط به تستر را انتخاب کنید.',
                                            db_column='tester_team_code', related_name='tester_team_code')    
    tester_report = models.BooleanField(null=True, help_text='در صورتی که تست موفقیت آمیز باشد مقدار 1 و در غیر این صورت مقدار صفر خواهد داشت')
    tester_report_date = models.CharField(null=True, max_length=10, verbose_name='تاریخ گزارش تستر',
                                                help_text='تاریخ گزارش تستر به شمسی.')
    tester_report_time = models.CharField(null=True, max_length=5, verbose_name='ساعت گزارش تستر',
                                            help_text='ساعت گزارش تستر به شمسی در قالب HH:MM.')
    test_date = models.CharField(null=True, max_length=10, verbose_name='تاریخ انجام تست',
                                                help_text='تاریخ انجام تست به شمسی.')
    test_time = models.CharField(null=True, max_length=5, verbose_name='ساعت انجام تست',
                                            help_text='ساعت انجام تست به شمسی در قالب HH:MM.')
    test_report_description = models.CharField(max_length=1000, verbose_name='توضیحات تست', null=True, blank=True, help_text='توضیحات تست را وارد کنید.')
    

    def get_state_display(self):
        """برگشت مقدار متنی متناظر با کد وضعیت."""
        for code, display in self.STATE_CHOICES:
            if code == self.state_code:
                return display
        return None  # در صورتی که کد وضعیت نامعتبر باشد

    class Meta:
        verbose_name = 'درخواست تغییر'
        verbose_name_plural = 'درخواست‌های تغییر'
        managed = True

    def __str__(self):
        return f"درخواست {self.change_title}"

    def clean(self):
        # # اعتبارسنجی تاریخ تست
        # if self.test_date and self.changing_date_actual:
        #     v.validate_test_date(self.test_date, self.changing_date_actual)

        # # اعتبارسنجی تاریخ گزارش تست
        # if self.tester_report_date and self.test_date:
        #     v.validate_tester_report_date(self.tester_report_date, self.test_date)

        # اعتبارسنجی فیلدهای کمیته
        v.validate_committee_fields(
            self.need_committee,
            self.committee_user_nationalcode,
            self.committee_opinion_date,
            self.committee_opinion,
            self.committee_reject_description
        )

        # اعتبارسنجی نظر مدیر
        v.validate_manager_opinion(self.manager_opinion, self.manager_reject_description)
        
        # اعتبارسنجی سایر الزامات
        v.validate_reason_other(self.reason_other, self.reason_other_description)

        # اعتبارسنجی توقف خدمات بحرانی
        v.validate_critical_service(self.stop_critical_service, self.critical_service_title)

        # اعتبارسنجی توقف خدمات حساس
        v.validate_sensitive_service(self.stop_sensitive_service, self.stop_service_title)

        # اعتبارسنجی محل تغییر: سایر
        v.validate_change_location_other(self.change_location_other, self.change_location_other_description)

        v.ConstValue_Validator(value=self.change_level, prefix="change_level")
        v.ConstValue_Validator(value=self.classification, prefix="classification")
        v.ConstValue_Validator(value=self.priority, prefix="priority")
        v.ConstValue_Validator(value=self.risk_level, prefix="risk_level")
        v.ConstValue_Validator(value=self.change_domain, prefix="change_domain")

        # اعتبارسنجی کد ملی درخواست کننده
        if not self.requestor_nationalcode:
            raise ValidationError("کد ملی درخواست کننده الزامی است.")

        # اعتبارسنجی عنوان تغییر
        if not self.change_title:
            raise ValidationError("عنوان تغییر الزامی است.")

        # اعتبارسنجی توضیحات تغییر
        if not self.change_description:
            raise ValidationError("توضیحات تغییر الزامی است.")

class RequestCorp_ChangeType(models.Model):
    changetype = models.ForeignKey(ChangeType, on_delete=models.CASCADE, 
                                        verbose_name='کد نوع تغییر', null=False)
    corp_code = models.ForeignKey(Corp, on_delete=models.CASCADE, verbose_name='شرکت', null=False, db_column='corp_code')

    class Meta:
        verbose_name = 'شرکت در نوع درخواست'
        verbose_name_plural = 'شرکت‌ها در نوع  درخواست ها'
        managed = True

    def __str__(self):
        return f"{self.corp_code} در {self.request}"

class RequestTeam_ChangeType(models.Model):
    changetype= models.ForeignKey(ChangeType, on_delete=models.CASCADE, 
                                        verbose_name='کد نوع تغییر', null=False)
    team_code = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='تیم', null=False, db_column='team_code')

    class Meta:
        verbose_name = 'تیم بر اساس نوع درخواست'
        verbose_name_plural = 'تیم‌ها بر اساس نوع درخواست ها'
        managed = True

    def __str__(self):
        return f"{self.team_code} در {self.request}"

class RequestExtraInformation_ChangeType(models.Model):
    extra_info = models.ForeignKey(to='ConstValue', on_delete=models.CASCADE, null=False, verbose_name='شناسه اطلاعات تکمیلی')
    change_type = models.ForeignKey(to='ChangeType', on_delete=models.CASCADE, null=False, verbose_name='شناسه نوع درخواست')
    class Meta:
        verbose_name = 'اطلاعات تکمیلی درخواست'
        verbose_name_plural = 'اطلاعات تکمیلی درخواست‌ها'

    def __str__(self) -> str:
        return f'{self.change_type.change_type_title} - {self.extra_info.Caption}'

class RequestCorp(models.Model):
    request = models.ForeignKey(ConfigurationChangeRequest, on_delete=models.CASCADE, verbose_name='درخواست', null=False)
    corp_code = models.ForeignKey(Corp, on_delete=models.CASCADE, verbose_name='شرکت', null=False, db_column='corp_code')

    class Meta:
        verbose_name = 'شرکت در درخواست'
        verbose_name_plural = 'شرکت‌ها در درخواست‌ها'
        managed = True

    def __str__(self):
        return f"{self.corp_code} در {self.request}"

class RequestTeam(models.Model):
    request = models.ForeignKey(ConfigurationChangeRequest, on_delete=models.CASCADE, verbose_name='درخواست', null=False)
    team_code = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='تیم', null=False, db_column='team_code')

    class Meta:
        verbose_name = 'تیم در درخواست'
        verbose_name_plural = 'تیم‌ها در درخواست‌ها'
        managed = True

    def __str__(self):
        return f"{self.team_code} در {self.request}"


class RequestExtraInformation(models.Model):
    extra_info = models.ForeignKey(to=ConstValue, on_delete=models.CASCADE, null=False, verbose_name='شناسه اطلاعات تکمیلی')
    request = models.ForeignKey(to='ConfigurationChangeRequest', on_delete=models.CASCADE, null=False, verbose_name='شناسه درخواست')
    class Meta:
        verbose_name = 'اطلاعات تکمیلی درخواست'
        verbose_name_plural = 'اطلاعات تکمیلی درخواست‌ها'


    def __str__(self) -> str:
        return f'{self.request.change_title} - {self.extra_info.Caption}'        