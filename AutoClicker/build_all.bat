@echo off
echo.
echo === JAVA'SIZ CALISAN AUTOCLICKER ===
echo.

if exist "JNativeHook-2.2.2.x86_64.dll" ren "JNativeHook-2.2.2.x86_64.dll" "NativeHook-2.2.x86_64.dll"

jar cfm AutoClicker.jar manifest.txt AutoClicker.class jnativehook-2.2.2.jar NativeHook-2.2.x86_64.dll

java -jar launch4j.jar AutoClicker_Config.xml

if exist "Dağıtım" rmdir /s /q "Dağıtım"
mkdir "Dağıtım"
copy AutoClicker.exe "Dağıtım\"
copy AutoClicker.jar "Dağıtım\"
xcopy jre "Dağıtım\jre" /E /I /H /Y

echo.
echo DAGITIM HAZIR: Dagitim klasoru
echo Java olmasa da calisir!
echo Kullanici sadece EXE'ye cift tiklar!
pause