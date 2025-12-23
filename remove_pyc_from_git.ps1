# Remove all .pyc files from git tracking
# This script removes .pyc files from git index without deleting them from disk

Write-Host "Finding all tracked .pyc files..." -ForegroundColor Yellow

# Get all tracked .pyc files
$pycFiles = git ls-files | Where-Object { $_ -match '\.pyc$' }

if ($pycFiles.Count -eq 0) {
    Write-Host "No .pyc files are currently tracked by git." -ForegroundColor Green
    exit 0
}

Write-Host "Found $($pycFiles.Count) tracked .pyc files" -ForegroundColor Yellow
Write-Host "Removing from git index..." -ForegroundColor Yellow

# Remove each file from git index
foreach ($file in $pycFiles) {
    git rm --cached $file
    Write-Host "Removed: $file" -ForegroundColor Gray
}

Write-Host "`nDone! All .pyc files have been removed from git tracking." -ForegroundColor Green
Write-Host "The files still exist on disk but are now ignored by git." -ForegroundColor Green
Write-Host "You can now commit this change." -ForegroundColor Green


