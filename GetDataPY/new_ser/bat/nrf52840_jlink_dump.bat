@echo off
REM Get the directory of the current batch file
set SCRIPT_DIR=%~dp0
REM Remove the trailing backslash
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

REM Create a temporary J-Link script file
set TEMP_JLINK_SCRIPT=%SCRIPT_DIR%\temp_dump.jlink

echo device NRF52840_XXAA > %TEMP_JLINK_SCRIPT%
echo si swd >> %TEMP_JLINK_SCRIPT%
echo speed 4000 >> %TEMP_JLINK_SCRIPT%
echo jtagconf -1,-1 >> %TEMP_JLINK_SCRIPT%
echo connect >> %TEMP_JLINK_SCRIPT%
echo r >> %TEMP_JLINK_SCRIPT%
echo h >> %TEMP_JLINK_SCRIPT%
REM 352Kbytes internal flash = 1024kbytes = 0x100000 bytes
echo savebin %SCRIPT_DIR%\nrf52840_firmware_dump.bin, 0x00000000, 0x100000 >> %TEMP_JLINK_SCRIPT%
echo r >> %TEMP_JLINK_SCRIPT%
echo g >> %TEMP_JLINK_SCRIPT%
echo exit >> %TEMP_JLINK_SCRIPT%

REM Call J-Link Commander and execute the temporary script
JLink.exe -CommanderScript %TEMP_JLINK_SCRIPT%

REM Delete the temporary script file
del %TEMP_JLINK_SCRIPT%

pause