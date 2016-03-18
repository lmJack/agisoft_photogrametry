@ECHO OFF 

set AssetsPath = %1
echo AssetsPath: %AssetsPath%


set num=1

:checkexist
IF NOT EXIST %AssetsPath%\output\model.obj (
ECHO Checking: %AssetsPath%\output\model.obj
ECHO File not found will check again in 10 minutes. File checked %num% time.
TIMEOUT /t 600 /nobreak
set /a num+=1
GOTO checkexist
) ELSE (
GOTO modelexist
)

:modelexist
ECHO Maya Scene file will be created in 30 seconds
"C:\Program Files\Autodesk\Maya2014\bin\mayapy.exe" "SceneCreate.py"
ECHO Maya Scene Complete
EXIT /b