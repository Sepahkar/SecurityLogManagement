/**
 * اسکریپت‌های فرم ثبت درخواست تغییرات
 * استفاده از jQuery برای تعامل با کاربر
 */

$(document).ready(function() {
    'use strict';
    
    // متغیرهای سراسری
    let currentChangeType = null;
    let formData = {};
    
    // مقداردهی اولیه
    initializeForm();
    
    /**
     * مقداردهی اولیه فرم
     */
    function initializeForm() {
        console.log('فرم ثبت درخواست در حال بارگذاری...');
        
        // تنظیم event listeners
        setupEventListeners();
        
        // بارگذاری داده‌های اولیه
        loadInitialData();
        
        // اعتبارسنجی اولیه
        validateForm();
    }
    
    /**
     * تنظیم event listeners
     */
    function setupEventListeners() {
        // تغییر نوع تغییر
        $('#change_type').on('change', function() {
            handleChangeTypeChange();
        });
        
        // تغییر عنوان تغییر
        $('#change_title').on('input', function() {
            handleChangeTitleInput();
        });
        
        // تغییر شرح درخواست
        $('#change_description').on('input', function() {
            handleDescriptionInput();
        });
    
        // تغییر تیم و سمت
        $('.team-role-select').on('change', function() {
            handleTeamRoleChange();
        });
        
        // ارسال درخواست
        $('#submit-request').on('click', function(e) {
            e.preventDefault();
            handleSubmitRequest();
        });
        
        // ذخیره پیش‌نویس
        $('#save-draft').on('click', function(e) {
            e.preventDefault();
            handleSaveDraft();
        });
        
        // اعتبارسنجی real-time
        $('input, select, textarea').on('blur', function() {
            validateField($(this));
        });
        
        // اعتبارسنجی هنگام تایپ
        $('input, textarea').on('input', function() {
            validateField($(this));
        });
    }
    
    /**
     * بارگذاری داده‌های اولیه
     */
    function loadInitialData() {
        console.log('بارگذاری داده‌های اولیه...');
        
        // بررسی وجود تصویر کاربر
        checkUserImage();
        
        // بارگذاری انواع تغییرات
        loadChangeTypes();
        
        // تنظیم مقادیر پیش‌فرض
        setDefaultValues();
    }
    
    /**
     * بررسی وجود تصویر کاربر
     */
    function checkUserImage() {
        const userAvatar = $('#user-avatar');
        const originalSrc = userAvatar.attr('src');
        
        // تست بارگذاری تصویر
        const img = new Image();
        img.onload = function() {
            console.log('تصویر کاربر با موفقیت بارگذاری شد');
        };
        
        img.onerror = function() {
            console.log('تصویر کاربر یافت نشد، استفاده از تصویر پیش‌فرض');
            userAvatar.attr('src', '/static/ConfigurationChangeRequest/images/Avatar.png');
        };
        
        img.src = originalSrc;
    }
    
    /**
     * بارگذاری انواع تغییرات
     */
    function loadChangeTypes() {
        // این تابع می‌تواند برای بارگذاری دینامیک انواع تغییرات استفاده شود
        console.log('انواع تغییرات بارگذاری شدند');
    }
    
    /**
     * تنظیم مقادیر پیش‌فرض
     */
    function setDefaultValues() {
        // تنظیم تاریخ امروز
        const today = new Date();
        const persianDate = convertToPersianDate(today);
        
        // تنظیم سایر مقادیر پیش‌فرض
        formData.request_date = persianDate;
        formData.status = 'INSERT';
    }
    
    /**
     * تبدیل تاریخ میلادی به شمسی
     */
    function convertToPersianDate(date) {
        // این تابع باید با کتابخانه تبدیل تاریخ شمسی پیاده‌سازی شود
        return date.toLocaleDateString('fa-IR');
    }
    
    /**
     * مدیریت تغییر نوع تغییر
     */
    function handleChangeTypeChange() {
        const changeTypeId = $('#change_type').val();
        const changeTypeSelect = $('#change_type option:selected');
        
        if (changeTypeId) {
            // دریافت اطلاعات نوع تغییر انتخاب شده
            const changeTitle = changeTypeSelect.data('title');
            const changeDescription = changeTypeSelect.data('description');
            
            // ذخیره نوع تغییر فعلی
            currentChangeType = {
                id: changeTypeId,
                title: changeTitle,
                description: changeDescription
            };
            
            // پر کردن فیلدهای مربوطه
            if (changeTitle) {
                $('#change_title').val(changeTitle);
            }
            
            if (changeDescription) {
                $('#change_description').val(changeDescription);
            }
            
            // نمایش پیام موفقیت
            showMessage('نوع تغییر با موفقیت انتخاب شد', 'success');
            
            // اعتبارسنجی فرم
            validateForm();
        } else {
            // پاک کردن فیلدها
            $('#change_title').val('');
            $('#change_description').val('');
            currentChangeType = null;
        }
    }
    
    /**
     * مدیریت ورودی عنوان تغییر
     */
    function handleChangeTitleInput() {
        const changeTitle = $('#change_title').val();
        
        if (changeTitle.length > 0) {
            // اعتبارسنجی طول عنوان
            if (changeTitle.length < 10) {
                showFieldError('#change_title', 'عنوان تغییر باید حداقل 10 کاراکتر باشد');
            } else if (changeTitle.length > 200) {
                showFieldError('#change_title', 'عنوان تغییر نمی‌تواند بیشتر از 200 کاراکتر باشد');
            } else {
                clearFieldError('#change_title');
            }
        }
        
        // اعتبارسنجی فرم
        validateForm();
    }
    
    /**
     * مدیریت ورودی شرح درخواست
     */
    function handleDescriptionInput() {
        const description = $('#change_description').val();
        
        if (description.length > 0) {
            // اعتبارسنجی طول شرح
            if (description.length < 50) {
                showFieldError('#change_description', 'شرح درخواست باید حداقل 50 کاراکتر باشد');
            } else {
                clearFieldError('#change_description');
            }
        }
        
        // اعتبارسنجی فرم
        validateForm();
    }
    
    /**
     * مدیریت تغییر تیم و سمت
     */
    function handleTeamRoleChange() {
        const teamRole = $('.team-role-select').val();
        
        if (teamRole) {
            clearFieldError('.team-role-select');
            showMessage('تیم و سمت با موفقیت انتخاب شد', 'success');
        } else {
            showFieldError('.team-role-select', 'لطفاً تیم و سمت را انتخاب کنید');
        }
        
        validateForm();
    }
    
    /**
     * مدیریت ارسال درخواست
     */
    function handleSubmitRequest() {
        console.log('در حال ارسال درخواست...');
        
        // اعتبارسنجی کامل فرم
        if (!validateForm()) {
            showMessage('لطفاً تمام فیلدهای الزامی را تکمیل کنید', 'error');
            return;
        }
        
        // جمع‌آوری داده‌های فرم
        collectFormData();
        
        // نمایش loading
        showLoading();
        
        // ارسال درخواست
        submitFormData();
    }
    
    /**
     * مدیریت ذخیره پیش‌نویس
     */
    function handleSaveDraft() {
        console.log('در حال ذخیره پیش‌نویس...');
        
        // جمع‌آوری داده‌های فرم
        collectFormData();
        formData.is_draft = true;
        
        // نمایش loading
        showLoading();
        
        // ذخیره پیش‌نویس
        saveDraftData();
    }
    
    /**
     * جمع‌آوری داده‌های فرم
     */
    function collectFormData() {
        formData = {
            change_type: $('#change_type').val(),
            change_title: $('#change_title').val(),
            change_description: $('#change_description').val(),
            requestor_user_team_role: $('.team-role-select').val() || $('input[name="requestor_user_team_role"]').val(),
            request_date: formData.request_date,
            status: formData.status
        };
        
        console.log('داده‌های فرم جمع‌آوری شدند:', formData);
    }
    
    /**
     * ارسال داده‌های فرم
     */
    function submitFormData() {
        $.ajax({
            url: '/ConfigurationChangeRequest/request/',
            method: 'POST',
            data: formData,
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            success: function(response) {
                hideLoading();
                
                if (response.success) {
                    showMessage('درخواست با موفقیت ارسال شد', 'success');
                    
                    // انتقال به صفحه بعدی یا نمایش پیام موفقیت
                    setTimeout(function() {
                        window.location.href = '/ConfigurationChangeRequest/request/view/' + response.request_id + '/';
                    }, 2000);
                } else {
                    showMessage(response.errors || 'خطا در ارسال درخواست', 'error');
                }
            },
            error: function(xhr, status, error) {
                hideLoading();
                showMessage('خطا در ارتباط با سرور: ' + error, 'error');
                console.error('خطای AJAX:', error);
            }
        });
    }
    
    /**
     * ذخیره داده‌های پیش‌نویس
     */
    function saveDraftData() {
        $.ajax({
            url: '/ConfigurationChangeRequest/request/save_draft/',
            method: 'POST',
            data: formData,
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            success: function(response) {
                hideLoading();
                
                if (response.success) {
                    showMessage('پیش‌نویس با موفقیت ذخیره شد', 'success');
                } else {
                    showMessage(response.errors || 'خطا در ذخیره پیش‌نویس', 'error');
                }
            },
            error: function(xhr, status, error) {
                hideLoading();
                showMessage('خطا در ارتباط با سرور: ' + error, 'error');
                console.error('خطای AJAX:', error);
            }
        });
    }
    
    /**
     * اعتبارسنجی فیلد
     */
    function validateField(field) {
        const fieldId = '#' + field.attr('id');
        const fieldName = field.attr('name');
        const fieldValue = field.val();
        
        // بررسی فیلدهای الزامی
        if (field.prop('required') && !fieldValue) {
            showFieldError(fieldId, 'این فیلد الزامی است');
            return false;
        }
        
        // اعتبارسنجی خاص هر فیلد
        switch (fieldName) {
            case 'change_type':
                if (!fieldValue) {
                    showFieldError(fieldId, 'لطفاً نوع تغییر را انتخاب کنید');
                    return false;
                }
                break;
                
            case 'change_title':
                if (fieldValue && fieldValue.length < 10) {
                    showFieldError(fieldId, 'عنوان تغییر باید حداقل 10 کاراکتر باشد');
                    return false;
                }
                break;
                
            case 'change_description':
                if (fieldValue && fieldValue.length < 50) {
                    showFieldError(fieldId, 'شرح درخواست باید حداقل 50 کاراکتر باشد');
                    return false;
                }
                break;
                
            case 'requestor_user_team_role':
                if (!fieldValue) {
                    showFieldError(fieldId, 'لطفاً تیم و سمت را انتخاب کنید');
                    return false;
                }
                break;
        }
        
        clearFieldError(fieldId);
        return true;
    }
    
    /**
     * اعتبارسنجی کامل فرم
     */
    function validateForm() {
        let isValid = true;
        
        // اعتبارسنجی تمام فیلدها
        $('input[required], select[required], textarea[required]').each(function() {
            if (!validateField($(this))) {
                isValid = false;
            }
        });
        
        // بررسی نوع تغییر
        if (!$('#change_type').val()) {
            isValid = false;
        }
        
        // بررسی عنوان تغییر
        if (!$('#change_title').val()) {
            isValid = false;
        }
        
        // بررسی شرح درخواست
        if (!$('#change_description').val()) {
            isValid = false;
        }
        
        // فعال/غیرفعال کردن دکمه‌ها
        updateButtonStates(isValid);
        
        return isValid;
    }
    
    /**
     * به‌روزرسانی وضعیت دکمه‌ها
     */
    function updateButtonStates(isValid) {
        if (isValid) {
            $('#submit-request').prop('disabled', false).removeClass('btn-disabled');
            $('#save-draft').prop('disabled', false).removeClass('btn-disabled');
        } else {
            $('#submit-request').prop('disabled', true).addClass('btn-disabled');
            $('#save-draft').prop('disabled', true).addClass('btn-disabled');
        }
    }
    
    /**
     * نمایش خطای فیلد
     */
    function showFieldError(fieldId, message) {
        const field = $(fieldId);
        const errorDiv = field.siblings('.field-error') || $('<div class="field-error text-danger"></div>');
        
        errorDiv.text(message);
        errorDiv.addClass('text-danger');
        
        if (!field.siblings('.field-error').length) {
            field.after(errorDiv);
        }
        
        field.addClass('is-invalid');
    }
    
    /**
     * پاک کردن خطای فیلد
     */
    function clearFieldError(fieldId) {
        const field = $(fieldId);
        field.removeClass('is-invalid');
        field.siblings('.field-error').remove();
    }
    
    /**
     * نمایش پیام
     */
    function showMessage(message, type = 'info') {
        const alertClass = type === 'success' ? 'alert-success' : 
                          type === 'error' ? 'alert-danger' : 'alert-info';
        
        const alertHtml = `
            <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        // حذف پیام‌های قبلی
        $('.alert').remove();
        
        // نمایش پیام جدید
        $('.request-register-container').prepend(alertHtml);
        
        // حذف خودکار پیام بعد از 5 ثانیه
        setTimeout(function() {
            $('.alert').fadeOut();
        }, 5000);
    }
    
    /**
     * نمایش loading
     */
    function showLoading() {
        const loadingHtml = `
            <div class="loading-overlay">
                <div class="loading-spinner">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">در حال بارگذاری...</span>
                    </div>
                    <p class="loading-text">لطفاً صبر کنید...</p>
                </div>
            </div>
        `;
        
        $('body').append(loadingHtml);
    }
    
    /**
     * مخفی کردن loading
     */
    function hideLoading() {
        $('.loading-overlay').remove();
    }
    
    /**
     * دریافت CSRF token
     */
    function getCSRFToken() {
        return $('input[name="csrfmiddlewaretoken"]').val();
    }
    
    // تنظیمات اضافی
    console.log('اسکریپت فرم ثبت درخواست با موفقیت بارگذاری شد');
}); 