#requires -version 2

[CmdLetBinding()]
param
(
    [string]$packageDownloadUrl = "https://dl.google.com/android/repository/sdk-tools-windows-3859397.zip",
    [string]$toolLocation = "Android_Tools",
    [string[]]$packagesToInstall,
    [string[]] $customNdkVersions,
    [System.Net.WebProxy]$proxy,
    [switch]$force
)

# Stop in case of any error
$ErrorActionPreference = 'Stop'

$tempLocation = $env:TEMP
$zipFile = 'AndroidTools.zip'
$toolsBin = Join-Path -Path 'tools' -ChildPath 'bin'
$treatedToolsLocation = [System.IO.Path]::GetFullPath($toolLocation)
$ndksArchiveLocation = Join-Path -Path $treatedToolsLocation -ChildPath 'ndk-bundle-old'
$ndkVariablePrefix = 'ANDROID_NDK_OLD'
$variablesScope = 'User'

function Download
{
    param (
        [string]$packageDownloadUrl,
        [System.Net.WebProxy]$proxy,
        [string]$file
    )

    $downloader = new-object System.Net.WebClient
    if ($proxy -ne $null)
    {
        $downloader.Proxy = $proxy
    }
    $downloader.Proxy.Credentials = [System.Net.CredentialCache]::DefaultNetworkCredentials
    $downloader.Credentials = $ldapCredentials

    Write-Verbose "Downloading $packageDownloadUrl to $file"
    $downloader.DownloadFile($packageDownloadUrl, $file)
}

function Unzip
{
    param (
        [string] $targetDir,
        [string] $file,
        [boolean] $keepZipFile = $false
    )

    Write-Verbose "Extracting $file to $targetDir..."
    $shellApplication = new-object -com shell.application
    $zipPackage = $shellApplication.NameSpace($file)
    $destinationFolder = $shellApplication.NameSpace($targetDir)
    $destinationFolder.CopyHere($zipPackage.Items(), 0x10)

    if($keepZipFile -eq $false)
    {
        Remove-Item -Path $file -Force
    }
}

function Write-Licenses
{
    param
    (
        [string]$toolLocation
    )

    $licensesFolder = Join-Path -Path $toolLocation -ChildPath 'licenses'
    New-Item -ItemType Container -Path $licensesFolder -Force | Out-Null

    @"

d56f5187479451eabf01fb78af6dfcb131a6481e

24333f8a63b6825ea9c5514f83c2829b004d1fee
"@ | Set-Content -Path (Join-Path -Path $licensesFolder -ChildPath 'android-sdk-license')
}

$binFolder = Join-Path -Path $treatedToolsLocation -ChildPath $toolsBin
$zipLocaion = Join-Path -Path $tempLocation -ChildPath $zipFile

if ((-not (Test-Path -Path $binFolder)) -or $force.IsPresent)
{
    Write-Host "Cleaning ..."
    Remove-Item -Path $treatedToolsLocation -Recurse -Force -ErrorAction SilentlyContinue
    
    Write-Host "Installing basic tools ..."
    New-Item -ItemType Container -Path $treatedToolsLocation -Force | Out-Null
    Download -packageDownloadUrl $packageDownloadUrl -file $zipLocaion -proxy $proxy
    Unzip -file $zipLocaion -targetDir $treatedToolsLocation
    Write-Host "SDK Manager installed." -ForegroundColor Green
}

if (-not (Test-Path -Path $binFolder))
{
    throw "Path to bin folder '$binFolder' cannot be resolved."
}

Write-Licenses -toolLocation $treatedToolsLocation

Write-Host "Running installation of '$packagesToInstall' ..."
$executable = "$(Resolve-Path -Path (Join-Path -Path $binFolder -ChildPath 'sdkmanager.bat'))"
$params = @()

if ($proxy -ne $null)
{
    $params += ("--proxy=http", "--proxy_host=$($proxy.Address.Host)", "--proxy_port=$($proxy.Address.Port)")
}

foreach ($package in $packagesToInstall)
{
    $procuredPackage = $package -replace '"', ''
    $params += "`"$procuredPackage`""
}

Write-Verbose "Executing command '$executable $params' ... This might take long time."
& $executable $params 

if ($LASTEXITCODE -gt 0)
{
    Write-Error "Nonzero exit code returned. (code: '$LASTEXITCODE')"
    exit
}

Write-Host "Required packages installed." -ForegroundColor Green

Write-Verbose "Delete all previous NDK archive variables."
Get-ChildItem Env:"$ndkVariablePrefix*" | ForEach-Object {
    $variableName = $_.Name
    Write-Host "Cleaning environment variable '$variableName'"
    [Environment]::SetEnvironmentVariable("$variableName", $null, $variablesScope)
}

foreach($ndkVersion in $customNdkVersions)
{
    Write-Host "Installing NDK version '$ndkVersion' ..."
    $zipFile = "android-ndk-$ndkVersion-windows-x86_64.zip"
    $zipLocaion = Join-Path -Path $tempLocation -ChildPath $zipFile
    $variableName = "${ndkVariablePrefix}_$ndkVersion"
    $checkFileName = Join-Path -Path $ndksArchiveLocation -ChildPath "$ndkVersion.set"
 
    # Ensure archive folder exists.
    New-Item -ItemType Container -Path $ndksArchiveLocation -Force | Out-Null

    # There is no reason to use force option here as if that is specified whole $toolsFolder will be deleted including NDKs
    if (-not (Test-Path -Path $checkFileName))
    {
        # Only windows donwloads are support right now.
        $urlToDownload = "https://dl.google.com/android/repository/android-ndk-$ndkVersion-windows-x86_64.zip"
        Download -packageDownloadUrl $urlToDownload -file $zipLocaion -proxy $proxy
        Unzip -file $zipLocaion -targetDir $ndksArchiveLocation

        # Create a check file to prevent redownloading of succesfully installed version.
        Tee-Object -FilePath $checkFileName
    }
    else 
    {
        Write-Host "Skipping '$ndkVersion' download as it is already unpacked." -ForegroundColor Green
    }
    
    # Zip with NDK contains root folder in format 'android-ndk-$ndkVersion'
    $targetLocation = Join-Path -Path $ndksArchiveLocation -ChildPath "android-ndk-$ndkVersion"

    if(-not (Test-Path -Path $targetLocation))
    {
        throw "Unpacking of '$ndkVersion' failed as expected path after extraction '$targetLocation' does not exists."
    }

    Write-Verbose "Setting environment variable for '$variableName' pointing to '$targetLocation'"
    [Environment]::SetEnvironmentVariable("$variableName", "$targetLocation", $variablesScope)
    Write-Host "NDK version '$ndkVersion' installed succesfully." -ForegroundColor Green
}

Write-Host "All packages installed." -ForegroundColor Green