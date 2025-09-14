# Requires -Version 5.0
$ErrorActionPreference = "Stop"

# Determine Python executable
$PY = "python"
if (Test-Path ".venv\Scripts\python.exe") {
    $PY = ".venv\Scripts\python.exe"
}

Write-Host "Using Python: $PY"
& $PY -m pip install --upgrade pip setuptools wheel

function Read-Packages($file) {
    if (-not (Test-Path $file)) { return @() }
    Get-Content $file | Where-Object {
        -not ($_ -match '^\s*(#|$|-r\s+)')
    } | ForEach-Object {
        ($_ -replace ';.*$', '') -replace '==.*$', ''
    }
}

function Get-Version($pkg) {
    try {
        $output = & $PY -m pip show $pkg 2>&1
        # Filter out logging errors and empty lines
        $versionLine = $output | Where-Object { $_ -match '^Version:' }
        if ($versionLine) {
            return $versionLine.ToString().Split(':')[1].Trim()
        }
    } catch {
        # Ignore errors
        return $null
    }
    return $null
}
function Remove-NonAscii($text) {
    return ($text -replace '[^\u0000-\u007F]', '')
}

function Write-PinnedFile($src, $dst) {
    if (-not (Test-Path $src)) { return }
    $output = @()
    Get-Content $src | ForEach-Object {
        $line = $_
        $trim = $line.Trim()
        if ($trim -eq "" -or $trim.StartsWith("#")) {
            $output += $line; return
        }
        if ($trim -match '^-r\s+') {
            $output += $line; return
        }
        $base = $trim.Split(";")[0]
        $marker = ""
        if ($trim -like "*;*") {
            $marker = "; " + ($trim -split ";",2)[1]
        }
        $pkg = $base -replace '==.*$', ''
        Write-Host "Checking version for package: $pkg"  # <--- Add this line
        $ver = Get-Version $pkg
        if ($ver) {
            $newline = "$pkg==$ver$marker"
        } else {
            $newline = $line
        }
        $output += Remove-NonAscii $newline
    }
    Set-Content $dst -Value $output
    Write-Host "Updated $dst"
}

# runtime
if (Test-Path "requirements.txt") {
    foreach ($p in Read-Packages "requirements.txt") {
        Write-Host "Updating $p ..."
        & $PY -m pip install --upgrade $p
    }
    Write-PinnedFile "requirements.txt" "requirements.txt"
}

# dev
if (Test-Path "requirements-dev.txt") {
    foreach ($p in Read-Packages "requirements-dev.txt") {
        Write-Host "Updating $p ..."
        & $PY -m pip install --upgrade $p
    }
    Write-PinnedFile "requirements-dev.txt" "requirements-dev.txt"
}

# Update all requirements*.txt files in the current directory
Get-ChildItem -Path . -Filter "requirements*.txt" | ForEach-Object {
    $file = $_.FullName
    Write-Host "Processing $file ..."
    foreach ($p in Read-Packages $file) {
        Write-Host "Updating $p ..."
        & $PY -m pip install --upgrade $p
    }
    Write-PinnedFile $file $file
}

# Write lock file
& $PY -m pip freeze | ForEach-Object { Remove-NonAscii $_ } | Set-Content "requirements.lock.txt"
Write-Host "Wrote requirements.lock.txt"
