@echo off
setlocal enabledelayedexpansion

net session >nul 2>&1
if %errorlevel% neq 0 exit /b

for %%P in (
    VALORANT.exe
    VALORANT-Win64-Shipping.exe
    RiotClientServices.exe
    RiotClientCrashHandler.exe
    vgc.exe
    VGAuthService.exe
    RiotClientUx.exe
) do taskkill /f /im %%P >nul 2>&1

sc stop vgc >nul 2>&1
sc stop vgk >nul 2>&1
sc delete vgc >nul 2>&1
sc delete vgk >nul 2>&1

for %%D in (
    "%PROGRAMFILES%\Riot Games\VALORANT"
    "%PROGRAMFILES%\Riot Games\Riot Client"
    "%PROGRAMFILES%\Riot Vanguard"
    "%PROGRAMFILES(X86)%\Riot Games\VALORANT"
    "%PROGRAMFILES(X86)%\Riot Games\Riot Client"
    "%PROGRAMFILES(X86)%\Riot Vanguard"
) do if exist "%%D" (
    takeown /f "%%D" /r /d y >nul 2>&1
    icacls "%%D" /grant administrators:F /t /c >nul 2>&1
    rd /s /q "%%D" >nul 2>&1
)

for %%U in (
    "%APPDATA%\VALORANT"
    "%APPDATA%\Riot Games"
    "%LOCALAPPDATA%\VALORANT"
    "%LOCALAPPDATA%\Riot Games"
    "%LOCALAPPDATA%\RiotClient"
    "%USERPROFILE%\Saved Games\VALORANT"
    "%USERPROFILE%\Documents\VALORANT"
) do if exist "%%U" (
    takeown /f "%%U" /r /d y >nul 2>&1
    icacls "%%U" /grant administrators:F /t /c >nul 2>&1
    rd /s /q "%%U" >nul 2>&1
)

for %%R in (
    "HKLM\SOFTWARE\Riot Games"
    "HKLM\SOFTWARE\WOW6432Node\Riot Games"
    "HKCU\SOFTWARE\Riot Games"
    "HKLM\SYSTEM\CurrentControlSet\Services\vgc"
    "HKLM\SYSTEM\CurrentControlSet\Services\vgk"
    "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\vgk.sys"
) do reg delete "%%R" /f >nul 2>&1

for /f "delims=" %%K in ('reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" 2^>nul ^| findstr /i "VALORANT Riot Vanguard"') do reg delete "%%K" /f >nul 2>&1
for /f "delims=" %%K in ('reg query "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall" 2^>nul ^| findstr /i "VALORANT Riot Vanguard"') do reg delete "%%K" /f >nul 2>&1

for %%S in (
    "%USERPROFILE%\Desktop\VALORANT.lnk"
    "%USERPROFILE%\Desktop\Riot Client.lnk"
    "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\VALORANT.lnk"
    "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Riot Client.lnk"
    "%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs\Riot Games"
) do if exist "%%S" (
    if "%%~xS"==".lnk" del /f /q "%%S" >nul 2>&1
    if not "%%~xS"==".lnk" rd /s /q "%%S" >nul 2>&1
)

del /f /q "%TEMP%\*VALORANT*" "%TEMP%\*Riot*" "%TEMP%\*Vanguard*" >nul 2>&1
del /f /q "%WINDIR%\Prefetch\*VALORANT*.pf" "%WINDIR%\Prefetch\*RIOT*.pf" "%WINDIR%\Prefetch\*VGC*.pf" >nul 2>&1
del /f /q "%APPDATA%\Microsoft\Windows\Recent\*VALORANT*" "%APPDATA%\Microsoft\Windows\Recent\*Riot*" >nul 2>&1

for /f "delims=" %%F in ('dir /s /b /a-d "%SystemDrive%" ^| findstr /i /r "\\VALORANT \\Riot \\Vanguard .*valorant.* .*riot.* .*vanguard.*" 2^>nul') do (
    attrib -r -s -h "%%F" >nul 2>&1
    del /f /q "%%F" >nul 2>&1
)

for /f "delims=" %%D in ('dir /s /b /ad "%SystemDrive%" ^| findstr /i /r "\\VALORANT \\Riot \\Vanguard" 2^>nul') do rd /s /q "%%D" >nul 2>&1

for %%P in ("%PROGRAMFILES%" "%PROGRAMFILES(X86)%") do if exist "%%P\Riot Games" rd /s /q "%%P\Riot Games" >nul 2>&1

pause