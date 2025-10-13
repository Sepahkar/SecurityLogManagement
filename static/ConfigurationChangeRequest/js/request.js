// کدهای عمومی که در تمامی فرم ها اجرا می شوند
'use strict';
const touchedFields = new Set(); // فیلدهایی که کاربر با آن‌ها تعامل داشته است
let isSubmitting = false; // وضعیت ارسال فرم


    /******************************توابع مربوط به نمایش پیامها******************/
class message_manager
{
    processContextMessages() {
        const contextMessage = $('meta[name="context-message"]').attr('content');
        const contextSuccess = $('meta[name="context-success"]').attr('content');
        const contextSuccessMessage = $('meta[name="context-success-message"]').attr('content');
        const contextWarningMessage = $('meta[name="context-warning-message"]').attr('content');
        
        if (contextMessage) {
            if (contextSuccess === 'false') {
                this.showErrorMessage(contextMessage);
            } else {
                this.showSuccessMessage(contextMessage);
            }
        }
        
        if (contextSuccessMessage) {
            this.showSuccessMessage(contextSuccessMessage);
        }
        
        if (contextWarningMessage) {
            this.showWarningMessage(contextWarningMessage);
        }
    }
    
    initializeForm() {
        let formMode = $('form').hasClass('readonly-form') ? 'READONLY' : 'EDIT';        
        console.log('فرم در حال بارگذاری...');
        console.log('حالت فرم:', formMode);

    }


    showSuccessMessage(message) {
        if (typeof showSuccess === 'function') {
            showSuccess(message, 'موفقیت');
        } else {
            alert(message);
        }
    }
    
    showErrorMessage(message) {
        if (typeof showError === 'function') {
            showError(message, 'خطا');
        } else {
            alert(message);
        }
    }
    
    showWarningMessage(message) {
        if (typeof showWarning === 'function') {
            showWarning(message, 'هشدار');
        } else {
            alert(message);
        }
    }

    /*
    چرا این کد درست کار نمی‌کند؟
    1. نام تابع فراخوانی شده در اینجا confirmDelete است، اما در فایل message-handler.js تابع به صورت MessageHandler.confirmDelete تعریف شده و همچنین به صورت window.showConfirmDelete نیز به window متصل شده است، و به احتمال زیاد confirmDelete به صورت global تابع نیست، بلکه باید از showConfirmDelete استفاده شود.
    2. حتی اگر confirmDelete موجود باشد، تابع هیچ عملی روی url و id انجام نمی‌دهد و هیچ فرایند حذف فراخوانی نمی‌شود.
    3. باید پس از تایید، عملیات حذف (مثلاً فراخوانی AJAX یا هدایت به url) انجام شود.
    4. بهتر است بررسی به جای typeof confirmDelete، typeof showConfirmDelete انجام شود یا حتی بهترین حالت: همیشه از MessageHandler.confirmDelete استفاده شود که در فایل message-handler.js تعریف شده است.

    راه حل پیشنهادی:
    فراخوانی صحیح تابع حذف، استفاده درست از پارامترها، و انجام عملیات پس از تایید کاربر.
    */

    confirmDeleteMessage(itemName, url, id, on_success, on_error) {
        // فرض: عملیات حذف باید با AJAX انجام شود یا به url هدایت شود
        if (typeof showConfirmDelete === 'function') {
            showConfirmDelete(itemName, () => {
                // مثال: ارسال درخواست AJAX برای حذف
                // فرض: AJAX_call از همین فایل قابل دسترسی است
                AJAX_call(
                    url,
                    { id: id }, // یا صرفاً null اگر سرور فقط URL نیاز دارد
                    (response) => { // on_success
                        if (on_success == 'function')
                            on_success(data)
                        // اختیاری: رفرش جدول، حذف سطر یا ... 
                        // location.reload(); // یا هر کار دیگر
                    },
                    (error) => { // on_error
                        // this.showErrorMessage('خطا در حذف: ' + (error?.message || ''));
                    }
                );
            }, () => {
                // کاربر لغو کرد
                this.showWarningMessage('عملیات حذف لغو شد.');
            });
        } else {
            alert('امکان حذف وجود ندارد');
        }
    }
}
    /********************توابع مدیریت نمایش المان های فرم و بارگذاری فرم*********** */
    
    // این تابع برای پیاده سازی رخدادهای سفارشی المان ها در هر فرم پیاده سازی می شود
    // در اینجا به جهت جلوگیری از بروز خطا آورده شده است
    function setupSpecialFromEventListeners()
    {

    }

class form_manager
{
    markTouched(selector) {
        touchedFields.add(selector);
    }
    
    showLoading(action) {
        isSubmitting = true;
        $('form').addClass('loading');
        $('button[type="button"][value="'+action+'"]').prop('disabled', true).text('در حال ارسال...');
    }
    
    hideLoading(action) {
        isSubmitting = false;
        $('form').removeClass('loading');
        if (action) {
            let btn = $('button[type="button"][value="'+action+'"]')
            let txt = btn.data('original-text')
            btn.prop('disabled', false).text(txt);
        }
    }

    // مدیریت اختصاصی عمومی
    setupEventListeners() {
        var formMode = $('form').hasClass('readonly-form') ? 'READONLY' : 'EDIT';
        if (formMode === 'READONLY') {
            return; // در حالت READONLY نیازی به event listeners نیست
        }
        
        // مدیریت رخدادهای اختصاصی فرم ها فراخوانی می شود
        setupSpecialFromEventListeners()

        // جلوگیری از submit خودکار فرم
        $('#requestForm').on('submit', function(e) { 
            e.preventDefault(); 
            return false; 
        });
    }    
}   
/********************************توابع صحت سنجی فرم********************** */

// این تابع در کد مخصوص هر فرم مجددا پیاده سازی می شود و وظیفه اعتبارسنجی فیلدهای آن فرم را برعهده دارد
// تعریف این تابع به این دلیل انجام شده که از بروز خطا جلوگیری شود
function validateSpecialForm(showErrors = false) {
    return true;
}

function validateForm(showErrors = false) {
    let isValid = true;
    // بعدا باید اینجا کدی بنویسیم که اعتبارسنجی عمومی (مثل فیلدهای اجباری یا تاریخ و ...) را انجام دهد
    isValid = validateSpecialForm(showErrors) && isValid;
    
    return isValid;
}

function toggleFieldValidation(selector, isValid, errorMessage, showError) {
    const field = $(selector);
    const errorElement = field.siblings('.invalid-feedback');
    
    // پاکسازی اولیه اگر نباید خطا نمایش داده شود
    if (!showError) {
        field.removeClass('is-invalid');
        // در صورت درست بودن، می‌توانیم کلاس معتبر را بگذاریم
        if (isValid) {
            field.addClass('is-valid');
        } else {
            field.removeClass('is-valid');
        }
        if (errorElement.length) {
            errorElement.remove();
        }
        return;
    }
    
    if (isValid) {
        field.removeClass('is-invalid').addClass('is-valid');
        if (errorElement.length) errorElement.remove();
    } else {
        field.removeClass('is-valid').addClass('is-invalid');
        if (errorElement.length === 0) {
            field.after('<div class="invalid-feedback">' + errorMessage + '</div>');
        }
    }
}

/************************توابع مربوط به ارسال فرم به سرور******************/
    // این تابع در اسکریپت های مربوط به هر فرم پیاده سازی می شود
    // اینجا صرفا آورده شده که به خطا نخوریم
    function handleSpecialFormSubmit(e, actionType = null) 
    {
        
    };

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    // helper: اطمینان از اینکه body شامل csrfmiddlewaretoken با مقدار cookie است
    function ensureCSRFInData(data) {
        const csrftoken = getCookie('csrftoken') || $('input[name="csrfmiddlewaretoken"]').val();
    
        // اگر فرم از نوع FormData است
        if (typeof FormData !== 'undefined' && data instanceof FormData) {
        data.set('csrfmiddlewaretoken', csrftoken);
        return { data, csrftoken, isFormData: true };
        }
    
        // اگر data رشته serialize شده است (query string)
        if (typeof data === 'string') {
        // اگر پارامتر csrfmiddlewaretoken وجود دارد، مقدارش را جایگزین کن
        if (/csrfmiddlewaretoken=/.test(data)) {
            data = data.replace(/(csrfmiddlewaretoken=)[^&]*/, '$1' + encodeURIComponent(csrftoken));
        } else {
            // اضافه کن
            if (data.length) data += '&';
            data += 'csrfmiddlewaretoken=' + encodeURIComponent(csrftoken);
        }
        return { data, csrftoken, isFormData: false };
        }
    
        // اگر data یک شیء جاوااسکریپتی است (برای JSON)
        if (data && typeof data === 'object') {
        data.csrfmiddlewaretoken = csrftoken;
        return { data, csrftoken, isJSON: true };
        }
    
        // fallback: هیچ داده‌ای نداریم — فقط هدر می‌فرستیم
        return { data, csrftoken, isFormData: false };
    }    

    function AJAX_call(url, data, on_success, on_error)
    {
        const message_manager_obj = new message_manager();

        // let csrftoken = $('input[name="csrfmiddlewaretoken"]').val() || getCookie('csrftoken');
        
        
        // مشکل اینه که گاهی توکن موجود در بدنه درخواست با توکن موجود در هدر که از کوکی می خواند فرق می کند
        // این اتفاق در درخواست های AJAX رخ می دهد
        // بنابراین ما باید توکن را از بدنه درخواست حذف کنیم و فقط در هدر بفرستیم
        const res = ensureCSRFInData(data);
        const csrftoken = res.csrftoken;

        // فراخوانی سرور  
        $.ajax({
            url: url,
            type: 'POST', // در jQuery بهتر است از type به جای method استفاده شود
            data: res.data,
            headers: { "X-CSRFToken": csrftoken },
            success: function(response) {
                if (response && response.success) {
                    if (typeof on_success === "function") {
                        on_success(response);
                    }
                } else {
                    let msg = 'خطا: ';
                    if (response && response.message) {
                        msg += response.message;
                    } else {
                        msg += 'پاسخ نامعتبر از سرور دریافت شد.';
                    }
                    message_manager_obj.showErrorMessage(msg);
                    if (typeof on_error === "function") {
                        on_error(response);
                    }
                }
            },
            error: function(xhr, status, error) {
                let errorMessage = 'خطا در ارتباط با سرور: ' + xhr.status + " - " + error;
                if (xhr.responseText) {
                    errorMessage += "\nاطلاعات سرور:\n" + xhr.responseText;
                }
                message_manager_obj.showErrorMessage(errorMessage);
                if (typeof on_error === "function") {
                    on_error(xhr);
                }
            }
        });
    }
    
// function handleFormSubmit(e, actionType = null) 
// {

//     // جلوگیری از ارسال چندباره
//     if (typeof isSubmitting !== 'undefined' && isSubmitting) {
//         return;
//     }
    
//     const message_manager_obj = new message_manager()
//     // اعتبارسنجی فرم (با نمایش خطاها)
//     if (!validateForm(true)) {
//         // toggleSubmitButton(false);
//         message_manager_obj.showWarningMessage('لطفاً خطاهای فرم را برطرف کنید.');
//         return;
//     }
    
//     const form_manager_obj = new form_manager()
//     // نمایش loading
//     form_manager_obj.showLoading(actionType);
    
//     // داده های فرم را دریافت می کنیم
//     const formEl = $('#requestForm')[0];
//     const formData = new FormData(formEl);

//     // در صورتی که action
//     // نامعلوم باشد از مقدار پیش فرض استفاده می کنیم
//     const resolvedAction = actionType || 'start';
//     // action را در داده ها قرار می دهیم
//     formData.set('action', resolvedAction);
    
//     // فرم را ارسال می کنیم
//     fetch('', {
//         method: 'POST',
//         body: formData,
//         headers: {
//             'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
//         }
//     })
//     // در صورتی که جوابی از سرور دریافت نشود
//     .then(response => {
//         if (!response.ok) {
//             throw new Error('خطا در ارتباط با سرور');
//         }
//         return response.json();
//     })
//     // در صورتی که جواب دریافت شود
//     .then(data => {

//         form_manager_obj.hideLoading();
//         // در صورتی که عملیات موفقیت آمیز باشد
//         if (data.success) {
//             // پیام موفقیت آمیز را نمایش می دهیم
//             const message = data.message
//             message_manager_obj.showSuccessMessage(message);
//             // حالت فرم را می خوانیم
//             var formMode = data.mode
//             // در صورتی که شناسه درخواست وجود داشته باشد
//             if (data.request_id) {
//                 setTimeout(() => {
//                     window.location.href = '/ConfigurationChangeRequest/' + data.request_id + '/';
//                 }, 2000);
//             }
//         } 
//         // اگر خطا بازگشت شده باشد
//         else {
//             message_manager_obj.showErrorMessage('خطا: ' + data.message);
//         }
//     })
//     // اگر خطای مدیریت نشده ای رخ داده باشد
//     .catch(error => {
//         form_manager_obj.hideLoading();
//         console.error('Error:', error);
//         message_manager_obj.showErrorMessage('خطا در ارسال درخواست: ' + error.message);
//     });
// }

function handleFormSubmit(e, actionType = null) {
    e.preventDefault(); // جلوگیری از رفتار پیش‌فرض فرم

    // جلوگیری از ارسال چندباره
    if (typeof isSubmitting !== 'undefined' && isSubmitting) {
        return;
    }
    isSubmitting = true; // تنظیم پرچم ارسال

    const message_manager_obj = new message_manager();
    // اعتبارسنجی فرم
    if (!validateForm(true)) {
        // message_manager_obj.showWarningMessage('لطفاً خطاهای فرم را برطرف کنید.');
        isSubmitting = false;
        return;
    }

    const form_manager_obj = new form_manager();
    // نمایش loading
    form_manager_obj.showLoading(actionType);

    // نوع فرم را به دست می آوریم
    var form_type = $('input[name="form_type"]').val() || 'request'

    var resolvedAction = actionType || 'start';
    // اگر فرم نوع تغییر باشد، عملیات ذخیره سازی است
    if (form_type != 'request')
        resolvedAction = 'save'
    // تنظیم action
    // formData.set('action', resolvedAction);
    $('#requestForm').find('input[name="action"]').val(resolvedAction);

    // داده‌های فرم
    const formEl = $('#requestForm')[0];
    // const formData = new FormData(formEl);
    const formData = $('#requestForm').serialize();

    // تنظیم URL (یا خالی برای URL فعلی یا از متغیر جنگو)
    var submitUrl = window.submitUrl || ''; // فرض می‌کنیم submitUrl توی HTML تعریف شده
    // // اگر فرم نوع تغییر باشد، آدرس متفاوت است
    // if (form_type != 'request')
    //     submitUrl += 'change-type'


    AJAX_call(submitUrl,formData,
        function on_success(data)
        {
            message_manager_obj.showSuccessMessage(data.message);

            if (data.request_id) {
                new_address =  window.location.origin + '/ConfigurationChangeRequest/' 
                if (form_type != 'request')
                    new_address += 'change-type/'
                
                new_address += data.request_id + '/';

                setTimeout(() => {
                    window.location.href =new_address;
                }, 2000);
            }
            isSubmitting = false; // بازگرداندن پرچم به حالت اولیه

        },
        function on_error(data)
        {
            // message_manager_obj.showErrorMessage('خطا: ' + data.message);
            isSubmitting = false; // بازگرداندن پرچم به حالت اولیه
        })


    // // ارسال درخواست
    // fetch(submitUrl, {
    //     method: 'POST',
    //     body: formData,
    //     headers: {
    //         'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
    //     }
    // })
    // .then(response => {
    //     if (!response.ok) {
    //         throw new Error('خطا در ارتباط با سرور: ' + response.status);
    //     }
    //     return response.json();
    // })
    // .then(data => {
    //     form_manager_obj.hideLoading(actionType);
    //     if (data.success) {
    //         message_manager_obj.showSuccessMessage(data.message);

    //         if (data.request_id) {
    //             setTimeout(() => {
    //                 window.location.href = window.location.origin + '/ConfigurationChangeRequest/' + data.request_id + '/';
    //             }, 2000);
    //         }
    //     } else {
    //         message_manager_obj.showErrorMessage('خطا: ' + data.message);
    //     }
    // })
    // .catch(error => {
    //     form_manager_obj.hideLoading(actionType);
    //     console.log('Error during fetch:', error);
    //     message_manager_obj.showErrorMessage('خطا در ارسال درخواست: ' + error.message);
    // })
    // .finally(() => {
    //     isSubmitting = false; // بازگرداندن پرچم به حالت اولیه
    // });
}


/***********************مدیریت رخدادهای اصلی و بارگذاری اولیه فرم******************/
    $(document).ready(function() 
    {

        let isSubmitting = false;
        let hasTriedSubmit = false; // آیا کاربر تلاش به ثبت کرده است؟

        // اضافه کردن console.log برای تست لود شدن فایل
        console.log('request.js loaded successfully!');    
    
       
        // متغیرهای سراسری
        let formMode = $('form').hasClass('readonly-form') ? 'READONLY' : 'EDIT';
        
        const form_manager_obj = new form_manager()
        form_manager_obj.setupEventListeners();

        // پردازش پیام‌های context (اگر وجود داشته باشند)
        const message_manager_obj = new message_manager();
        message_manager_obj.processContextMessages();

        // Event listener برای دکمه‌های فرم - فقط اگر handleFormSubmit تعریف شده باشد
        if (typeof handleGeneralFormSubmit === 'function') {
            $('button[type="button"]').click(
                function(e)
                {
                    var action = $(this).val()
                    if (e) e.preventDefault();
            
                    if (isSubmitting) {
                        return; // جلوگیری از ارسال چندباره
                    }
                    
                    hasTriedSubmit = true;

                    handleGeneralFormSubmit(e, action)
                }
            )
        }
    });