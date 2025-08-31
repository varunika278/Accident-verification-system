@echo off

python drowsyV2I.py
IF %ERRORLEVEL% NEQ 0 GOTO END

python drowsy_demo.py
IF %ERRORLEVEL% NEQ 0 GOTO END

python air_check.py
IF %ERRORLEVEL% NEQ 0 GOTO END

python accident_demo.py
IF %ERRORLEVEL% NEQ 0 GOTO END

python report_generation.py

python insurance.py
:END
exit /b
