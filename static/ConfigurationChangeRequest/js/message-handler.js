/**
 * سیستم مدیریت پیام‌ها با استفاده از jquery-confirm
 * برای نمایش پیام‌های خطا، موفقیت و سایر پیام‌ها
 */

// تنظیمات پیش‌فرض برای jquery-confirm
$.confirm.defaults = {
    theme: 'modern',
    animation: 'scale',
    closeAnimation: 'scale',
    animationSpeed: 300,
    animationBounce: 1.2,
    draggable: true,
    dragWindowGap: 15,
    dragWindowBorder: true,
    useBootstrap: true,
    columnClass: 'col-md-6 col-md-offset-3 col-sm-8 col-sm-offset-2 col-xs-10 col-xs-offset-1',
    escapeKey: true,
    backgroundDismiss: false,
    closeIcon: true,
    closeIconClass: 'fa fa-times',
    icon: '',
    title: '',
    content: '',
    buttons: {},
    onOpenBefore: function () {
        // اضافه کردن کلاس RTL برای زبان فارسی
        this.$el.addClass('jconfirm-rtl');
    },
    onOpen: function () {
        // فوکوس روی دکمه اصلی
        setTimeout(() => {
            this.$btnc.find('button:first').focus();
        }, 100);
    }
};

// کلاس مدیریت پیام‌ها
class MessageHandler {
    
    /**
     * نمایش پیام موفقیت
     * @param {string} message - متن پیام
     * @param {string} title - عنوان پیام (اختیاری)
     * @param {Function} callback - تابع اجرا شده بعد از بستن (اختیاری)
     */
    static success(message, title = 'موفقیت', callback = null) {
        $.confirm({
            title: title,
            content: message,
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
                    keys: ['enter'],
                    action: function () {
                        if (callback && typeof callback === 'function') {
                            callback();
                        }
                    }
                }
            }
        });
    }

    /**
     * نمایش پیام خطا
     * @param {string} message - متن پیام
     * @param {string} title - عنوان پیام (اختیاری)
     * @param {Function} callback - تابع اجرا شده بعد از بستن (اختیاری)
     */
    static error(message, title = 'خطا', callback = null) {
        $.confirm({
            title: title,
            content: message,
            type: 'red',
            typeAnimated: true,
            icon: 'fa fa-exclamation-triangle',
            theme: 'modern',
            animation: 'shake',
            closeAnimation: 'scale',
            animationSpeed: 400,
            buttons: {
                ok: {
                    text: 'متوجه شدم',
                    btnClass: 'btn-red',
                    keys: ['enter'],
                    action: function () {
                        if (callback && typeof callback === 'function') {
                            callback();
                        }
                    }
                }
            }
        });
    }

    /**
     * نمایش پیام هشدار
     * @param {string} message - متن پیام
     * @param {string} title - عنوان پیام (اختیاری)
     * @param {Function} callback - تابع اجرا شده بعد از بستن (اختیاری)
     */
    static warning(message, title = 'هشدار', callback = null) {
        $.confirm({
            title: title,
            content: message,
            type: 'orange',
            typeAnimated: true,
            icon: 'fa fa-exclamation-circle',
            theme: 'modern',
            animation: 'bounce',
            closeAnimation: 'scale',
            animationSpeed: 350,
            buttons: {
                ok: {
                    text: 'باشه',
                    btnClass: 'btn-orange',
                    keys: ['enter'],
                    action: function () {
                        if (callback && typeof callback === 'function') {
                            callback();
                        }
                    }
                }
            }
        });
    }

    /**
     * نمایش پیام اطلاعات
     * @param {string} message - متن پیام
     * @param {string} title - عنوان پیام (اختیاری)
     * @param {Function} callback - تابع اجرا شده بعد از بستن (اختیاری)
     */
    static info(message, title = 'اطلاعات', callback = null) {
        $.confirm({
            title: title,
            content: message,
            type: 'blue',
            typeAnimated: true,
            icon: 'fa fa-info-circle',
            theme: 'modern',
            animation: 'slide',
            closeAnimation: 'slide',
            animationSpeed: 300,
            buttons: {
                ok: {
                    text: 'باشه',
                    btnClass: 'btn-blue',
                    keys: ['enter'],
                    action: function () {
                        if (callback && typeof callback === 'function') {
                            callback();
                        }
                    }
                }
            }
        });
    }

    /**
     * نمایش پیام تایید (بله/خیر)
     * @param {string} message - متن پیام
     * @param {string} title - عنوان پیام (اختیاری)
     * @param {Function} onConfirm - تابع اجرا شده در صورت تایید
     * @param {Function} onCancel - تابع اجرا شده در صورت لغو (اختیاری)
     */
    static confirm(message, title = 'تایید', onConfirm, onCancel = null) {
        $.confirm({
            title: title,
            content: message,
            type: 'blue',
            typeAnimated: true,
            icon: 'fa fa-question-circle',
            theme: 'modern',
            animation: 'scale',
            closeAnimation: 'scale',
            animationSpeed: 300,
            buttons: {
                confirm: {
                    text: 'بله',
                    btnClass: 'btn-blue',
                    keys: ['enter'],
                    action: function () {
                        if (onConfirm && typeof onConfirm === 'function') {
                            onConfirm();
                        }
                    }
                },
                cancel: {
                    text: 'خیر',
                    btnClass: 'btn-default',
                    keys: ['esc'],
                    action: function () {
                        if (onCancel && typeof onCancel === 'function') {
                            onCancel();
                        }
                    }
                }
            }
        });
    }

    /**
     * نمایش پیام تایید حذف
     * @param {string} itemName - نام آیتم مورد نظر
     * @param {Function} onConfirm - تابع اجرا شده در صورت تایید
     * @param {Function} onCancel - تابع اجرا شده در صورت لغو (اختیاری)
     */
    static confirmDelete(itemName, onConfirm, onCancel = null) {
        $.confirm({
            title: 'تایید حذف',
            content: `آیا از حذف "${itemName}" اطمینان دارید؟ این عملیات قابل بازگشت نیست.`,
            type: 'red',
            typeAnimated: true,
            icon: 'fa fa-trash',
            theme: 'modern',
            animation: 'shake',
            closeAnimation: 'scale',
            animationSpeed: 400,
            buttons: {
                confirm: {
                    text: 'بله، حذف کن',
                    btnClass: 'btn-red',
                    keys: ['enter'],
                    action: function () {
                        if (onConfirm && typeof onConfirm === 'function') {
                            onConfirm();
                        }
                    }
                },
                cancel: {
                    text: 'لغو',
                    btnClass: 'btn-default',
                    keys: ['esc'],
                    action: function () {
                        if (onCancel && typeof onCancel === 'function') {
                            onCancel();
                        }
                    }
                }
            }
        });
    }

    /**
     * نمایش فرم ورودی
     * @param {string} message - متن پیام
     * @param {string} title - عنوان پیام (اختیاری)
     * @param {string} placeholder - متن راهنما (اختیاری)
     * @param {Function} onSubmit - تابع اجرا شده در صورت ارسال
     * @param {Function} onCancel - تابع اجرا شده در صورت لغو (اختیاری)
     */
    static prompt(message, title = 'ورود اطلاعات', placeholder = '', onSubmit, onCancel = null) {
        $.confirm({
            title: title,
            content: '' +
                '<form action="" class="formName">' +
                '<div class="form-group">' +
                '<label>' + message + '</label>' +
                '<input type="text" placeholder="' + placeholder + '" class="form-control" required />' +
                '</div>' +
                '</form>',
            type: 'blue',
            typeAnimated: true,
            icon: 'fa fa-edit',
            theme: 'modern',
            animation: 'scale',
            closeAnimation: 'scale',
            animationSpeed: 300,
            buttons: {
                formSubmit: {
                    text: 'ارسال',
                    btnClass: 'btn-blue',
                    action: function () {
                        var input = this.$content.find('input').val();
                        if (!input) {
                            MessageHandler.error('لطفاً اطلاعات را وارد کنید');
                            return false;
                        }
                        if (onSubmit && typeof onSubmit === 'function') {
                            onSubmit(input);
                        }
                    }
                },
                cancel: {
                    text: 'لغو',
                    btnClass: 'btn-default',
                    keys: ['esc'],
                    action: function () {
                        if (onCancel && typeof onCancel === 'function') {
                            onCancel();
                        }
                    }
                }
            },
            onContentReady: function () {
                // باند کردن رویداد submit فرم
                var jc = this;
                this.$content.find('form').on('submit', function (e) {
                    e.preventDefault();
                    jc.$$formSubmit.trigger('click');
                });
                
                // فوکوس روی فیلد ورودی
                this.$content.find('input').focus();
            }
        });
    }

    /**
     * نمایش پیام بارگذاری
     * @param {string} message - متن پیام
     * @param {string} title - عنوان پیام (اختیاری)
     */
    static loading(message = 'در حال بارگذاری...', title = 'لطفاً صبر کنید') {
        return $.confirm({
            title: title,
            content: message,
            type: 'blue',
            typeAnimated: true,
            icon: 'fa fa-spinner fa-spin',
            theme: 'modern',
            animation: 'scale',
            closeAnimation: 'scale',
            animationSpeed: 300,
            closeIcon: false,
            escapeKey: false,
            backgroundDismiss: false,
            buttons: {}
        });
    }

    /**
     * نمایش پیام با آیکون سفارشی
     * @param {string} message - متن پیام
     * @param {string} title - عنوان پیام (اختیاری)
     * @param {string} iconClass - کلاس آیکون FontAwesome
     * @param {string} type - نوع پیام (success, error, warning, info)
     * @param {Function} callback - تابع اجرا شده بعد از بستن (اختیاری)
     */
    static custom(message, title = '', iconClass = 'fa fa-info-circle', type = 'blue', callback = null) {
        $.confirm({
            title: title,
            content: message,
            type: type,
            typeAnimated: true,
            icon: iconClass,
            theme: 'modern',
            animation: 'scale',
            closeAnimation: 'scale',
            animationSpeed: 300,
            buttons: {
                ok: {
                    text: 'باشه',
                    btnClass: 'btn-' + type,
                    keys: ['enter'],
                    action: function () {
                        if (callback && typeof callback === 'function') {
                            callback();
                        }
                    }
                }
            }
        });
    }
}

// تابع‌های کوتاه برای استفاده آسان
window.showSuccess = MessageHandler.success;
window.showError = MessageHandler.error;
window.showWarning = MessageHandler.warning;
window.showInfo = MessageHandler.info;
window.showConfirm = MessageHandler.confirm;
window.showConfirmDelete = MessageHandler.confirmDelete;
window.showPrompt = MessageHandler.prompt;
window.showLoading = MessageHandler.loading;
window.showCustom = MessageHandler.custom;

// مدیریت پیام‌های AJAX
$(document).ready(function() {
    
    // مدیریت پیام‌های موفقیت
    $(document).on('ajax:success', function(event, data, status, xhr) {
        if (data.success && data.message) {
            MessageHandler.success(data.message);
        }
    });

    // مدیریت پیام‌های خطا
    $(document).on('ajax:error', function(event, xhr, status, error) {
        let message = 'خطایی رخ داده است';
        if (xhr.responseJSON && xhr.responseJSON.message) {
            message = xhr.responseJSON.message;
        }
        MessageHandler.error(message);
    });

    // مدیریت پیام‌های فرم
    $('form').on('submit', function(e) {
        let $form = $(this);
        let $submitBtn = $form.find('button[type="submit"]');
        
        if ($submitBtn.length && !$submitBtn.prop('disabled')) {
            $submitBtn.prop('disabled', true);
            $submitBtn.html('<i class="fa fa-spinner fa-spin"></i> در حال ارسال...');
            
            // فعال کردن دوباره دکمه بعد از 5 ثانیه (برای جلوگیری از قفل)
            setTimeout(function() {
                $submitBtn.prop('disabled', false);
                $submitBtn.html('ارسال');
            }, 5000);
        }
    });
});
