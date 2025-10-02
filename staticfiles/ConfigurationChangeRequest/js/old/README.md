# فایل‌های JavaScript

## request-simple.js
این فایل شامل اسکریپت‌های مخصوص فرم درخواست ساده است.

### ویژگی‌ها:
- مدیریت حالت‌های مختلف فرم (INSERT, UPDATE, READONLY)
- اعتبارسنجی real-time فیلدها
- ارسال AJAX فرم
- نمایش پیام‌های مناسب
- مدیریت loading state

### توابع اصلی:
- `initializeForm()`: مقداردهی اولیه فرم
- `validateForm()`: اعتبارسنجی کامل فرم
- `handleFormSubmit()`: مدیریت ارسال فرم
- `showLoading()` و `hideLoading()`: مدیریت حالت بارگذاری

### متغیرهای سراسری:
- `formMode`: حالت فعلی فرم
- `isSubmitting`: وضعیت ارسال فرم

### API عمومی:
```javascript
window.RequestSimpleForm = {
    validateForm: validateForm,
    showSuccessMessage: showSuccessMessage,
    showErrorMessage: showErrorMessage,
    showWarningMessage: showWarningMessage
};
```

## message-handler.js
این فایل شامل کلاس MessageHandler و توابع کمکی برای نمایش پیام‌ها است.

### ویژگی‌ها:
- استفاده از jquery-confirm
- پیام‌های فارسی
- انیمیشن‌های مناسب
- پشتیبانی از انواع مختلف پیام

### توابع کمکی:
- `showSuccessMessage(message)`
- `showErrorMessage(message)`
- `showWarningMessage(message)`
- `showInfoMessage(message)`
