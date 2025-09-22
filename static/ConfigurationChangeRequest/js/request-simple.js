/**
 * اسکریپت‌های فرم درخواست ساده
 * مدیریت حالت‌های مختلف فرم (INSERT, UPDATE, READONLY)
 */

function setupSpecialFromEventListeners() {

    $('#change_type').on('change', function() {
        const form_manager_obj = new form_manager()
        form_manager_obj.markTouched('#change_type');
        validateChangeType();
    });
    
    $('#change_title').on('input', function() {
        const form_manager_obj = new form_manager()
        form_manager_obj.markTouched('#change_title');
        validateChangeTitle();
    });
    
    $('#change_description').on('input', function() {
        const form_manager_obj = new form_manager()
        form_manager_obj.markTouched('#change_description');
        validateChangeDescription();
    });
    
    if ($('#user_team_role').length > 0) {
        $('#user_team_role').on('change', function() {
            const form_manager_obj = new form_manager()
            form_manager_obj.markTouched('#user_team_role');
            validateUserTeamRole();
        });
    }
    
}


// validateForm(showErrors)
// اگر showErrors = true باشد، خطاها نمایش داده می‌شوند
// اگر false باشد، فقط اعتبارسنجی منطقی انجام می‌شود بدون نمایش خطا برای فیلدهای لمس‌نشده
function validateSpecialForm(showErrors = false) {
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


// function handleFormSubmit(e, actionType = null) {
//     // جلوگیری از ارسال چندباره
//     if (typeof isSubmitting !== 'undefined' && isSubmitting) {
//         return;
//     }
    
//     // اعتبارسنجی فرم (با نمایش خطاها)
//     if (!validateForm(true)) {
//         toggleSubmitButton(false);
//         showWarningMessage('لطفاً خطاهای فرم را برطرف کنید.');
//         return;
//     }
    
//     // نمایش loading
//     showLoading(actionType);
    
//     const formEl = document.getElementById('requestForm');
//     const formData = new FormData(formEl);
//     const resolvedAction = actionType || 'start';
//     formData.set('action', resolvedAction);
    
//     fetch('', {
//         method: 'POST',
//         body: formData,
//         headers: {
//             'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
//         }
//     })
//     .then(response => {
//         if (!response.ok) {
//             throw new Error('خطا در ارتباط با سرور');
//         }
//         return response.json();
//     })
//     .then(data => {
//         hideLoading();
//         if (data.success) {
//             const message = data.message
            
//             showSuccessMessage(message);
//             var formMode = data.mode
//             // در صورتی که update باشد، باید به صفحه درخواست برود
//             if (formMode === 'UPDATE') {
//                 let targetUrl = '/ConfigurationChangeRequest/' + data.request_id + '/';
//                 setTimeout(() => {
//                     window.location.href = targetUrl;
//                 }, 2000);
//             } else if (data.request_id) {
//                 setTimeout(() => {
//                     window.location.href = '/ConfigurationChangeRequest/' + data.request_id + '/';
//                 }, 2000);
//             }
//         } else {
//             showErrorMessage('خطا: ' + data.message);
//         }
//     })
//     .catch(error => {
//         hideLoading(actionType);
//         console.error('Error:', error);
//         showErrorMessage('خطا در ارسال درخواست: ' + error.message);
//     });
// }



$(document).ready(function() {

    
    // اضافه کردن console.log برای تست لود شدن فایل
    console.log('request-simple.js loaded successfully!');
    



    $('#change_type').change(function() {
        // وقتی نوع تغییر عوض شد، مقدار data-title و data-description گزینه انتخاب شده را می‌گیریم
        var selectedOption = $(this).find('option:selected');
        var change_title = selectedOption.data('title');
        var change_description = selectedOption.data('description');
    
        // اگر مقدار change_title نال نبود، در input مربوطه قرار بده
        if (change_title != null) {
            $('#change_title').val(change_title);
        }
    
        // اگر مقدار change_description نال نبود، در textarea مربوطه قرار بده
        if (change_description != null) {
            $('#change_description').val(change_description);
        }
    });
    

    
});
