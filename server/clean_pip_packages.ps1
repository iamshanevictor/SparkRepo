# PowerShell script to remove pip packages installed outside of .venv (except pip itself)

# Get list of all installed packages
$installedPackages = pip list --format=freeze | Where-Object { $_ -notmatch '^pip==' -and $_ -notmatch '^setuptools==' }

Write-Host "Removing pip packages installed outside of .venv environment..." -ForegroundColor Yellow

foreach ($package in $installedPackages) {
    $packageName = $package.Split('==')[0]
    Write-Host "Removing package: $packageName" -ForegroundColor Cyan
    pip uninstall -y $packageName
}

Write-Host "Cleanup complete. Only pip and setuptools remain in the global environment." -ForegroundColor Green
Write-Host "Remember to use .venv for all future Python package installations." -ForegroundColor Green
