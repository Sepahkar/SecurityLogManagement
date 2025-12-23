@echo off
echo Finding all tracked .pyc files...
git ls-files | findstr /R "\.pyc$" > temp_pyc_files.txt

if %errorlevel% neq 0 (
    echo No .pyc files are currently tracked by git.
    del temp_pyc_files.txt 2>nul
    exit /b 0
)

echo Removing .pyc files from git index...
for /f "delims=" %%f in (temp_pyc_files.txt) do (
    git rm --cached "%%f"
    echo Removed: %%f
)

del temp_pyc_files.txt 2>nul
echo.
echo Done! All .pyc files have been removed from git tracking.
echo The files still exist on disk but are now ignored by git.
echo You can now commit this change.
pause


