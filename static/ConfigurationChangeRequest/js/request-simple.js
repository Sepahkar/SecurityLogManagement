/**
 * اسکریپت‌های فرم درخواست ساده
 * مدیریت حالت‌های مختلف فرم (INSERT, UPDATE, READONLY)
 */

$(document).ready(function() {
    'use strict';
    
    // اضافه کردن console.log برای تست لود شدن فایل
    console.log('request-simple.js loaded successfully!');
    
    // متغیرهای سراسری
    let formMode = $('form').hasClass('readonly-form') ? 'READONLY' : 'EDIT';
    let isSubmitting = false;
    let hasTriedSubmit = false; // آیا کاربر تلاش به ثبت کرده است؟
    const touchedFields = new Set(); // فیلدهایی که کاربر با آن‌ها تعامل داشته است
    
    // مقداردهی اولیه
    initializeForm();
    
    // پردازش پیام‌های context (اگر وجود داشته باشند)
    processContextMessages();
    
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
        console.log('فرم درخواست ساده در حال بارگذاری...');
        console.log('حالت فرم:', formMode);
        
        setupEventListeners();
        
        // در شروع، خطاها نشان داده نشوند و دکمه‌ها فعال باشند
        toggleSubmitButton(true);
    }
    
    function setupEventListeners() {
        if (formMode === 'READONLY') {
            return; // در حالت READONLY نیازی به event listeners نیست
        }
        
        $('#change_type').on('change', function() {
            markTouched('#change_type');
            validateChangeType();
            toggleSubmitButton(validateForm(false));
        });
        
        $('#change_title').on('input', function() {
            markTouched('#change_title');
            validateChangeTitle();
            toggleSubmitButton(validateForm(false));
        });
        
        $('#change_description').on('input', function() {
            markTouched('#change_description');
            validateChangeDescription();
            toggleSubmitButton(validateForm(false));
        });
        
        if ($('#user_team_role').length > 0) {
            $('#user_team_role').on('change', function() {
                markTouched('#user_team_role');
                validateUserTeamRole();
                toggleSubmitButton(validateForm(false));
            });
        }
        
        // نگه داشتن submit برای زمانی که کاربر Enter می‌زند
        $('#requestForm').on('submit', function(e) { handleFormSubmit(e, null); });
    }
    
    function markTouched(selector) {
        touchedFields.add(selector);
    }
    
    function handleFormSubmit(e, actionType = null) {
        if (e) e.preventDefault();
        
        if (isSubmitting) {
            return; // جلوگیری از ارسال چندباره
        }
        
        hasTriedSubmit = true;
        
        // اعتبارسنجی فرم (با نمایش خطاها)
        if (!validateForm(true)) {
            toggleSubmitButton(false);
            showWarningMessage('لطفاً خطاهای فرم را برطرف کنید.');
            return;
        }
        
        // نمایش loading
        showLoading();
        
        const formEl = document.getElementById('requestForm');
        const formData = new FormData(formEl);
        const resolvedAction = actionType || 'start';
        formData.set('action', resolvedAction);
        
        fetch('', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('خطا در ارتباط با سرور');
            }
            return response.json();
        })
        .then(data => {
            hideLoading();
            if (data.success) {
                const message = formMode === 'UPDATE' 
                    ? 'درخواست با موفقیت به‌روزرسانی شد'
                    : 'درخواست با موفقیت ایجاد شد';
                
                showSuccessMessage(message);
                
                // در صورتی که update باشد، باید به صفحه درخواست برود
                if (formMode === 'UPDATE') {
                    let targetUrl = '/ConfigurationChangeRequest/' + data.request_id + '/';
                    if (resolvedAction === 'approve') {
                        targetUrl += 'C/';
                    } else if (resolvedAction === 'reject') {
                        targetUrl += 'J/';
                    } else if (resolvedAction === 'back') {
                        targetUrl += 'R/';
                    }
                    setTimeout(() => {
                        window.location.href = targetUrl;
                    }, 2000);
                } else if (data.request_id) {
                    setTimeout(() => {
                        window.location.href = '/ConfigurationChangeRequest/' + data.request_id + '/';
                    }, 2000);
                }
            } else {
                showErrorMessage('خطا: ' + data.message);
            }
        })
        .catch(error => {
            hideLoading();
            console.error('Error:', error);
            showErrorMessage('خطا در ارسال درخواست: ' + error.message);
        });
    }
    
    // validateForm(showErrors)
    // اگر showErrors = true باشد، خطاها نمایش داده می‌شوند
    // اگر false باشد، فقط اعتبارسنجی منطقی انجام می‌شود بدون نمایش خطا برای فیلدهای لمس‌نشده
    function validateForm(showErrors = false) {
        let isValid = true;
        
        isValid = validateChangeTitle(showErrors) && isValid;
        isValid = validateChangeType(showErrors) && isValid;
        isValid = validateChangeDescription(showErrors) && isValid;
        isValid = validateUserTeamRole(showErrors) && isValid;
        
        return isValid;
    }
    
    function validateChangeTitle(showErrors = false) {
        const selector = '#change_title';
        const title = $(selector).val().trim();
        const isValid = title.length >= 3;
        toggleFieldValidation(selector, isValid, 'عنوان درخواست باید حداقل 3 کاراکتر باشد', showErrors || touchedFields.has(selector));
        return isValid;
    }
    
    function validateChangeType(showErrors = false) {
        const selector = '#change_type';
        const changeType = $(selector).val();
        const isValid = changeType !== '' && changeType !== null;
        toggleFieldValidation(selector, isValid, 'لطفاً نوع تغییر را انتخاب کنید', showErrors || touchedFields.has(selector));
        return isValid;
    }
    
    function validateChangeDescription(showErrors = false) {
        const selector = '#change_description';
        const description = $(selector).val().trim();
        const isValid = description.length >= 10;
        toggleFieldValidation(selector, isValid, 'توضیحات باید حداقل 10 کاراکتر باشد', showErrors || touchedFields.has(selector));
        return isValid;
    }
    
    function validateUserTeamRole(showErrors = false) {
        const selector = '#user_team_role';
        const $element = $(selector);
        if ($element.length === 0) {
            return true; // اگر فیلد وجود ندارد، معتبر فرض کن
        }
        const userTeamRole = $element.val();
        const isValid = userTeamRole !== '' && userTeamRole !== null;
        toggleFieldValidation(selector, isValid, 'لطفاً تیم و سمت را انتخاب کنید', showErrors || touchedFields.has(selector));
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
    
    function toggleSubmitButton(enabled) {
        const submitButton = $('button[type="submit"]');
        
        // دکمه‌ها در ابتدا باید فعال باشند؛ فقط زمانی غیرفعال شوند که بعد از سابمیت نامعتبر باشند
        if (enabled) {
            submitButton.prop('disabled', false).removeClass('btn-secondary').addClass('btn-primary');
        } else {
            // فقط بعد از تلاش برای ثبت، غیرفعال شود
            if (hasTriedSubmit) {
                submitButton.prop('disabled', true).removeClass('btn-primary').addClass('btn-secondary');
            } else {
                submitButton.prop('disabled', false).removeClass('btn-secondary').addClass('btn-primary');
            }
        }
    }
    
    function showLoading() {
        isSubmitting = true;
        $('form').addClass('loading');
        $('button[type="submit"]').prop('disabled', true).text('در حال ارسال...');
    }
    
    function hideLoading() {
        isSubmitting = false;
        $('form').removeClass('loading');
        $('button[type="submit"]').prop('disabled', false);
        
        if (formMode === 'UPDATE') {
            $('button[type="submit"]').text('به‌روزرسانی');
        } else {
            $('button[type="submit"]').text('شروع فرآیند');
        }
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
    
    // توابع عمومی برای استفاده خارجی
    window.RequestSimpleForm = {
        validateForm: validateForm,
        showSuccessMessage: showSuccessMessage,
        showErrorMessage: showErrorMessage,
        showWarningMessage: showWarningMessage
    };
});
