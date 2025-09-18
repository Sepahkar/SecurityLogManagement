from turtle import mode
from django.db import models
import jdatetime
from django.core.validators import MinValueValidator
from ConfigurationChangeRequest.validator import Validator as v, DefaultValue as d
from django.core.exceptions import ValidationError
from django.utils import timezone

class BaseModel(models.Model):
    """
    این مدل 4 فیلد مربوط به ایجاد و تغییرات را به جدول مربوطه اضافه می کند
    هر کلاسی که از این کلاس ارث ببرد به صورت خودکار فیلدهای تاریخ ایجاد، تاریخ تغییر، کاربر ایجاد کننده و آخرین کاربر تغییر دهنده را دریافت می کند
    تاریخ ایجاد و تاریخ تغییر به صورت خودکار مقداردهی می گردد
    ولی کاربر ایجاد کننده و کاربر تغییر دهنده باید توسط کدی که برنامه نویس می نویسد مدیریت شوند
    """
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد',)
    modify_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین تغییر')
    creator_user = models.ForeignKey(
        'User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='created_%(class)ss', verbose_name='کاربر ایجادکننده')
    last_modifier_user = models.ForeignKey(
        'User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='modified_%(class)ss', 
        # %(class)s در Django هنگام تعریف مدل‌های انتزاعی (abstract) استفاده می‌شود تا نام مدل فرزند را به طور خودکار جایگزین کند. این باعث می‌شود هر مدل فرزند یک related_name یکتا داشته باشد، مثلاً برای مدل ConfigurationChangeRequest مقدار آن modified_configurationchangerequests خواهد شد.
        verbose_name='آخرین کاربر ویرایشگر')

    def save(self, *args, **kwargs):
        # اطمینان از استفاده از timezone-aware datetime
        if not self.pk:  # اگر رکورد جدید است
            self.create_date = timezone.now()
        self.modify_date = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True

class User(models.Model):
    """
    این جدول دربردارنده اطلاعات کلیه کاربران سازمان است
    اطلاعات این جدول به صورت خودکار از سیستم منابع انسانی تکمیل می شود 
    نیازی به اینکه کاربر بتواند رکوردهای این جدول را تغییر دهد وجود ندارد
    """
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
    """
    در این جدول سمت های جاری کلیه کاربران قرار دارد
    اطلاعات این جدول از سیستم منابع انسانی به صورت خودکار تغییر می گردد و نیازی نیست که کاربر چیزی را تغییر دهد
    از اطلاعات این جدول برای پیدا کردن مدیر مستقیم فرد درخواست دهنده استفاده می کنیم

    """
    national_code = models.ForeignKey(to='user', db_column='national_code', verbose_name='کد ملی کاربر', related_name='user', on_delete=models.CASCADE)    
    role_id = models.IntegerField(verbose_name="شناسه سمت")
    team_code = models.ForeignKey('Team', on_delete=models.SET_NULL, verbose_name='تیم کاربر', null=True, blank=True, help_text='تیم مربوط به کاربر را انتخاب کنید.', db_column='team_code')
    manager_national_code = models.ForeignKey(to='user', db_column='manager_national_code', null=True, 
                                              verbose_name='کد ملی مدیر مستقیم', related_name='direct_manager',on_delete=models.SET_NULL)    

    class Meta:
        verbose_name = 'سمت کاربر'
        verbose_name_plural = 'سمت های کاربران'

    def __str__(self) -> str:
        return f"{self.role_title} {self.team_code.team_name}"

class ConstValue(models.Model):
    """
        کلیه اطلاعات مربوط به مقادیر ثابت پروژه در این جدول ذخیره می شود
        این اطلاعات شامل مواردی می شوند که کومبوها و یا دکمه های رادیویی را نشان می دهند
        مثلا اولویت تغییر (استاندارد، فوری، اضطراری)
        نحوه ذخیره سازی به این صورت است که یک رکورد مادر داریم (مثلا با عنوان «اولویت تغییر» که دارای یک کد Priority است.)
        رکوردهای فرزند (مثلا استاندارد، فوری، اضطراری) در ذیل این رکورد ثبت می شوند و مقدار فیلد parent_id
        آنها برابر با فیلد id رکورد مادر است
        همچنین کد آنها هم ترکیبی از کد مادر و فرزند است. مثلا:
        Priority_Standard: اولویت استاندارد
        Priority_Urgent: اولویت فوری
        Priority_Emergency: اولویت اضطراری
        یک مقدار ثابت را نمی توان پاک کرد، ولی می توان غیر فعال کرد
        همچنین می توان ترتیب نمایش انها را با استفاده از فیلد
        OrderNumber
        تغییر داد
    """
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
    """
    لیست شرکت ها در این جدول ذخیره می شود. 
    این اطلاعات از سیستم EIT
    به صورت خودکار تکمیل می شود و نیازی نیست که کاربر رکوردی را ویرایش کند
    """
    corp_code = models.CharField(max_length=3, primary_key=True, verbose_name='کد شرکت', null=False, help_text='کد منحصر به فرد شرکت را وارد کنید.')
    corp_name = models.CharField(max_length=100, verbose_name='نام شرکت', null=False, help_text='نام شرکت را وارد کنید.')

    class Meta:
        verbose_name = 'شرکت'
        verbose_name_plural = 'شرکت‌ها'
        managed = True

    def __str__(self):
        
        return self.corp_name

class Team(models.Model):
    """
    اطلاعات کلیه تیم ها در این جدول ذخیره می شود
    این جدول به صورت خودکار از HR مقدار می گیرد
    این امکان وجود دارد که یک تیم فعال یا غیر فعال شود

    """
    team_code = models.CharField(max_length=3, primary_key=True, verbose_name='کد تیم', null=False, help_text='کد منحصر به فرد تیم را وارد کنید.')
    team_name = models.CharField(max_length=100, verbose_name='نام تیم', null=False, help_text='نام تیم را وارد کنید.')
    is_active = models.BooleanField(default=True, verbose_name='فعال است')
    class Meta:
        verbose_name = 'تیم'
        verbose_name_plural = 'تیم‌ها'
        managed = True

    def __str__(self):
        return self.team_name

class Role(models.Model):
    """
    این جدول حاوی اطلاعات سمت های سازمانی است
    این اطلاعات از جدول سمت ها در سیستم منابع انسانی به صورت خودکار تکمیل می شود
    نیازی به تغییر اطلاعات این جدول نیست
    """
    role_id = models.IntegerField(primary_key=True, verbose_name='شناسه سمت')
    role_title = models.CharField(max_length=150, verbose_name='عنوان سمت')

    class Meta:
        verbose_name = 'سمت'
        verbose_name_plural = 'سمت‌ها'
        managed = True

    def __str__(self):
        return self.role_title

class Committee(models.Model):
    """
    اطلاعات کمیته ها در این جدول ذخیره می شود
    ممکن است نیاز باشد کمیته جدیدی اضافه شود و یا دبیر یک کمیته تغییر کند
    نباید امکان حذف کمیته وجود داشته باشد، فقط می شود کمیته ای که وجود دارد را غیر فعال کرد
    فعلا سابقه ای برای تغییرات دبیر کمیته وجود ندارد
    ولی در صورت نیاز باید سوابق تغییرات دبیرکمیته در یک جدول دیگر ذخیره شود
    """
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
        return self.title    

class ChangeType(models.Model):
    """ 
    در این جدول به ازای هر نوع درخواست، اطلاعات پیش فرض مربوطه ذخیره می شود
    این جدول در حقیقت الگوهای درخواست را مشخص می کند
    وقتی کاربر یک الگو را انتخاب می کند، به صورت پیش فرض اطلاعات فیلدهای درخواست بر اساس آن تکمیل می گردد
    البته کاربر مدیر مربوطه می تواند حسب نیاز این اطلاعات را ویرایش نماید
    در حال حاضر هیچ جدولی برای ذخیره سوابق تغییرات این الگوها نداریم.
    یعنی اگر کسی یک الگو را تغییر دهد، معلوم نمی شود که چه موقعی چه مقداری توسط چه کسی ویرایش شده است
    جداول وابسته زیادی (مانند جدول تسک ها، شرکت های مرتبط و ...) به این جدول وجود دارند
    """
    code = models.CharField(max_length=6, verbose_name='کد نوع تغییر', db_column='code',
                            null=True, help_text='لطفاً کد نوع تغییر را وارد کنید.')
    change_type_title = models.CharField(max_length=255, verbose_name='عنوان نوع تغییر', null=True)
    change_title = models.CharField(max_length=255, verbose_name='عنوان تغییر', null=True, 
                                    help_text='لطفاً عنوان تغییر را وارد کنید.')
    change_description = models.TextField(max_length=1000, verbose_name='توضیحات تغییر', 
                                        null=True, blank=True, help_text='توضیحات مربوط به تغییر را وارد کنید.')

    related_manager = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, 
                                        verbose_name = "مدیر مربوطه",
                                        help_text="مدیر مربوطه را انتخاب کنید")
    
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

    need_committee = models.BooleanField(default=False, 
                                        verbose_name='نیاز به کمیته',
                                        null=True,
                                        help_text='آیا نیاز به کمیته وجود دارد؟')
    committee = models.ForeignKey(to=Committee, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='کمیته' )

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
        return self.code
    
    def clean(self) -> None:
        v.ConstValue_Validator(prefix="change_level")
        v.ConstValue_Validator(prefix="classification")
        v.ConstValue_Validator(prefix="priority")
        v.ConstValue_Validator(prefix="risk_level")
        v.ConstValue_Validator(prefix="change_domain")
        return super().clean()

class NotifyGroup(models.Model):
    """ 
    این جدول شامل اطلاعات گروه های اطلاع رسانی است
    یک گروه اطلاع رسانی می تواند شامل یک سمت خاص باشد، مثلا برنامه نویسان
    یا یک تیم خاص باشد، مثلا تیم خودرو
    یا هر دو مثلا تحلیل گران تیم درمان
    در زمانی که قرار است اطلاع رسانی انجام شود، در صورتی که این گروه انتخاب شده باشد
    اطلاع رسانی به کلیه اعضای آن گروه (کلیه برنامه نویسان، یا کلیه اعضای تیم خودرو، یا تمامی تحلیل گران تیم درمان) انجام می شود
    همچنین می شود یک گروه تعریف کنیم که سمت و تیم خاصی را شامل نشود، مثلا گروه آدم های مهم!
    بعدش در جدول
    NotifyGroupUser
    مشخص می کنیم که منظورمان چه افرادی است
    """
    
    code = models.CharField(verbose_name='کد گروه', max_length=10)
    title = models.CharField(verbose_name='عنوان گروه', max_length=30)
    role_id = models.ForeignKey(to=Role, verbose_name='شناسه سمت', on_delete=models.SET_NULL,
                                null=True, related_name='notify_role_id',
                                help_text='در صورتی این گروه مربوط به یک سمت خاص است')
    team_code = models.ForeignKey(to=Team, verbose_name='کد سمت', on_delete=models.SET_NULL,
                                null=True, related_name='notify_team_code',
                                help_text='در صورتی این گروه مربوط به یک تیم است')

    class Meta:
        verbose_name = 'گروه اطلاع رسانی'
        verbose_name_plural = 'گروه های اطلاع رسانی'
        managed = True

    def __str__(self):
        return self.title

class NotifyGroupUser(models.Model):
    """
    در صورتی که بخواهیم یک گروه تعریف کنیم که شامل افراد خاصی باشد
    اطلاعات آنها را در این جدول ذخیره می کنیم
    توجه کنید که سمت و تیم هر فرد را هم باید اینجا ذخیره کنیم
    """
    notify_group_code = models.ForeignKey(to=NotifyGroup, verbose_name='کد گروه اطلاع رسانی', on_delete=models.CASCADE)
    user_nationalcode = models.ForeignKey(to=User, verbose_name='کاربر مربوطه',
                                          db_column='user_nationalcode', on_delete=models.CASCADE)
    user_role_id = models.ForeignKey(to=Role, db_column='user_role_id' ,verbose_name='سمت کاربر', 
                                    null=True,
                                    help_text='لطفاً سمت فرد کاربر را وارد کنید.', 
                                    on_delete=models.SET_NULL)
    user_team_code = models.ForeignKey(to=Team, on_delete=models.SET_NULL, 
                                       verbose_name='تیم کاربر', 
                                        null=True, blank=True, 
                                        help_text='تیم مربوط به کاربر را انتخاب کنید.',
                                        db_column='user_team_code')

    class Meta:
        verbose_name = 'افراد اطلاع رسانی'
        verbose_name_plural = 'افراد اطلاع رسانی'
        managed = True

    def __str__(self):
        return self.user_nationalcode    




class ConfigurationChangeRequest(BaseModel):
    """
    این جدول اصلی ترین جدول سیستم است
    کلیه درخواست های تغییرات در این جدول ذخیره می شوند
    جدوال وابسته هم به این جدول رابطه دارند
    وقتی کاربر درخواست دهنده نوع تغییر را وارد می کند، اطلاعات از جدول
    change_type
    در این جدول کپی می شوند
    در حال حاضر جدولی برای ذخیره سوابق تغییرات نداریم 
    """
    
    doc_id = models.IntegerField(verbose_name='کد سند', null=True, 
                                help_text='لطفاً کد سند را وارد کنید.')
    STATUS_CHOICES = [
        ('DRAFTD', 'پیش نویس'),
        ('DIRMAN', 'اظهار نظر مدیر مستقیم'),
        ('RELMAN', 'اظهار نظر مدیر مستقیم'),
        ('COMITE', 'اظهار نظر کمیته'),
        ('DOTASK', 'انجام تسک ها'),
        ('FINISH', 'خاتمه یافته'),
        ('FAILED', 'خاتمه ناموفقیت آمیز'),
        ('ERRORF', 'خاتمه با خطا'),
        
    ]

    status_code = models.CharField(
        max_length=6, choices=STATUS_CHOICES,
        verbose_name='کد وضعیت',
        default='DRAFTD',
        help_text='لطفاً کد وضعیت را وارد کنید.'
    )
    
    # اطلاعات تغییر
    change_type = models.ForeignKey(ChangeType, on_delete=models.CASCADE, verbose_name='کد نوع تغییر',
                                        null=False)
    change_title = models.CharField(max_length=255, verbose_name='عنوان تغییر', null=False, 
                                    help_text='لطفاً عنوان تغییر را وارد کنید.')
    change_description = models.TextField(max_length=1000, verbose_name='توضیحات تغییر', 
                                        null=True, blank=True, help_text='توضیحات مربوط به تغییر را وارد کنید.')
 
    # اطلاعات افراد درگیر
    requestor_nationalcode = models.ForeignKey(User, on_delete=models.CASCADE, 
                                                verbose_name='کد ملی درخواست کننده',
                                                null=False, db_column='requestor_nationalcode',
                                                related_name='requestor_nationalcode')
    requestor_team_code = models.ForeignKey(Team, on_delete=models.CASCADE, 
                                                verbose_name='تیم درخواست کننده',
                                                null=False, db_column='requestor_team_code',
                                                related_name='requestor_team_code')
    requestor_role_id = models.ForeignKey(Role, on_delete=models.CASCADE, 
                                                verbose_name='سمت درخواست کننده',
                                                null=False, db_column='requestor_role_id',
                                                related_name='requestor_role_id')
    direct_manager_nationalcode = models.ForeignKey(User, on_delete=models.CASCADE, 
                                            db_column='direct_manager_nationalcode',
                                            verbose_name='کد ملی مدیر', 
                                            related_name='direct_manager_nationalcode',
                                            null=False)
    related_manager_nationalcode = models.ForeignKey(User, on_delete=models.CASCADE, 
                                            db_column='related_manager_nationalcode',
                                            verbose_name='کد ملی مدیر مربوطه', 
                                            related_name='related_manager_natioanlcode',
                                            null=False)
    committee_user_nationalcode = models.ForeignKey(User, on_delete=models.CASCADE, 
                                                    db_column='committee_user_nationalcode',
                                                    verbose_name='کد ملی کاربر کمیته', 
                                                    related_name='committee_user_nationalcode',
                                                    null=True, blank=True)    
    
    # کمیته
    need_committee = models.BooleanField(default=False, verbose_name='نیاز به کمیته', 
                                        help_text='آیا نیاز به کمیته وجود دارد؟')    
    committee = models.ForeignKey(to=Committee, on_delete=models.SET_NULL, null=True, 
                                  blank=True, verbose_name='کمیته' )
    
    # این فیلدها توسط مدیر مربوطه تکمیل می شود
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

class Task(models.Model):
    """ 
    در این جدول اطلاعات تسک هایی که در راستای تغییرات مختلف باید انجام شوند وجود دارد
    توجه کنید که ممکن است ترکیبی از این تسک ها در یک درخواست انجام شوند که در جداول بعدی مشخص می شود
    """
    title = models.CharField(max_length=50, verbose_name='عنوان فعالیت')
    test_required = models.BooleanField(verbose_name='نیازمند تست است؟', default=0,
                                    help_text='در صورتی که نیاز به تست داشته باشد مقدار یک و در غیر این صورت مقدار صفر خواهد داشت')
    order_number = models.PositiveSmallIntegerField(verbose_name='شماره ترتیب', default = 1)
    
    class Meta:
        verbose_name = 'تسک'
        verbose_name_plural = 'تسک ها'
        managed = True  
    
    def __str__(self) -> str:
        return self.title
        
class TaskUser(models.Model):
    """
    در این جدول افراد مرتبط با تسک (تستر یا مجری) مشخص می شود
    این افراد کسانی هستند که می توانند تسک را انجام داده و یا تست کنند
    تیم و سمت کاربر را هم ذخیره می کنیم
    اینکه کاربر نقش تستر و یا مجری دارد در فیلد
    user_role_code
    مشخص می شود
    توجه کنید که این افراد، کاندید هستند، یعنی ممکن است برای یک تسک 5 مجری تعریف شود
    ولی در نهایت به ازای هر درخواست، فقط یکی از این افراد، مجری آن تسک در آن درخواست خواهد بود     
    """
    task = models.ForeignKey(to=Task, verbose_name='شناسه تسک', on_delete=models.CASCADE)
    user_nationalcode = models.ForeignKey(to=User, verbose_name='کاربر مربوطه',
                                          db_column='user_nationalcode', on_delete=models.CASCADE)
    user_role_id = models.ForeignKey(to=Role, db_column='user_role_id' ,verbose_name='سمت کاربر', 
                                    null=True, related_name='user_role_id',
                                    help_text='لطفاً سمت فرد کاربر را وارد کنید.', 
                                    on_delete=models.SET_NULL)
    user_team_code = models.ForeignKey(to=Team, on_delete=models.SET_NULL, verbose_name='تیم کاربر', 
                                        null=True, blank=True, 
                                        help_text='تیم مربوط به کاربر را انتخاب کنید.',
                                        db_column='user_team_code')
    ROLE_CHOICES = [
        ('E', 'مجری'),
        ('T', 'تستر'),
    ]    
    user_role_code = models.CharField(max_length=1,choices=ROLE_CHOICES, verbose_name='سمت کاربر در تسک' )
    
    class Meta:
        verbose_name = 'کاربر تسک'
        verbose_name_plural = 'کاربران تسک ها'
        managed = True  
    
    def __str__(self) -> str:
        return self.task      


class RequestTask(models.Model):
    """ 
    در این جدول تسک های مربوط به یک درخواست درج می شود
    به صورت پیش فرض این تسک ها بر اساس نوع درخواست تعیین  می شوند
    ولی مدیر مربوطه می تواند آنها را کم و یا زیاد کند
    """
    request = models.ForeignKey(to=ConfigurationChangeRequest, 
                                verbose_name='شناسه درخواست', 
                                on_delete=models.CASCADE)
    task = models.ForeignKey(to=Task, verbose_name='شناسه تسک', 
                            on_delete=models.CASCADE)

    STATUS_CHOICES = [
        ('DEFINE', 'تعریف'),
        ('EXERED', 'آماده انتخاب مجری'),
        ('EXESEL', 'مجری انتخاب شده'),
        ('TESRED', 'آماده انتخاب تستر'),
        ('TESSEL', 'تستر انتخاب شده'),
        ('FINISH', 'انجام موفق'),
        ('FAILED', 'انجام ناموفق'),
        
        
    ]
    status_code = models.CharField(max_length=6, verbose_name='وضعیت تسک' , choices=STATUS_CHOICES)
    
    class Meta:
        verbose_name = 'تسک درخواست'
        verbose_name_plural = 'تسک های درخواست ها'
        managed = True  
    
    def __str__(self) -> str:
        return f'{self.request} - {self.task}'


class TaskUserSelected(models.Model):
    """ 
    زمانی که یک فرد یک تسک را جهت انجام عملیات مربوطه (اجرای تسک یا تست تسک) انتخاب می کند
    یک رکورد در این جدول درج می شود
    همچنین فرد مربوطه باید گزارش، تاریخ انجام تسک و ... را هم وارد کند که در این جدول ذخیره می شود
    در حال حاضر جدولی نداریم که سوابق تغییرات این جدول در آن ذخیره شود
    یعنی اگر تستر فرم را به مجری برگرداند و مجری دوباره تسک را انجام دهد
    فقط تاریخ آخر را خواهیم داشت
    """
    task_user = models.ForeignKey(to=TaskUser, verbose_name='شناسه کاربر تسک', on_delete=models.CASCADE)
    request_task = models.ForeignKey(to=RequestTask, verbose_name='شناسه کاربر تسک', on_delete=models.CASCADE)
    pickup_date = models.DateTimeField(verbose_name='تاریخ و ساعت انتخاب تسک', auto_now_add=True,
                                       help_text='تاریخ و ساعتی که این تسک توسط کاربر انتخاب شده است')
    user_report_result = models.BooleanField(null=True, 
                                             help_text='در صورتی که تست موفقیت آمیز باشد مقدار 1 و در غیر این صورت مقدار صفر خواهد داشت')
    user_report_date = models.CharField(null=True, max_length=10, verbose_name='تاریخ گزارش تستر',
                                                help_text='تاریخ گزارش تستر به شمسی.')
    user_report_time = models.CharField(null=True, max_length=5, verbose_name='ساعت گزارش تستر',
                                        help_text='ساعت گزارش تستر به شمسی در قالب HH:MM.')
    user_done_date = models.CharField(null=True, max_length=10, verbose_name='تاریخ انجام تست',
                                help_text='تاریخ انجام تست به شمسی.')
    user_done_time = models.CharField(null=True, max_length=5, verbose_name='ساعت انجام تست',
                                help_text='ساعت انجام تست به شمسی در قالب HH:MM.')
    user_report_description = models.CharField(max_length=1000, verbose_name='توضیحات تست', null=True, blank=True, 
                                               help_text='توضیحات تست را وارد کنید.')
    
    
    class Meta:
        verbose_name = 'کاربر انجام دهنده تسک'
        verbose_name_plural = 'کاربران انجام دهنده تسک ها'
        managed = True  
    
    def __str__(self) -> str:
        return self.task_user      



class RequestTask_ChangeType(models.Model):
    """ 
    در این جدول به ازای هر نوع تغییر، تسک های مربوطه ذکر شده است
    وقتی کاربر یک نوع تغییر را انتخاب می کند، به صورت خودکار کلیه تسک های مربوطه در جدول تسک های آن درخواست ثبت خواهد شد
    """
    changetype= models.ForeignKey(to=ChangeType, on_delete=models.CASCADE, 
                                verbose_name='کد نوع تغییر', null=False)
    task = models.ForeignKey(to=Task, verbose_name='شناسه تسک', 
                            on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'تسک نوع درخواست'
        verbose_name_plural = 'تسک های نوع درخواست ها'
        managed = True  
    
    def __str__(self) -> str:
        return f'{self.request} - {self.task}'

class RequestTaskUser(models.Model):
    """ 
    هر تسک می تواند چند مجری یا تستر داشته باشد
    اما مدیر مربوطه می تواند تعدادی از آنها را در یک درخواست کم و زیاد کند
    مثلا یک تسک داریم که علی و حسن و حسین می توانند مجری آن باشند
    مدیر مربوطه برای یک درخواست خاص به دلیل اینکه حسن به مرخصی رفته است، اسم او را حذف کرده 
    و اسم لیلا و مینا را اضافه می کند
    در نتیجه برای این تسک در این درخواست خاص، مجریان می شوند علی، حسین، لیلا و مینا
    به صورت پیش فرض تمامی افراد مرتبط (مجریان و تسترها) در یک تسک برای یک درخواست ثبت می شوند
    مدیر مربوطه می تواند آنها را کم و یا زیاد کند
    """
    request_task = models.ForeignKey(to=RequestTask, 
                                verbose_name='شناسه تسک درخواست', 
                                on_delete=models.CASCADE)
    user_nationalcode = models.ForeignKey(to=User, verbose_name='کاربر مربوطه',
                                          db_column='user_nationalcode', on_delete=models.CASCADE)
    user_role_id = models.ForeignKey(to=Role, db_column='user_role_id' ,verbose_name='سمت کاربر', 
                                    null=True,
                                    help_text='لطفاً سمت فرد کاربر را وارد کنید.', 
                                    on_delete=models.SET_NULL)
    user_team_code = models.ForeignKey(to=Team, on_delete=models.SET_NULL, verbose_name='تیم کاربر', 
                                        null=True, blank=True, 
                                        help_text='تیم مربوط به کاربر را انتخاب کنید.',
                                        db_column='user_team_code')
    STATUS_CHOICES = [
        ('E', 'مجری'),
        ('T', 'تستر'),
    ]    
    user_role_code = models.CharField(max_length=1, verbose_name='سمت کاربر در تسک' )
    
    class Meta:
        verbose_name = 'کاربر تسک درخواست'
        verbose_name_plural = 'کاربران تسک های درخواست ها'
        managed = True  
    
    def __str__(self) -> str:
        return f'{self.request} - {self.task} '

class RequestFlow(models.Model):
    """ 
    در این جدول سوابق گردش مدرک ذخیره می شود
    یعنی مشخص می کند که مثلا مدیر مستقیم درخواست را تایید کرده است
    یا مدیر مربوطه آن را بازگشت داده است و ...
    نکته مهم این است که در حال حاضر این موضوع فقط مربوط به گردش درخواست است نه گردش تسک
    """
    request = models.ForeignKey(to=ConfigurationChangeRequest, verbose_name='شناسه درخواست', 
                                on_delete=models.CASCADE)
    user_nationalcode = models.ForeignKey(to=User, verbose_name='کاربر مربوطه',
                                          db_column='user_nationalcode', on_delete=models.CASCADE)
    user_role_id = models.ForeignKey(to=Role, db_column='user_role_id' ,verbose_name='سمت کاربر', 
                                    null=True, 
                                    help_text='لطفاً سمت فرد کاربر را وارد کنید.', 
                                    on_delete=models.SET_NULL)
    user_team_code = models.ForeignKey(to=Team, on_delete=models.SET_NULL, verbose_name='تیم کاربر', 
                                        null=True, blank=True, 
                                        help_text='تیم مربوط به کاربر را انتخاب کنید.',
                                        db_column='user_team_code')
    user_role_code = models.ForeignKey(to=ConstValue, on_delete=models.CASCADE, 
                                       related_name='user_role_code',
                                       verbose_name='کد سمت کاربر', 
                                        help_text='کد سمت کاربر',
                                        db_column='user_role_code') 
    user_opinion = models.ForeignKey(to=ConstValue, verbose_name='نظر کاربر', 
                                     related_name='user_opinion',
                                     on_delete=models.CASCADE)
    receiver_date = models.DateTimeField(auto_now_add=True, verbose_name='زمان دریافت')
    send_date = models.DateTimeField(null=True, verbose_name='زمان دریافت')
    fields_value = models.JSONField(null=True, verbose_name='مقادیر فیلدها', 
                                    help_text='مقادیر فیلدهای فرم در زمان خروج از کارتابل، به صورت json ذخیره می شود')
    user_send_date = models.CharField(null=True, max_length=10, verbose_name='تاریخ اعلام نظر کاربر',
                                                help_text='تاریخ اظهار نظر کاربر به شمسی.')
    user_send_time = models.CharField(null=True, max_length=5, verbose_name='ساعت اعلام نظر کاربر',
                                                help_text=' ساعت اظهار نظر کاربر در قالب HH:MM.')
    user_reject_description = models.CharField(max_length=500, verbose_name='توضیحات رد کاربر', 
                                                null=True, blank=True, 
                                                help_text='توضیحات مربوط به رد کاربر را وارد کنید.')
    class Meta:
        verbose_name = 'گردش درخواست'
        verbose_name_plural = 'گردش درخواست ها'
        managed = True

    def __str__(self):
        return f"{self.request} در {self.request}"
    
class RequestNotifyGroup(models.Model):
    """
    در این جدول مشخص می شود که گروه های اطلاع رسانی مربوط به یک درخواست چه موارد است
    در پایان فرآیند اطلاع رسانی به صورت خودکار به تمامی افراد هر یک از این گروه ها انجام می شود 
    """
    request = models.ForeignKey(to=ConfigurationChangeRequest, verbose_name='شناسه درخواست', 
                                on_delete=models.CASCADE)
    notify_group = models.ForeignKey(to=NotifyGroup, verbose_name='شناسه گروه اطلاع رسانی'
                                     ,db_column='notify_group_code', on_delete=models.CASCADE)
    by_email = models.BooleanField(verbose_name='اطلاع رسانی از طریق ایمیل', default=True)
    by_sms = models.BooleanField(verbose_name='اطلاع رسانی از طریق پیامک', default=False)
    by_phone = models.BooleanField(verbose_name='اطلاع رسانی از طریق تلفن گویا', default=False)

    class Meta:
        verbose_name = 'گروه اطلاع رسانی درخواست'
        verbose_name_plural = 'گروه های اطلاع رسانی درخواست ها'
        managed = True

    def __str__(self):
        return f"{self.request} در {self.notify_group}"   

class RequestNotifyGroup_ChangeType(models.Model):
    """ 
    در این جدول گروه های اطلاع رسانی به ازای هر نوع درخواست مشخص می شود
    زمانی که کاربر نوع درخواست را مشخص می کند به صورت خودکار تمامی گروه های اطلاع رسانی مربوطه
    برای آن درخواست کپی می شود
    مدیر مربوطه میتواند این گروه ها را کم و یا زیاد کند
    """
    changetype = models.ForeignKey(ChangeType, on_delete=models.CASCADE, 
                                    verbose_name='کد نوع تغییر', null=False)
    notify_group = models.ForeignKey(to=NotifyGroup, verbose_name='شناسه گروه اطلاع رسانی'
                                     ,db_column='notify_group_code', on_delete=models.CASCADE)
    by_email = models.BooleanField(verbose_name='اطلاع رسانی از طریق ایمیل', default=True)
    by_sms = models.BooleanField(verbose_name='اطلاع رسانی از طریق پیامک', default=False)
    by_phone = models.BooleanField(verbose_name='اطلاع رسانی از طریق تلفن گویا', default=False)
    
     
    class Meta:
        verbose_name = 'گروه اطلاع رسانی درخواست نوع درخواست'
        verbose_name_plural = 'گروه های اطلاع رسانی درخواست ها نوع درخواست'
        managed = True

    def __str__(self):
        return f"{self.request} در {self.notify_group}"   


class RequestCorp_ChangeType(models.Model):
    """
    در این جدول مشخص می شود که شرکت های مرتبط با نوع درخواست چه شرکت هایی هستند
    زمانی که کاربر نوع درخواست را مشخص می کند، کلیه شرکت های مربوطه در لیست شرکت های مرتبط با آن درخواست کپی می شوند 
    """
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
    """
        در این جدول اطلاعات تیم های مرتبط با نوع درخواست ذخیره می شود
        زمانی که کاربر یک نوع درخواست را انتخاب می کند، اطلاعات کلیه تیم های مرتبط برای آن درخواست کپی می شود
        کاربر بعدا می تواند برای آن درخواست خاص، تیم ها را کم و یا اضافه نماید
    """
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
    """ 
    به ازای هر درخواست یک سری اطلاعات تکمیلی داریم
    مثلا اطلاعات انواع مراکز داده در محل تغییر (ارتباطات مخابراتی، شبکه و ...) در این جدول ذخیره می شوند
    البته مقدار این جدول مربوط به نوع تغییر است.
    وقتی کاربر یک نوع تغییر را انتخاب می کند، کلیه اطلاعات تکمیلی درخواست در آن درخواست کپی می شود
    بعدا مدیر مربوطه می تواند این اطلاعات را ویرایش کند
    """
    extra_info = models.ForeignKey(to='ConstValue', on_delete=models.CASCADE, null=False, verbose_name='شناسه اطلاعات تکمیلی')
    change_type = models.ForeignKey(to='ChangeType', on_delete=models.CASCADE, null=False, verbose_name='شناسه نوع درخواست')
    class Meta:
        verbose_name = 'اطلاعات تکمیلی درخواست'
        verbose_name_plural = 'اطلاعات تکمیلی درخواست‌ها'

    def __str__(self) -> str:
        return f'{self.change_type.change_type_title} - {self.extra_info.Caption}'

class RequestCorp(models.Model):
    """
        این جدول دربردارنده اطلاعات شرکت های مرتبط با یک درخواست است
        در ابتدا این موارد با توجه به نوع درخواست که توسط کاربر مشخص می شود تعیین می شوند
        بعدا مدیر مربوطه می تواند آنها را تغییر دهد
    """
    request = models.ForeignKey(ConfigurationChangeRequest, on_delete=models.CASCADE, verbose_name='درخواست', null=False)
    corp_code = models.ForeignKey(Corp, on_delete=models.CASCADE, verbose_name='شرکت', null=False, db_column='corp_code')

    class Meta:
        verbose_name = 'شرکت در درخواست'
        verbose_name_plural = 'شرکت‌ها در درخواست‌ها'
        managed = True

    def __str__(self):
        return f"{self.corp_code} در {self.request}"

class RequestTeam(models.Model):
    """ 
        این جدول دربردارنده اطلاعات تیم های مرتبط با یک درخواست است
        در ابتدا این موارد با توجه به نوع درخواست که توسط کاربر مشخص می شود تعیین می شوند
        بعدا مدیر مربوطه می تواند آنها را تغییر دهد
    """
    request = models.ForeignKey(ConfigurationChangeRequest, on_delete=models.CASCADE, verbose_name='درخواست', null=False)
    team_code = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='تیم', null=False, db_column='team_code')

    class Meta:
        verbose_name = 'تیم در درخواست'
        verbose_name_plural = 'تیم‌ها در درخواست‌ها'
        managed = True

    def __str__(self):
        return f"{self.team_code} در {self.request}"


class RequestExtraInformation(models.Model):
    """ 
        به ازای هر درخواست یک سری اطلاعات تکمیلی داریم
        مثلا اطلاعات انواع مراکز داده در محل تغییر (ارتباطات مخابراتی، شبکه و ...) در این جدول ذخیره می شوند
        البته مقدار این جدول مربوط به نوع تغییر است.
        وقتی کاربر یک نوع تغییر را انتخاب می کند، کلیه اطلاعات تکمیلی درخواست در آن درخواست کپی می شود
        بعدا مدیر مربوطه می تواند این اطلاعات را ویرایش کند
    """    
    extra_info = models.ForeignKey(to=ConstValue, on_delete=models.CASCADE, null=False, verbose_name='شناسه اطلاعات تکمیلی')
    request = models.ForeignKey(to='ConfigurationChangeRequest', on_delete=models.CASCADE, null=False, verbose_name='شناسه درخواست')
    class Meta:
        verbose_name = 'اطلاعات تکمیلی درخواست'
        verbose_name_plural = 'اطلاعات تکمیلی درخواست‌ها'


    def __str__(self) -> str:
        return f'{self.request.change_title} - {self.extra_info.Caption}'        