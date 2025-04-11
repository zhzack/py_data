@echo off
setlocal

REM Get the directory of the currently running batch file
set "SCRIPT_DIR=%~dp0"

REM Check if the user provided the binary file name
if "%~1"=="" (
    echo No file name provided. Opening file selection dialog...
    
    REM Use PowerShell to open file selection dialog and get the selected file path
    for /f "usebackq delims=" %%i in (`powershell -Command "Add-Type -AssemblyName System.Windows.Forms; $f = New-Object System.Windows.Forms.OpenFileDialog; $f.InitialDirectory = '%SCRIPT_DIR%'; $f.Filter = 'Binary Files (*.bin)|*.bin|All Files (*.*)|*.*'; if ($f.ShowDialog() -eq 'OK') { $f.FileName }"`) do (
        set "BINARY_FILE=%%i"
    )
) else (
    set "BINARY_FILE=%~1"
)

REM Check if a file was selected or provided
if "%BINARY_FILE%"=="" (
    echo No file selected.
    exit /b 1
)

REM Set the binary file path
set "BINARY_PATH=%BINARY_FILE%"

REM Check if the binary file exists
if not exist "%BINARY_PATH%" (
    echo Binary file "%BINARY_PATH%" does not exist.
    exit /b 1
)

REM Set the path to J-Link tools
REM set "JLINK_PATH=C:\Program Files (x86)\SEGGER\JLink"

REM Create a JLink script file
set "JLINK_SCRIPT=jlink_script.jlink"
echo device NRF52840_XXAA > %JLINK_SCRIPT%
echo si swd >> %JLINK_SCRIPT%
echo speed 4000 >> %JLINK_SCRIPT%
echo jtagconf -1,-1 >> %JLINK_SCRIPT%
echo connect >> %JLINK_SCRIPT%
echo h >> %JLINK_SCRIPT%
echo sleep 50 >> %JLINK_SCRIPT%
echo loadbin %BINARY_PATH%, 0x00000000, reset >> %JLINK_SCRIPT%
echo sleep 50 >> %JLINK_SCRIPT%
echo r >> %JLINK_SCRIPT%
echo h >> %JLINK_SCRIPT%
echo g >> %JLINK_SCRIPT%
echo q >> %JLINK_SCRIPT%

REM Execute the JLink command
REM "%JLINK_PATH%\JLink.exe" -CommanderScript %JLINK_SCRIPT%
"JLink.exe" -CommanderScript %JLINK_SCRIPT%

REM Clean up the script file
del %JLINK_SCRIPT%

REM Check the result of the JLink command
if %errorlevel% neq 0 (
    echo Failed to flash the binary file.
    pause /b %errorlevel%
REM    exit /b %errorlevel%
)

echo Flashing completed successfully.
endlocal
pause
