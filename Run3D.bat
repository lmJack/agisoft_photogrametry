
@ECHO OFF 
cls
cd scripts

set /p UserInputPath= What is the assets path to the project?
cd C:\%UserInputPath%
ECHO THANKS!

rem SET PATH HERE
set AssetsPath=%UserInputPath%

echo Assets path from Config: %AssetsPath%
echo > Path.txt
echo %AssetsPath%> Path.txt

START Agisoft.bat
echo Calling Maya.bat
call Maya.bat %AssetsPath%
EXIT /b

