// کدهای عمومی که در تمامی فرم ها اجرا می شوند



    
    function processContextMessages() {
        const contextMessage = $('meta[name="context-message"]').attr('content');
        const contextSuccess = $('meta[name="context-success"]').attr('content');
        const contextSuccessMessage = $('meta[name="context-success-message"]').attr('content');
        const contextWarningMessage = $('meta[name="context-warning-message"]').attr('content');
        
        if (contextMessage) {
            if (contextSuccess === 'false') {
                showErrorMessage(contextMessage);
            } else {
                showSuccessMessage(contextMessage);
            }
        }
        
        if (contextSuccessMessage) {
            showSuccessMessage(contextSuccessMessage);
        }
        
        if (contextWarningMessage) {
            showWarningMessage(contextWarningMessage);
        }
    }
    
    function initializeForm() {
        let formMode = $('form').hasClass('readonly-form') ? 'READONLY' : 'EDIT';        
        console.log('فرم در حال بارگذاری...');
        console.log('حالت فرم:', formMode);

    }


    function showSuccessMessage(message) {
        if (typeof showSuccess === 'function') {
            showSuccess(message, 'موفقیت');
        } else {
            alert(message);
        }
    }
    
    function showErrorMessage(message) {
        if (typeof showError === 'function') {
            showError(message, 'خطا');
        } else {
            alert(message);
        }
    }
    
    function showWarningMessage(message) {
        if (typeof showWarning === 'function') {
            showWarning(message, 'هشدار');
        } else {
            alert(message);
        }
    }
    

    $(document).ready(function() 
    {
        'use strict';
        let isSubmitting = false;
        let hasTriedSubmit = false; // آیا کاربر تلاش به ثبت کرده است؟

        // اضافه کردن console.log برای تست لود شدن فایل
        console.log('request.js loaded successfully!');    
    
        // مقداردهی اولیه
        initializeForm();
        
        // پردازش پیام‌های context (اگر وجود داشته باشند)
        processContextMessages();

        // Event listener برای دکمه‌های فرم - فقط اگر handleFormSubmit تعریف شده باشد
        if (typeof handleFormSubmit === 'function') {
            $('button[type="button"]').click(
                function(e)
                {
                    var action = $(this).val()
                    if (e) e.preventDefault();
            
                    if (isSubmitting) {
                        return; // جلوگیری از ارسال چندباره
                    }
                    
                    hasTriedSubmit = true;

                    handleFormSubmit(e, action)
                }
            )
        }
    });