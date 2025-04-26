function toBoolean(value) {
    return value === true || value === 'True' || value === 1;
}
function toString(value) {
    return (value === null || value === undefined || value === 'None') ? '' : value;
}
// تابع برای تبدیل رشته به آرایه
function parseList(listString) {
    if (listString != undefined &&  listString.length>0) {
        listString = listString.replace(/'/g, '"'); // حذف / های اضافی
        return JSON.parse(listString); // تبدیل به آرایه
    }
    return [];
}
function toJalaali(year, month, day) {
    // محاسبه تعداد روزهای سال‌های میلادی تا سال مورد نظر
    var g_days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    if (year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0)) {
        g_days_in_month[1] = 29; // سال کبیسه
    }

    var g_day_no = day;
    for (var i = 0; i < month - 1; i++) {
        g_day_no += g_days_in_month[i];
    }
    g_day_no += (year - 1) * 365 + Math.floor((year - 1) / 4) - Math.floor((year - 1) / 100) + Math.floor((year - 1) / 400);

    // محاسبه سال جلالی
    var j_year = 1348 + Math.floor((g_day_no - 226899) / 1029983);
    var j_day_no = g_day_no - (j_year - 1348) * 1029983 + 226899;
    var j_month = 0;

    // محاسبه ماه و روز جلالی
    var j_days_in_month = [31, 31, 31, 31, 30, 30, 30, 30, 30, 30, 30, 29];
    if (j_year % 4 === 3) {
        j_days_in_month[11] = 30; // سال کبیسه جلالی
    }

    for (var j = 0; j < 12; j++) {
        if (j_day_no <= j_days_in_month[j]) {
            j_month = j + 1;
            break;
        }
        j_day_no -= j_days_in_month[j];
    }

    // اصلاح تاریخ جلالی
    j_year = j_year + 621; // تبدیل سال میلادی به جلالی
    return [j_year, j_month, j_day_no]; // بازگشت تاریخ جلالی
}
function IsValidPersianDate(dateString) {
    // الگوی عبارات منظم برای بررسی فرمت YYYY/MM/DD
    var regex = /^(140[0-3]|139[0-9])\/(0[1-9]|1[0-2])\/(0[1-9]|[12][0-9]|3[01])$/;

    // بررسی فرمت تاریخ
    if (!regex.test(dateString)) {
        return false; // فرمت نامعتبر
    }

    // جدا کردن سال، ماه و روز
    var parts = dateString.split('/');
    var year = parseInt(parts[0], 10);
    var month = parseInt(parts[1], 10);
    var day = parseInt(parts[2], 10);

    // بررسی تعداد روزهای ماه
    var daysInMonth = [31, 31, 31, 31, 30, 30, 30, 30, 30, 30, 30, 29]; // سال جلالی
    if (month === 12) {
        // اگر سال کبیسه باشد، اسفند 30 روز دارد
        if (year % 4 === 3) {
            daysInMonth[11] = 30; // سال کبیسه
        } else {
            daysInMonth[11] = 29; // سال غیر کبیسه
        }
    }

    // بررسی روز
    return day <= daysInMonth[month - 1] && day > 0; // بررسی روز
}
function IsValidTime(timeString) {
    // الگوی عبارات منظم برای بررسی فرمت HH:MM
    var regex = /^(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])$/;

    // بررسی فرمت زمان
    return regex.test(timeString); // بازگشت true یا false
}
function compare_persian_date(date1, date2) {
    // date1 و date2 باید به صورت آرایه [year, month, day] باشند
    var year1 = date1[0], month1 = date1[1], day1 = date1[2];
    var year2 = date2[0], month2 = date2[1], day2 = date2[2];

    // مقایسه سال‌ها
    if (year1 < year2) {
        return -1; // date1 قبل از date2
    } else if (year1 > year2) {
        return 1; // date1 بعد از date2
    }

    // اگر سال‌ها برابر بودند، ماه‌ها را مقایسه می‌کنیم
    if (month1 < month2) {
        return -1; // date1 قبل از date2
    } else if (month1 > month2) {
        return 1; // date1 بعد از date2
    }

    // اگر سال‌ها و ماه‌ها برابر بودند، روزها را مقایسه می‌کنیم
    if (day1 < day2) {
        return -1; // date1 قبل از date2
    } else if (day1 > day2) {
        return 1; // date1 بعد از date2
    }

    return 0; // date1 و date2 برابر هستند
}
function ActiveInActiveImages(imgs, active_inactive) {
    if (active_inactive=='inactive')
    {
        imgs.each(
            //چون مسیر تصویر هر آیکون متفاوت است نمی توانیم از یک دستور واحد استفاده کنیم
            //و باید حلقه استفاده شود
            function() {
                //تصویر عنصر فعال فعلی را غیرفعال می کنیم
                inactive_src = $(this).attr('src').split('.')[0] + '_Gray.png';
                $(this).attr('src', inactive_src)
            })    
    }
    else
    {
        imgs.each(
            //چون مسیر تصویر هر آیکون متفاوت است نمی توانیم از یک دستور واحد استفاده کنیم
            //
            function() {
                active_src = $(this).attr('src').replace('_Gray','')
                $(this).attr('src', active_src)
            })                
    }
}
function check_location(eleman_name) {
    var selector = $('input[name="'+ eleman_name +'"]')
    // بررسی اینکه آیا چک باکس مربوطه تیک خورده است
    if (selector.is(':checked')) {
        //بررسی اینکه آیا زیر مجموعه ای دارد؟
        if (selector.parent().parent().find('.check-list-box').length > 0) {
            //اگر از گزینه های زیرمجموعه هیچ موردی انتخاب نشده باشد
            if (selector.parent().parent().find('.check-list-box.active').length===0)
                return "با توجه به انتخاب گزینه " + selector.parent().find('label').text() + " لطفا یکی از گزینه های زیرمجموعه آن را انتخاب کنید.";
        }
    }
    return null; // اگر خطایی وجود نداشته باشد
}
function form_validation() {
    var errors = [];

    $('.required').removeClass('error'); // حذف کلاس error
    $('.required').each(function() {
        // حذف علامت ستاره قرمز از فیلدها
        $(this).prev('.red-star').remove(); // حذف ستاره قرمز
    });
    
    // بررسی فیلدهای اجباری
    $('.required').each(function() {
        if (!$(this).val()) {
            // اضافه کردن کلاس خطا
            $(this).addClass('error'); // اضافه کردن کلاس error
            errors.push($(this).data('field-name') + " الزامی است.");
            // اضافه کردن علامت ستاره قرمز
            $(this).before('<span class="red-star">*</span>'); // اضافه کردن ستاره قرمز
        }
    });
    /*-------------------------------------صفحه اول----------------------------------------------/
    /***************************************سطر اول********************************************* */
    //////////////////////////////////بخش اول//////////////////////////
    // افراد درگیر

    //////////////////////////////////بخش دوم//////////////////////////
    // ویژگی های تغییر


    /***************************************سطر دوم********************************************* */
    //////////////////////////////////بخش اول//////////////////////////
    //اطلاعات تغییر
    if (!$('select[name="change_type"]').val()) {
        errors.push("لطفا نوع تغییر را مشخص کنید.");
    }

    if (!$('input[name="change_location_data_center"]').is(':checked') && 
        !$('input[name="change_location_database"]').is(':checked') && 
        !$('input[name="change_location_systems"]').is(':checked') &&
        !$('input[name="change_location_other"]').is(':checked')) {
        errors.push("لطفا یکی از گزینه های محل تغییر را انتخاب کنید");
    }

    // بررسی محل تغییر: مرکز داده
    var dataCenterError = check_location('change_location_data_center');
    if (dataCenterError) {
        errors.push(dataCenterError);
    }

    // بررسی محل تغییر: پایگاه داده
    var databaseError = check_location('change_location_database');
    if (databaseError) {
        errors.push(databaseError);
    }

    // بررسی محل تغییر: سیستم‌ها
    var systemsError = check_location('change_location_systems');
    if (systemsError) {
        errors.push(systemsError);
    }

    //////////////////////////////////بخش دوم//////////////////////////
    //حوزه و ارتباطات تغییر
    //اگر گزینه نیاز به کمیته دارد انتخاب شده باشد باید کمیته هم انتخاب شده باشد
    if ($('input[name="need_committee"]:checked').val() === 1
        && $('select[name="committee"]').val() < 0)
        errors.push("با توجه به اینکه گزینه نیاز به کمیته دارد انتخاب شده است، باید کمیته مربوطه را انتخاب نمایید")

    //دامنه تغییر
    //باید یکی از گزینه های دامنه تغییر انتخاب شده باشد
    if (!$('.change-team-corp input[name="domain"]:checked'))
        errors.push("لطفا یکی از گزینه های 'درون سازمانی' یا 'بین سازمانی' یا 'برون سازمانی' را برای دامنه تغییرات انتخاب کنید")
    //در غیر این صورت باید کنترل کنیم با توجه به حوزه مربوطه، تیم یا شرکت را انتخاب کرده باشد
    else
    {
        //اگر گزینه درون سازمانی یا بین سازمانی انتخاب شده باشد
        if ($('.change-team-corp .radio-box.Domain_Inside').hasClass('active') ||
            $('.change-team-corp .radio-box.Domain_Between').hasClass('active'))
        {
            //باید حداقل یک تیم انتخاب شده باشد
            if ($('.change-team-corp .team-icons img.active').length === 0)
                errors.push("در قسمت دامنه تغییر، حداقل یک تیم را انتخاب کنید")
        }
        if ($('.change-team-corp .radio-box.Domain_Outside').hasClass('active') ||
            $('.change-team-corp .radio-box.Domain_Between').hasClass('active'))
        {
            //باید حداقل یک تیم انتخاب شده باشد
            if ($('.change-team-corp .corp-icons img.active').length === 0)
                errors.push("در قسمت دامنه تغییر، حداقل یک شرکت را انتخاب کنید")
        }
    }

    /*-------------------------------------صفحه دوم----------------------------------------------/
    /***************************************سطر اول********************************************* */
    //////////////////////////////////بخش اول//////////////////////////
    // زمانبندی تغییرات
    if ($('input[name="request_date"]').val() === '') {
        errors.push("لطفا زمان انجام تغییرات را مشخص کنید")
    }
    //اگر زمان معلوم شده باشد، باید مربوط به آینده باشد
    else
    {
        var persianDate = $('input[name="request_date"]').val();
        var requestTime = $('input[name="request_time"]').val();
        var today = new Date();
        var persianToday = toJalaali(today.getFullYear(), today.getMonth() + 1, today.getDate());
        // if (!IsValidPersianDate(persianDate)) {
        //     errors.push("تاریخ شمسی وارد شده معتبر نیست.");
        
        // } else if (compare_persian_date(persianDate, persianToday) <= 0) {
        //     errors.push("زمان درخواست تغییرات نمی تواند مربوط به گذشته باشد.");
        // }
        if (!IsValidTime(requestTime)) {
            errors.push("زمان درخواست باید در فرمت HH:MM باشد.");
        }
    }

    if ($('input[name="duration_hour"]').val() == 0
        && $('input[name="duration_minute"]').val() == 0) {
        errors.push("مدت زمان لازم برای انجام کار نمی‌تواند صفر باشد.");
    }
    var downtime = parseInt($('input[name="estimate_downtime_hour"]').val()) * 60 + parseInt($('input[name="estimate_downtime_minute"]').val())
    var worstcase = parseInt($('input[name="worstcase_downtime_hour"]').val()) * 60 + parseInt($('input[name="worstcase_downtime_minute"]').val())
    //بدترین زمان تخمین نمی تواند از زمان تخمینی اصلی کمتر باشد
    if (downtime > worstcase) {
        errors.push("بدترین تخمین قطعی سیستم باید بزرگتر یا مساوی میزان تخمین قطعی سیستم باشد.");
    }


    //////////////////////////////////بخش دوم//////////////////////////
    // حوزه اثرگذاری
    if ($('input[name="ImpactOnCriticalService"]').is(':checked') && !$('[name="ImpactOnCriticalServiceDescription"]').val()) {
        errors.push("با توجه به اینکه گزینه قطعی سرویس‌های حیاتی را انتخاب کرده اید، باید توضیحات مربوطه را وارد کنید.");
    }
    if ($('input[name="ImpactOnSensitiveService"]').is(':checked') && !$('[name="ImpactOnSensitiveServiceDescription"]').val()) {
        errors.push("با توجه به اینکه گزینه قطعی سرویس‌های حساس را انتخاب کرده اید، باید توضیحات مربوطه را وارد کنید.");
    }
    if (!$('input[name="ImpactOnSensitiveService"]').is(':checked') && !$('input[name="ImpactOnCriticalService"]').is(':checked') && !$('input[name="ImpactNotOnAnyService"]').is(':checked')) {
        errors.push("حداقل یکی از گزینه‌های منجر به قطعی سرویس‌های حساس، حیاتی یا عدم قطعی سرویس‌ها باید انتخاب شود.");
    }
    
    if (($('input[name="ImpactOnSensitiveService"]').is(':checked') || $('input[name="ImpactOnCriticalService"]').is(':checked')) && $('input[name="ImpactNotOnAnyService"]').is(':checked')) {
        errors.push("اگر گزینه عدم قطعی سرویس‌ها انتخاب شده باشد، نمی‌توانید گزینه‌های منجر به قطعی سرویس‌های حساس یا حیاتی را انتخاب کنید.");
    }


    /***************************************سطر دوم********************************************* */
    //////////////////////////////////بخش اول//////////////////////////
    // الزام به تغییر
    if ($('.reason-table input[type="checkbox"]:checked').length === 0) {
        errors.push("حداقل یکی از گزینه‌های الزام به تغییر باید انتخاب شود.");
    }

    //اگز گزینه سایر انتخاب شده باشد باید توضیحات بیان شود
    if ($('.reason-table input[name="ReasonOther"]').is(':checked')
        && $('.reason-table input[name="ReasonOtherDescription"]').val() === "")
    {
        errors.push("با توجه به اینکه برای دلایل الزام به تغییر گزینه 'سایر'' انتخاب شده است، باید در قسمت مربوطه توضیحات لازم را درج نمایید.");
    }

    //////////////////////////////////بخش دوم//////////////////////////
    // بازگشت تغییرات
    //باید حداقل یک گزینه را انتخاب کرده باشد
    if ($('input[name="Rollback"]:checked').length === 0) {
        errors.push("لطفا مشخص کنید که طرحی برای بازگشت تغییرات وجود دارد یا خیر")
    }
    else
    {
        //اگر طرح تغییری وجود دارد باید بیان شود
        if ($('input[name="Rollback"]:checked').val() == 1 
            && $('textarea[name="RollbackPlan"]').val() === '')
            errors.push("لطفاً طرح بازگشت را تکمیل کنید.");
    }


    return errors;
}


function ChangeLocation(list, list_class)
{
    if (list.length > 0)
        {

            // پیدا کردن div با کلاس data-center-list
            $('.'+list_class+' .check-list-box').each(function() {
                var box = $(this);
                var code =box.find('input[type="checkbox"').val()
                var img = box.find('img')
                // برای هر کد در changeLocation_datacenter_list
                list.forEach(function(item) {
                    // اگر قبلا انتخاب نشده باشد باید انتخاب شود
                    if (code == item && img.parents('.check-list-box').hasClass('inactive'))                
                        img.trigger('click');
                });
            });             

        }        
}
function SetTeamCorp(list, TeamCorp)
{
    if (list.length > 0)
    {
        
        //اگر مربوط به تیم ها باشد
        var div = $(".team-icons")
        // اگر مربوط به شرکت ها باشد
        if (TeamCorp === 'C')
            div = $(".corp-icons")

        div.find('.icon-list img').each(function() {
            var code = $(this).data("code")
            var img = $(this)

            list.forEach(function(item) {
                // اگر قبلا انتخاب نشده باشد باید انتخاب شود
                if (code == item && img.hasClass('inactive'))
                {
                    img.trigger("click")
                }
            });
        });
        //حالا می خواهیم گزینه طبقه بندی تغییر را تنظیم کنیم
        //ابتدا مقدار فعلی را به دست می آوریم
        domain = $("input[name='domain']:checked").val()
        //اگر این گزینه مربوط به تیم باشد و قبلا شرکتی انتخاب شده باشد
        //یا اینکه این گزینه شرکت باشد و قبلا تیمی انتخاب شده باشد
        //باید گزینه بین سازمانی انتخاب شود
        if ((TeamCorp === 'T' && (domain === 'Domain_Between' || domain === 'Domain_Outside')) ||
            (TeamCorp === 'C' && (domain === 'Domain_Between' || domain === 'Domain_Inside')))
            {
                $('.change-team-corp .radio-list img.Domain_Between').click()
            }
        //در غیر این صورت
        else
        {
            if (TeamCorp === 'T')
            {
                //اگر فقط تیم انتخاب شود، گزینه درون سازمانی را باید انتخاب کنیم
                $('.change-team-corp .radio-list img.Domain_Inside').click()
            }
            else 
            {
                //اگر فقط شرکت انتخاب شود، گزینه برون سازمانی را باید انتخاب کنیم
                $('.change-team-corp .radio-list img.Domain_Outside').click()
            }
        }
    }
}
function form_validation_committee()
{
    errors.push("لطفاً طرح بازگشت را تکمیل کنید.")
}
function form_validation_executor()
{

}
function form_validation_tester()
{

}
function confirm(request_status) {
    return new Promise(function(on_success,  on_failure) 
    {
    var error_message = []
    //اگر مدیر باشد نیازی به ورود اطلاعات ندارد
    //اگر کاربر کمیته باشد باید فیلدهای کاربر کمیته بررسی شوند
    if (request_status == 'COMITE')
    {
        error_message = form_validation_committee()
    }
    //اگر کاربر مجری باشد، باید فیلدهای کاربر مجری بررسی شوند
    else if (request_status == 'EXECUT')
    {
        error_message = form_validation_executor()
    }
    //اگر کاربر تستر باشد، باید فیلدهای کاربر تستر بررسی شوند
    else if (request_status == 'TESTER')
    {
        error_message = form_validation_tester()
    }
    

    // اگر خطا وجود دارد، نمایش پیام خطا
    if (error_message.length > 0) {
        $.alert({
            title: 'خطا',
            content: errors.join('<br>'),
        });
        return; // جلوگیری از ادامه
    }
    
    //شناسه درخواست را به دست می آوریم
    var requestId = $('input[name="request_id"]').val();
    
    //به سراغ مرحله بعدی می رویم
    var url = '/ConfigurationChangeRequest/request/next_step/' + requestId + '/CON/';

    // جمع‌آوری داده‌های فرم
    var formData = $('form').serialize();

    // ارسال درخواست AJAX
    $.ajax({
        url: url,
        method: 'POST',
        data: formData,
        success: function(response) 
        {
            if (response.success) 
            {
                if (response.message)
                    msg = response.message
                else
                    msg = 'اطلاعات با موفقیت ذخیره شده و فرم به مرحله بعدی ارسال شد'
                
                $.alert({
                    title: 'ارسال موفقیت آمیز',
                    content: msg,
                    buttons: {
                        confirm: {
                            text: 'بستن',
                            btnClass: 'btn-blue',
                            action: function() {
                                window.location.href = '/ConfigurationChangeRequest/request/view/'+response.request_id+'/';
                            }
                        }
                    }});                                
            } 
            else 
            {
                // در صورت بروز خطا، پیام‌های خطا را نمایش دهید
                var errorMessage = response.message;
                $.alert({
                    title: 'خطا',
                    content: errorMessage,
                });
                on_failure()
            }
        },
        error: function(xhr) 
        {
            // در صورت بروز خطا، پیام خطا را نمایش می‌دهیم
            // ایجاد یک عنصر موقتی
            var tempDiv = $('<div>').html(xhr.responseText);

            // استخراج متن از div با شناسه summary
            var errorMessage = tempDiv.find('#summary').text().trim(); // استفاده از #summary
            $.alert({
                title: 'خطا',
                content: errorMessage,
            });
            on_failure()
        }
        });
    
    //در صورت موفقیت آمیز بودن
    on_success
}
)
}
function reject()
{
    //شناسه درخواست را به دست می آوریم
    var requestId = $('input[name="request_id"]').val();
    
    //به سراغ مرحله بعدی می رویم
    var url = '/ConfigurationChangeRequest/request/next_step/' + requestId + '/REJ/';

    // جمع‌آوری داده‌های فرم


    $.confirm({
        title: 'دلیل رد',
        content: '' +
        '<form action="" class="formName">' +
        '<div class="form-group">' +
        '<label>دلیل رد مدرک را وارد کنید:</label>' +
        '<input type="text" placeholder="دلیل رد مدرک" class="reject-reason form-control" required />' +
        '</div>' +
        '</form>',
        buttons: {
            formSubmit: {
                text: 'رد مدرک',
                btnClass: 'btn-blue',
                action: function () {
                    var reject_reason = this.$content.find('.reject-reason').val();
                    if(!reject_reason){
                        $.alert('لطفا دلیل رد را وارد کنید');
                        return false;
                    }
                    var formData = {'reject_reason':reject_reason, 'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()}
                    // ارسال درخواست AJAX
                    $.ajax({
                        url: url,
                        method: 'POST',
                        data: formData,
                        success: function(response) 
                        {
                            if (response.success) 
                            {
                                if (response.message)
                                    msg = response.message
                                else
                                    msg = 'فرآیند مختومه شد'
                                
                                $.alert({
                                    title: 'خاتمه فرآیند',
                                    content: msg,
                                    buttons: {
                                        confirm: {
                                            text: 'بستن',
                                            btnClass: 'btn-blue',
                                            action: function() {
                                                window.location.href = '/ConfigurationChangeRequest/request/view/'+response.request_id+'/';
                                            }
                                        }
                                    }});                                
                            } 
                            else 
                            {
                                // در صورت بروز خطا، پیام‌های خطا را نمایش دهید
                                var errorMessage = response.message;
                                $.alert({
                                    title: 'خطا',
                                    content: errorMessage,
                                });
                                on_failure()
                            }
                        },
                        error: function(xhr) 
                        {
                            // در صورت بروز خطا، پیام خطا را نمایش می‌دهیم
                            // ایجاد یک عنصر موقتی
                            var tempDiv = $('<div>').html(xhr.responseText);
                
                            // استخراج متن از div با شناسه summary
                            var errorMessage = tempDiv.find('#summary').text().trim(); // استفاده از #summary
                            $.alert({
                                title: 'خطا',
                                content: errorMessage,
                            });
                            on_failure()
                        }
                        });
                }
            },
            cancel: {
                text:'انصراف',
                function () {
                    //close
                },
    
            }
        },
        onContentReady: function () {
            // bind to events
            var jc = this;
            this.$content.find('form').on('submit', function (e) {
                // if the user submits the form by pressing enter in the field.
                e.preventDefault();
                jc.$$formSubmit.trigger('click'); // reference the button and click it
            });
        }
    });    

    

}

/**
* @param {number} duration - مقدار زمان به دقیقه (باید عدد صحیح مثبت باشد)
* @param {jQuery} row - سلکتور jQuery که شامل input های مربوطه است
*/ 
function SetDuration(duration, row)
{
    // تبدیل به عدد صحیح
    duration = parseInt(duration);
    
    // محاسبه ساعت با تقسیم بر 60 و گرفتن قسمت صحیح
    var hours = Math.floor(duration / 60);
    
    // محاسبه دقیقه با گرفتن باقیمانده تقسیم بر 60 
    var minutes = duration % 60;
    
    // مقداردهی به input های مربوطه در row
    row.find('.hours').val(hours);
    row.find('.minutes').val(minutes);
}

function LoadData(selector) {
    var data = {};

    // 1- اطلاعات افراد درگیر
    data.executorNationalCode = toString($(selector).data('executor-nationalcode')); // کد ملی کاربر مجری
    data.testerNationalCode = toString($(selector).data('tester-nationalcode')); // کد ملی کاربر تست کننده
    data.testRequired = toBoolean($(selector).data('test-required')); // نیاز به تست

    // 2- ویژگی های تغییر
    data.changeLevel = toString($(selector).data('change-level')); // گستردگی تغییر
    data.classification = toString($(selector).data('classification')); // طبقه‌بندی
    data.priority = toString($(selector).data('priority')); // اولویت
    data.riskLevel = toString($(selector).data('risk-level')); // سطح ریسک

    // 3- اطلاعات تغییر
    data.changeTitle = toString($(selector).data('change-title')); // عنوان تغییر
    data.changeDescription = toString($(selector).data('change-description')); // توضیحات تغییر
    data.changeLocationDataCenter = toBoolean($(selector).data('change-location-data-center')); // محل تغییر: مرکز داده
    data.changeLocationDataCenterList = parseList($(selector).data('change-location-data-center-list')); // لیست محل تغییر: مرکز داده
    data.changeLocationDatabase = toBoolean($(selector).data('change-location-database')); // محل تغییر: پایگاه داده
    data.changeLocationDatabaseList = parseList($(selector).data('change-location-database-list')); // لیست محل تغییر: پایگاه داده
    data.changeLocationSystems = toBoolean($(selector).data('change-location-systems')); // محل تغییر: سیستم‌ها
    data.changeLocationSystemsList = parseList($(selector).data('change-location-systems-list')); // لیست محل تغییر: سیستم‌ها
    data.changeLocationOther = toBoolean($(selector).data('change-location-other')); // محل تغییر: سایر
    data.changeLocationOtherDescription = toString($(selector).data('change-location-other-description')); // توضیحات محل تغییر

    // 4- حوزه و ارتباطات تغییر
    data.needCommittee = toBoolean($(selector).data('need-committee')); // نیاز به کمیته
    data.committeeId = toString($(selector).data('committee-id')); // شناسه کمیته
    data.team_list = parseList($(selector).data('teams')) //لیست تیم های انتخاب شده
    data.corp_list  = parseList($(selector).data('corps')) //لیست شرکت های انتخاب شده

    // 5- زمانبندی تغییر
    data.changingDuration = parseInt($(selector).data('changing-duration')) || 0; // مدت زمان تغییرات
    data.downtimeDuration = parseInt($(selector).data('downtime-duration')) || 0; // مدت زمان توقف
    data.downtimeDurationWorstCase = parseInt($(selector).data('downtime-duration-worstcase')) || 0; // بدترین مدت زمان توقف

    // 6- اثرگذاری
    data.stopCriticalService = toBoolean($(selector).data('stop-critical-service')); // توقف خدمات بحرانی
    data.criticalServiceTitle = toString($(selector).data('critical-service-title')); // عنوان خدمات بحرانی
    data.stopSensitiveService = toBoolean($(selector).data('stop-sensitive-service')); // توقف خدمات حساس
    data.stopServiceTitle = toString($(selector).data('stop-service-title')); // عنوان خدمات متوقف شده
    data.notStopAnyService = toBoolean($(selector).data('not-stop-any-service')); // عدم توقف هیچ خدماتی

    // 7- برنامه بازگشت
    data.hasRoleBackPlan = toBoolean($(selector).data('has-role-back-plan')); // وجود برنامه بازگشت
    data.roleBackPlanDescription = toString($(selector).data('role-back-plan-description')); // توضیحات برنامه بازگشت

    // 8- الزامات
    data.reasonRegulatory = toBoolean($(selector).data('reason-regulatory')); // الزام قانونی
    data.reasonTechnical = toBoolean($(selector).data('reason-technical')); // الزام فنی
    data.reasonSecurity = toBoolean($(selector).data('reason-security')); // الزام امنیتی
    data.reasonBusiness = toBoolean($(selector).data('reason-business')); // الزام کسب و کاری
    data.reasonOther = toBoolean($(selector).data('reason-other')); // سایر الزامات
    data.reasonOtherDescription = toString($(selector).data('reason-other-description')); // توضیحات الزامات دیگر

    return data;
}

function FetchData(jsonData) {
    // 1- اطلاعات افراد درگیر
    if (jsonData.executorNationalCode) {
        $('select[name="executor_user_nationalcode"]').val(jsonData.executorNationalCode).change();
    }
    if (jsonData.testerNationalCode) {
        $('select[name="tester_user_nationalcode"]').val(jsonData.testerNationalCode).change();
    }
    $('input[name="need_test"][value=' + (jsonData.testRequired ? 1 : 0) + ']').prop('checked', true).change();

    // 2- ویژگی های تغییر
    if (jsonData.changeLevel) {
        $('input[name="change_level"][value="' + jsonData.changeLevel + '"]').parents('.radio-box').click();
    }
    if (jsonData.classification) {
        $('input[name="classification"][value="' + jsonData.classification + '"]').parents('.radio-box').click();
    }
    if (jsonData.priority) {
        $('input[name="priority"][value="' + jsonData.priority + '"]').parents('.radio-box').click();
    }
    if (jsonData.riskLevel) {
        $('input[name="risk_level"][value="' + jsonData.riskLevel + '"]').parents('.radio-box').click();
    }

    // 3- اطلاعات تغییر
    if (jsonData.changeTitle) {
        $('input[name="change_title"]').val(jsonData.changeTitle);
    }
    if (jsonData.changeDescription) {
        $('textarea[name="change_description"]').val(jsonData.changeDescription);
    }
    $('input[name="change_location_data_center"]').prop('checked', jsonData.changeLocationDataCenter);
    ChangeLocation(jsonData.changeLocationDataCenterList, 'data-center-list');
    $('input[name="change_location_database"]').prop('checked', jsonData.changeLocationDatabase);
    ChangeLocation(jsonData.changeLocationDatabaseList, 'database-list');
    $('input[name="change_location_systems"]').prop('checked', jsonData.changeLocationSystems);
    ChangeLocation(jsonData.changeLocationSystemsList, 'systems-list');
    $('input[name="change_location_other"]').prop('checked', jsonData.changeLocationOther);
    if (jsonData.changeLocationOtherDescription) {
        $('input[name="change_location_other_description"]').val(jsonData.changeLocationOtherDescription);
    }

    // 4- حوزه و ارتباطات تغییر
    $('input[name="need_committee"]').prop('checked', jsonData.needCommittee);
    if (jsonData.committeeId > 0) {
        $('select[name="committee"]').val(jsonData.committeeId);
    }
    SetTeamCorp(jsonData.team_list, 'T')
    SetTeamCorp(jsonData.corp_list, 'C')

    // 5- زمانبندی تغییر
    SetDuration(jsonData.changingDuration, $('.scheduling-table tr.duration'));
    SetDuration(jsonData.downtimeDuration, $('.scheduling-table tr.downtime'));
    SetDuration(jsonData.downtimeDurationWorstCase, $('.scheduling-table tr.downtime-worstcase'));

    // 6- اثرگذاری
    if (jsonData.stopCriticalService) 
    {
        $('input[name="ImpactOnCriticalService"]').prop('checked', true);
        if (jsonData.criticalServiceTitle) {
            $('input[name="ImpactOnCriticalServiceDescription"]').val(jsonData.criticalServiceTitle);
        }
    
    }
    if (jsonData.stopSensitiveService) 
    {
        $('input[name="ImpactOnSensitiveService"]').prop('checked', true);
        if (jsonData.stopServiceTitle) {
            $('input[name="ImpactOnSensitiveServiceDescription"]').val(jsonData.stopServiceTitle);
        }
    }
    //در صورتی که دو گزینه ی فوق انتخاب نشده باشد این گزینه انتخاب می شود
    if (!jsonData.stopCriticalService && !jsonData.stopSensitiveService && jsonData.notStopAnyService) 
        $('input[name="ImpactNotOnAnyService"]').prop('checked', true);

    // 7- برنامه بازگشت
    if (jsonData.hasRoleBackPlan) {
        $('input[name="Rollback"].has').prop('checked', true);
        
        if (jsonData.roleBackPlanDescription !== '') {
            $('textarea[name="RollbackPlan"]').val(jsonData.roleBackPlanDescription);
        }            
    }
    else
    {
        $('input[name="Rollback"].has-not').prop('checked', true);
        $('textarea[name="RollbackPlan"]').val('');
    }

    // 8- الزامات
    $('input[name="ReasonRegulatory"]').prop('checked', jsonData.reasonRegulatory);
    $('input[name="ReasonTechnical"]').prop('checked', jsonData.reasonTechnical);
    $('input[name="ReasonSecurity"]').prop('checked', jsonData.reasonSecurity);
    $('input[name="ReasonBusiness"]').prop('checked', jsonData.reasonBusiness);
    $('input[name="ReasonOther"]').prop('checked', jsonData.reasonOther);
    if (jsonData.reasonOtherDescription!=='') {
        $('input[name="ReasonOtherDescription"]').val(jsonData.reasonOtherDescription);
    }
}

$(document).ready(function() {
    // اضافه کردن رویداد برای Ctrl + S
    $(document).on('keydown', function(e) {
        if (e.altKey && e.key === 's') {
            e.preventDefault(); // جلوگیری از رفتار پیش‌فرض مرورگر
            $('#save').click(); // صدا زدن رخداد کلیک روی دکمه save
        }
    });

    $('.breadcrumbs__item').click(
        function()
        {
            // گرفتن شناسه آیتم کلیک شده
            var panel_id = 'pnl-step-' + $(this).attr('id').split('-')[1]; // استخراج شماره از id
            // مخفی کردن همه div هایی که با pnl شروع می شوند
            $('div[id^="pnl-step"]').hide();
            // نمایش div مربوط به شناسه پنل
            $('#' + panel_id).show();
        }
    )
    $('.radio-box').click(
        function()
        {
            //پدر رادیوی جاری را به دست می آوریم که همه رادیوهای آن گروه را دسترسی پیدا کنیم
            parent = $(this).parent()
            ActiveInActiveImages(parent.find('.active img'), 'inactive')

            //دکمه فعال قبلی را غیرفعال می کنیم
            parent.find('input[type="radio"]').prop('checked', false);
            parent.find('.active').removeClass('active').addClass('inactive');

            //حالا دکمه فعلی را فعال می کنیم
            ActiveInActiveImages($(this).find('img'), 'active')
            $(this).removeClass('inactive').addClass('active')
            $(this).find('input[type="radio"]').prop('checked', true);
        })

    $('.check-list-detail img').click(
        function()
        {
            check_list_box = $(this).parents('.check-list-box')
            //در اینجا هر عنصر یک آیکون است
            //در صورتی که آیکون فعال باشد آن را غیرفعال می کنیم
            //در غیر این صورت آن را فعال می کنیم
            if (check_list_box.hasClass('active'))
            {
                check_list_box.removeClass('active').addClass('inactive')
                check_list_box.find('input[type="checkbox"]').prop('checked', false);
                ActiveInActiveImages($(this), 'inactive')
                // اگر این آخرین مورد باشد، باید آیکون اصلی را غبرفعال کنیم
                if (check_list_box.parent().find('input[type="checkbox"]:checked').length == 0)
                    check_list_box.parents('.content-row').find('.check-list-main-checkbox input[type="checkbox"]').prop('checked', false);
            }
            else
            {
                check_list_box.removeClass('inactive').addClass('active')
                check_list_box.find('input[type="checkbox"]').prop('checked', true);
                ActiveInActiveImages($(this), 'active')
                check_list_box.parents('.content-row').find('.check-list-main-checkbox input[type="checkbox"]').prop('checked', true);
            }
        });
        // مربوط به لیست شرکت ها و لیست تیم ها
    $('.change-team-corp .icon-list img').click(
        function()
        {
            
            if ($(this).hasClass('active'))
                {
                    $(this).removeClass('active').addClass('inactive')
                    $(this).prev('input[type="checkbox"]').prop('checked', false);
                }
                else
                {
                    $(this).removeClass('inactive').addClass('active')
                    $(this).prev('input[type="checkbox"]').prop('checked', true);
                } 
            // در پایان باید کنترل کنیم که اگر تیمی/شرکتی انتخاب نشده باشد، چک باکس مربوطه را انتخاب کرده و یا از حالت انتخاب خارج کنیم
            if ($('.change-team-corp .icon-list img.inactive').length == 0)
                $(this).parent().parent().find('.team-corp-checkbox').prop('checked', true)
            else
                $(this).parent().parent().find('.team-corp-checkbox').prop('checked', false)
        });

    $('.change-team-corp .team-corp-checkbox').click(function()
    {
        //اگر مربوط به تیم ها باشد
        var icon_list = $(this).parent().parent().find('.icon-list')
        if ($(this).prop('checked'))
            icon_list.find('img.inactive').click()
        else
            icon_list.find('img.active').click()

    })
    $(".all-icon").click(function() {
        if (! $(this).prop('checked'))
        {
            $(this).parents('.content-row').find('img').removeClass('active').addClass('inactive')
            $(this).parents('.content-row').find('input[type="checkbox"]').prop('checked', false);
        }

        else
        {
            $(this).parents('.content-row').find('img').removeClass('inactive').addClass('active')
            $(this).parents('.content-row').find('input[type="checkbox"]').prop('checked', true);

        }

    });
    // هنگامی که بر روی هر یک از input های رادیویی یا label کلیک می‌شود
    $('.need-committee-box input').on('click', function() {
        // انتخاب گزینه رادیویی
        $(this).prop('checked', true);

        // بررسی اینکه آیا گزینه "دارد" انتخاب شده است
        if ($(this).val() == 1) {
            $('#committee').show(); // نمایش کومبو
        } else {
            $('#committee').hide(); // پنهان کردن کومبو
            $('#committee').val(-1)
        }
    });
    $('.need-committee-box label').on('click', function() {
        $(this).prev().click()
    });
    $('.change-team-corp .radio-list .radio-box').click(
        function()
        {
            //ابتدا همه پنل ها را مخفی می کنیم
            $('.change-team-corp .content-row.team-icons').hide()
            $('.change-team-corp .content-row.corp-icons').hide()

            // بررسی می کنیم که کدام گزینه انتخاب شده است
            var val = $(this).data('code')
            $(this).addClass('active')
            $("input[name='domain']:checked").val(val);

            // اگر گزینه داخلی و یا هر دو انتحاب شده باشد پنل تیم ها را نمایش می دهیم
            if (val == 'Domain_Inside' || val == 'Domain_Between')
                $('.change-team-corp .content-row.team-icons').show()

            // اگر گزینه خارجی و یا هر دو انتحاب شده باشد پنل شرکت ها را نمایش می دهیم
            if (val == 'Domain_Outside' || val == 'Domain_Between')
                $('.change-team-corp .content-row.corp-icons').show()

            // اگر گزینه تیم ها انتخاب شود، باید شرکت های انتخاب شده از حالت انتخاب خارج شوند
            if (val == 'Domain_Inside')
            {
                $('.change-team-corp .content-row.corp-icons input[type="checkbox"]').prop('checked', false);
                // شرکت هایی که انتخاب شده است را حذف می کنیم
                $('.change-team-corp .content-row.corp-icons img.active').each(function () {  
                    $(this).click()
                })
                $(this).find('.team-corp-checkbox.corp').prop('checked', false)

            }
            // اگر گزینه شرکت ها انتخاب شود، باید تیم های انتخاب شده از حالت انتخاب خارج شوند   
            if (val == 'Domain_Outside')
            {
                $('.change-team-corp .content-row.team-icons input[type="checkbox"]').prop('checked', false);
                // تیم هایی که انتخاب شده است را حذف می کنیم
                $('.change-team-corp .content-row.team-icons img.active').each(function () {  
                    $(this).click()
                })
                $(this).find('.team-corp-checkbox.team').prop('checked', false)
            }
        });
    $('.corp-icons img').click(function () {
        if ($(this).hasClass('active'))
            ActiveInActiveImages($(this), 'active')
        else
            ActiveInActiveImages($(this), 'inactive')
    })
    $('.user-select').on('change', function() {
        // اطلاعات مربوط به کاربر انتخاب شده را استخراج می کنیم
        var selectedUser = $(this).find(':selected');
        //کومبوی مربوط به سمت ها را انتخاب می کنیم
        var role_container = $(this).parent().find('.role-container');
        var role_selector = role_container.find('.role-select');
        var role_selector_single = role_container.find('.single-role');
        var role_selector_no_role = role_container.find('.no-role');

        //تصویر کاربر را پیدا می کنیم
        var img = $(this).parents('.user-info').find('.user-avatar img');        
        //نام کاربری و نام و نام خانوادگی را استخراج می کنیم
        var username = selectedUser.data('username')
        if (username == "" || username == undefined)
        {
            img.attr('src', '/static/ConfigurationChangeRequest/images/Avatar.png');
            img.attr('alt', 'کاربری انتخاب نشده است');
            img.attr('title', 'کاربری انتخاب نشده است');
            role_container.hide()
            return
        }
        role_container.show()
        username = username.split('@')[0];
        var fullname = selectedUser.data('fullname');
        var gender = selectedUser.data('gender');
        var national_code = selectedUser.val();



        //ابتدا کومبوی مربوطه را نمایش می دهیم
        role_selector.show()
        role_selector_single.hide()
        role_selector_no_role.hide()

        //همه سمت های کاربران را مخفی می کنیم
        role_selector.find('option').prop('hidden', true);
        //سمت های این کاربر را نشان می دهیم
        role_selector.find('option[data-national-code="' + national_code + '"]').prop('hidden', false);
        
        // انتخاب اولین رکورد
        role_selector.find('option[data-national-code="' + national_code + '"]').first().prop('selected', true);
        
        

        //حالا چک می کنیم اگر فقط یک سمت داشته باشد، کومبو را پنهان می کنیم
        if (role_selector.find('option:not([hidden])').length === 1) 
        {
            role_selector.hide();
            role = role_selector.find('option:not([hidden])').text();
            role_selector_single.text(role);
            role_selector_single.show();
        }

        //و اگر کاربر هیچ سمتی نداشته باشد، کومبو را پنهان می کنیم
        else if (role_selector.find('option:not([hidden])').length === 0)
        {
            role_selector.hide();
            role_selector_no_role.show() 
        }



        // تغییر تصویر پروفایل
        var imgSrc = img.attr('src');
        var basePath = imgSrc.substring(0, imgSrc.lastIndexOf('/') + 1); // یا می‌توانید از split استفاده کنید


        img.attr('src', basePath + 'personnel\\' + username + '.jpg');
        img.attr('alt', fullname);
        img.attr('title', fullname);

    });

    // مدیریت اجباری بودن فیلد کد ملی تستر
    $('input[name="need_test"]').change(function() {
        if ($(this).val() == 1) {
            // اگر گزینه "دارد" انتخاب شده باشد، کلاس required را اضافه می‌کنیم
            $('select[name="tester_user_select"]').addClass('required');
            $('select[name="tester_user_select"]').attr('required', true);
            $('.user-info.tester .user-avatar').css('opacity', 1);
            $('.user-info.tester .user-information').css('opacity', 1);
            $('.user-info.tester select[name="tester_user_select"]').prop('disabled', false);

        } else if ($(this).val() == 0) {
            // اگر گزینه "ندارد" انتخاب شده باشد، کلاس required را حذف می‌کنیم
            $('select[name="tester_user_select"]').removeClass('required');
            $('select[name="tester_user_select"]').attr('required', false);
            $('.user-info.tester .user-avatar').css('opacity', 0.3);
            $('.user-info.tester .user-information').css('opacity', 0.3);   
            //کاربر تستر را از حالت انتخاب خارج می کنیم
            $('.user-info.tester select[name="tester_user_select"]').prop('selectedIndex', 0);
            $('.user-info.tester select[name="tester_user_select"]').prop('disabled', true);
            //سمت کاربر تستر را پنهان می کنیم
            $('.user-info.tester .role-container').hide()

            //تصویر کاربر را پیدا می کنیم
            var img =  $('.user-info.tester .user-avatar img');        
            //تصویر کاربر را به حالت پیش فرض برمی گردانیم
            img.attr('src', '/static/ConfigurationChangeRequest/images/Avatar.png');
            img.attr('alt', 'کاربری انتخاب نشده است');
            img.attr('title', 'کاربری انتخاب نشده است');

        }
    });
    


    $('#save').click(function(event) {
        event.preventDefault(); // جلوگیری از ارسال فرم به صورت پیش‌فرض

        // گرفتن مقدار request_id
        var requestId = $('input[name="request_id"]').val();
        var url;
        var method;

        // اعتبارسنجی داده‌ها
        var errors = form_validation();

        // اگر خطا وجود دارد، نمایش پیام خطا
        if (errors.length > 0) {
            $.alert({
                title: 'خطا',
                content: errors.join('<br>'),
            });
            return; // جلوگیری از ادامه
        }

        // بررسی اینکه آیا request_id وجود دارد یا خیر
        if (requestId) {
            // اگر request_id وجود دارد، از سرویس update استفاده می‌کنیم
            url = '/ConfigurationChangeRequest/request/' + requestId + '/';
        } else {
            // اگر request_id وجود ندارد، از سرویس create استفاده می‌کنیم
            url = '/ConfigurationChangeRequest/request/0/';
        }

        // جمع‌آوری داده‌های فرم
        var formData = $('form').serialize(); // یا می‌توانید داده‌های خاصی را جمع‌آوری کنید

        // ارسال درخواست AJAX
        $.ajax({
            url: url,
            method: 'POST',
            data: formData,
            success: function(response) {
                if (response.success) {
                    //شناسه درخواست را مقداردهی می کنیم
                    //به این دلیل که اگر به هر دلیل شروع فرآیند به مشکل خورد، مشخص باشد که رکورد ایجاد شده است
                    $('#request_id').val(response.request_id)
                    //اگر فراخوانی موفقیت آمیز باشد، باید تابعی برای رفتن به مرحله بعد فراخوانی کنیم
                    url = '/ConfigurationChangeRequest/request/next_step/'+response.request_id+'/CON/';
                    data = {'request_id':response.request_id, 'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()}

                    $.ajax({
                        url: url,
                        method: 'POST',
                        data: data,
                        success: function(response) {
                            if (response.success) {
                                if (response.message)
                                    msg = response.message
                                else
                                    msg = 'اطلاعات با موفقیت ذخیره شده و فرم به مرحله بعدی ارسال شد'
            
                                $.alert({
                                    title: 'ارسال موفقیت آمیز',
                                    content: msg,
                                    buttons: {
                                        confirm: {
                                            text: 'بستن',
                                            btnClass: 'btn-blue',
                                            action: function() {
                                                window.location.href = '/ConfigurationChangeRequest/request/view/'+response.request_id+'/';
                                            }
                                        }
                                    }
                                    });                                
                            } else {
                                // در صورت بروز خطا، پیام‌های خطا را نمایش دهید
                                var errorMessage = response.message;
                                $.alert({
                                    title: 'خطا',
                                    content: errorMessage,
                                });
                            }
                        },
                        error: function(xhr) {
                            // در صورت بروز خطا، پیام خطا را نمایش می‌دهیم
                            // ایجاد یک عنصر موقتی
                            var tempDiv = $('<div>').html(xhr.responseText);

                            // استخراج متن از div با شناسه summary
                            var errorMessage = tempDiv.find('#summary').text().trim(); // استفاده از #summary
                            $.alert({
                                title: 'خطا',
                                content: errorMessage,
                            });
                        }
                    });
            

                } else {
                    // در صورت بروز خطا، پیام‌های خطا را نمایش دهید
                    var errorMessage = response.errors;
                    $.alert({
                        title: 'خطا',
                        content: errorMessage,
                    });
                }
            },
            error: function(xhr) {
                // در صورت بروز خطا، پیام خطا را نمایش می‌دهیم
                // ایجاد یک عنصر موقتی
                var tempDiv = $('<div>').html(xhr.responseText);

                // استخراج متن از div با شناسه summary
                var errorMessage = tempDiv.find('#summary').text().trim(); // استفاده از #summary
                $.alert({
                    title: 'خطا',
                    content: errorMessage,
                    buttons: {
                        confirm: {
                            text: 'بستن',
                            btnClass: 'btn-red',
                            action: function() {
                                // در اینجا می‌توانید اقدامات اضافی انجام دهید
                            }
                        }
                    }
                });
            }
        });
    });

    // هنگامی که یک گزینه جدید در فیلد نوع تغییر انتخاب می‌شود
    $('select[name="change_type"]').change(function() {
        // دریافت گزینه انتخاب شده
        var selectedOption = $(this).find('option:selected');
        //داده ها را از گزینه انتخاب شده واکشی می کنیم
        data = LoadData(selectedOption)
        //داده ها را در المان های متناظر مقداردهی می کنیم
        if (data && Object.keys(data).length > 0)
            FetchData(data)
    });

    $('button.confirm').click(function() {
        var statusClass = $(this).data('status');
        var $button = $(this); // ذخیره دکمه برای استفاده بعدی

        // غیرفعال کردن دکمه
        $button.prop('disabled', true);

        // فراخوانی تابع confirm
        confirm(statusClass).then(function() {
            // در اینجا می‌توانید کدهایی که بعد از اتمام تابع confirm باید اجرا شوند را قرار دهید
            // فعال کردن دکمه دوباره
            $button.prop('disabled', false);
        }).catch(function() {
            // در صورت بروز خطا، دکمه را دوباره فعال کنید
            $button.prop('disabled', false);
        });
    });

    $('#reject').click(function()
    {
        reject()        
    })
});
