# راه حل مشکل نمایش فایل‌های .pyc در git

## مشکل
فایل‌های `.pyc` در `.gitignore` مشخص شده‌اند اما هنوز در `git status` نمایش داده می‌شوند.

## علت
این فایل‌ها قبلاً در git ردیابی شده‌اند. اضافه کردن آن‌ها به `.gitignore` فقط برای فایل‌های جدید کار می‌کند، نه فایل‌های قبلاً ردیابی شده.

## راه حل

### روش ۱: استفاده از اسکریپت (توصیه می‌شود)
فایل `remove_pyc_from_git.bat` را اجرا کنید:
```cmd
remove_pyc_from_git.bat
```

### روش ۲: دستور دستی
در PowerShell یا CMD اجرا کنید:

```powershell
# حذف همه فایل‌های .pyc از ردیابی git
git ls-files | Select-String "\.pyc$" | ForEach-Object { git rm --cached $_ }
```

یا در CMD:
```cmd
for /f "delims=" %f in ('git ls-files ^| findstr /R "\.pyc$"') do git rm --cached "%f"
```

### روش ۳: حذف دستی فایل‌های خاص
اگر می‌خواهید فقط فایل‌های خاصی را حذف کنید:
```cmd
git rm --cached Config/__pycache__/__init__.cpython-313.pyc
git rm --cached Config/__pycache__/settings.cpython-313.pyc
# و به همین ترتیب برای بقیه فایل‌ها
```

## بعد از اجرا
1. فایل‌ها از ردیابی git حذف می‌شوند اما روی دیسک باقی می‌مانند
2. می‌توانید تغییرات را commit کنید:
   ```cmd
   git add .gitignore
   git commit -m "Remove .pyc files from git tracking"
   ```

## نکته مهم
- فایل‌های `.pyc` روی دیسک باقی می‌مانند (فقط از git حذف می‌شوند)
- از این به بعد git این فایل‌ها را نادیده می‌گیرد
- الگوهای `.gitignore` شما درست است و نیازی به تغییر ندارد


