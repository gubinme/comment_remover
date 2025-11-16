@echo off
echo ================================================
echo         Installing Dependencies
echo ================================================
echo.
echo Installing rich library...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo.
echo ================================================
echo       Installation completed successfully!
echo ================================================
pause
