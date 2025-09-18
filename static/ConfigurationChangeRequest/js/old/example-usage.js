/**
 * مثال‌های استفاده از سیستم پیام‌ها
 * این فایل نشان می‌دهد که چگونه از توابع مختلف نمایش پیام استفاده کنید
 */

// مثال 1: نمایش پیام موفقیت
function showSuccessExample() {
    showSuccess('درخواست با موفقیت ثبت شد');
}

// مثال 2: نمایش پیام خطا
function showErrorExample() {
    showError('خطا در ثبت درخواست. لطفاً دوباره تلاش کنید');
}

// مثال 3: نمایش پیام هشدار
function showWarningExample() {
    showWarning('اطلاعات وارد شده ناقص است. لطفاً تکمیل کنید');
}

// مثال 4: نمایش پیام اطلاعات
function showInfoExample() {
    showInfo('برای ادامه کار باید ابتدا اطلاعات پایه را تکمیل کنید');
}

// مثال 5: نمایش پیام تایید
function showConfirmExample() {
    showConfirm('آیا از ارسال این درخواست اطمینان دارید؟', 'تایید ارسال', function() {
        // کد اجرا شده در صورت تایید
        console.log('کاربر تایید کرد');
        showSuccess('درخواست ارسال شد');
    }, function() {
        // کد اجرا شده در صورت لغو
        console.log('کاربر لغو کرد');
    });
}

// مثال 6: نمایش پیام تایید حذف
function showConfirmDeleteExample() {
    showConfirmDelete('درخواست شماره 123', function() {
        // کد اجرا شده در صورت تایید
        console.log('آیتم حذف شد');
        showSuccess('آیتم با موفقیت حذف شد');
    }, function() {
        // کد اجرا شده در صورت لغو
        console.log('عملیات لغو شد');
    });
}

// مثال 7: نمایش فرم ورودی
function showPromptExample() {
    showPrompt('لطفاً کد ملی را وارد کنید:', 'ورود کد ملی', 'مثال: 1234567890', function(value) {
        // کد اجرا شده در صورت ارسال
        console.log('کد ملی وارد شده:', value);
        showSuccess('کد ملی ثبت شد: ' + value);
    }, function() {
        // کد اجرا شده در صورت لغو
        console.log('عملیات لغو شد');
    });
}

// مثال 8: نمایش loading
function showLoadingExample() {
    let loadingDialog = showLoading('در حال ذخیره اطلاعات...', 'لطفاً صبر کنید');
    
    // شبیه‌سازی عملیات طولانی
    setTimeout(function() {
        loadingDialog.close();
        showSuccess('اطلاعات با موفقیت ذخیره شد');
    }, 3000);
}

// مثال 9: نمایش پیام سفارشی
function showCustomExample() {
    showCustom(
        'این یک پیام سفارشی است با آیکون و رنگ خاص',
        'پیام سفارشی',
        'fa fa-star',
        'orange'
    );
}

// مثال 10: مدیریت AJAX responses
function handleAjaxResponse(response) {
    if (response.success) {
        if (response.message) {
            showSuccess(response.message);
        } else {
            showSuccess('عملیات با موفقیت انجام شد');
        }
        
        // اگر request_id وجود دارد، آن را ذخیره کنید
        if (response.request_id) {
            console.log('شناسه درخواست:', response.request_id);
        }
    } else {
        if (response.message) {
            showError(response.message);
        } else {
            showError('خطایی رخ داده است');
        }
    }
}

// مثال 11: مدیریت خطاهای AJAX
function handleAjaxError(xhr, status, error) {
    let message = 'خطایی رخ داده است';
    
    if (xhr.responseJSON && xhr.responseJSON.message) {
        message = xhr.responseJSON.message;
    } else if (xhr.status === 404) {
        message = 'صفحه مورد نظر یافت نشد';
    } else if (xhr.status === 500) {
        message = 'خطای سرور. لطفاً دوباره تلاش کنید';
    } else if (xhr.status === 403) {
        message = 'شما مجاز به انجام این عملیات نیستید';
    }
    
    showError(message);
}

// مثال 12: نمایش پیام‌های مختلف بر اساس نوع
function showMessageByType(type, message) {
    switch(type.toLowerCase()) {
        case 'success':
            showSuccess(message);
            break;
        case 'error':
            showError(message);
            break;
        case 'warning':
            showWarning(message);
            break;
        case 'info':
            showInfo(message);
            break;
        default:
            showInfo(message);
    }
}

// مثال 13: نمایش پیام با callback
function showMessageWithCallback() {
    showSuccess('عملیات با موفقیت انجام شد', 'موفقیت', function() {
        // این تابع بعد از بستن پیام اجرا می‌شود
        console.log('پیام بسته شد');
        // می‌توانید کاربر را به صفحه دیگری هدایت کنید
        // window.location.href = '/next-page/';
    });
}

// مثال 14: نمایش پیام‌های زنجیره‌ای
function showChainMessages() {
    showInfo('مرحله اول تکمیل شد', 'اطلاعات', function() {
        showSuccess('مرحله دوم تکمیل شد', 'موفقیت', function() {
            showWarning('مرحله سوم نیاز به بررسی دارد', 'هشدار', function() {
                showConfirm('آیا می‌خواهید ادامه دهید؟', 'تایید ادامه', function() {
                    showSuccess('تمام مراحل با موفقیت تکمیل شد');
                });
            });
        });
    });
}

// مثال 15: مدیریت فرم‌ها
function handleFormSubmit(formElement) {
    let $form = $(formElement);
    let $submitBtn = $form.find('button[type="submit"]');
    
    // غیرفعال کردن دکمه ارسال
    $submitBtn.prop('disabled', true);
    $submitBtn.html('<i class="fa fa-spinner fa-spin"></i> در حال ارسال...');
    
    // ارسال فرم با AJAX
    $.ajax({
        url: $form.attr('action'),
        method: $form.attr('method') || 'POST',
        data: $form.serialize(),
        success: function(response) {
            handleAjaxResponse(response);
        },
        error: function(xhr, status, error) {
            handleAjaxError(xhr, status, error);
        },
        complete: function() {
            // فعال کردن دوباره دکمه ارسال
            $submitBtn.prop('disabled', false);
            $submitBtn.html('ارسال');
        }
    });
}

// مثال 16: نمایش پیام‌های validation
function showValidationErrors(errors) {
    if (typeof errors === 'object') {
        let errorMessage = 'لطفاً خطاهای زیر را برطرف کنید:\n';
        for (let field in errors) {
            errorMessage += `• ${errors[field]}\n`;
        }
        showError(errorMessage);
    } else if (typeof errors === 'string') {
        showError(errors);
    }
}

// مثال 17: نمایش پیام‌های موفقیت با جزئیات
function showDetailedSuccess(title, details) {
    let content = details;
    if (Array.isArray(details)) {
        content = details.map(item => `• ${item}`).join('\n');
    }
    
    $.confirm({
        title: title,
        content: content,
        type: 'green',
        typeAnimated: true,
        icon: 'fa fa-check-circle',
        theme: 'modern',
        animation: 'zoom',
        closeAnimation: 'zoom',
        animationSpeed: 300,
        buttons: {
            ok: {
                text: 'باشه',
                btnClass: 'btn-green',
                keys: ['enter']
            }
        }
    });
}

// مثال 18: نمایش پیام با دکمه‌های سفارشی
function showCustomButtons() {
    $.confirm({
        title: 'انتخاب عملیات',
        content: 'لطفاً عملیات مورد نظر خود را انتخاب کنید',
        type: 'blue',
        typeAnimated: true,
        icon: 'fa fa-cogs',
        theme: 'modern',
        animation: 'scale',
        closeAnimation: 'scale',
        animationSpeed: 300,
        buttons: {
            edit: {
                text: 'ویرایش',
                btnClass: 'btn-blue',
                keys: ['e'],
                action: function() {
                    showInfo('عملیات ویرایش انتخاب شد');
                }
            },
            delete: {
                text: 'حذف',
                btnClass: 'btn-red',
                keys: ['d'],
                action: function() {
                    showConfirmDelete('این آیتم', function() {
                        showSuccess('آیتم حذف شد');
                    });
                }
            },
            view: {
                text: 'مشاهده',
                btnClass: 'btn-default',
                keys: ['v'],
                action: function() {
                    showInfo('عملیات مشاهده انتخاب شد');
                }
            },
            cancel: {
                text: 'لغو',
                btnClass: 'btn-default',
                keys: ['esc']
            }
        }
    });
}

// مثال 19: نمایش پیام با آیکون سفارشی
function showCustomIcon() {
    showCustom(
        'این پیام دارای آیکون سفارشی است',
        'پیام سفارشی',
        'fa fa-heart',
        'red'
    );
}

// مثال 20: نمایش پیام با انیمیشن سفارشی
function showCustomAnimation() {
    $.confirm({
        title: 'پیام با انیمیشن سفارشی',
        content: 'این پیام دارای انیمیشن سفارشی است',
        type: 'purple',
        typeAnimated: true,
        icon: 'fa fa-magic',
        theme: 'modern',
        animation: 'bounce',
        closeAnimation: 'shake',
        animationSpeed: 500,
        buttons: {
            ok: {
                text: 'باشه',
                btnClass: 'btn-purple',
                keys: ['enter']
            }
        }
    });
}

// اضافه کردن event listeners برای دکمه‌های مثال
$(document).ready(function() {
    // دکمه‌های مثال را به صفحه اضافه کنید
    if ($('#message-examples').length) {
        $('#message-examples').html(`
            <div class="row">
                <div class="col-md-6">
                    <h4>نمونه‌های پیام‌ها</h4>
                    <button class="btn btn-success mb-2" onclick="showSuccessExample()">پیام موفقیت</button><br>
                    <button class="btn btn-danger mb-2" onclick="showErrorExample()">پیام خطا</button><br>
                    <button class="btn btn-warning mb-2" onclick="showWarningExample()">پیام هشدار</button><br>
                    <button class="btn btn-info mb-2" onclick="showInfoExample()">پیام اطلاعات</button><br>
                    <button class="btn btn-primary mb-2" onclick="showConfirmExample()">پیام تایید</button><br>
                </div>
                <div class="col-md-6">
                    <h4>نمونه‌های پیشرفته</h4>
                    <button class="btn btn-danger mb-2" onclick="showConfirmDeleteExample()">تایید حذف</button><br>
                    <button class="btn btn-primary mb-2" onclick="showPromptExample()">فرم ورودی</button><br>
                    <button class="btn btn-info mb-2" onclick="showLoadingExample()">نمایش بارگذاری</button><br>
                    <button class="btn btn-warning mb-2" onclick="showCustomExample()">پیام سفارشی</button><br>
                    <button class="btn btn-success mb-2" onclick="showChainMessages()">پیام‌های زنجیره‌ای</button><br>
                </div>
            </div>
        `);
    }
});
