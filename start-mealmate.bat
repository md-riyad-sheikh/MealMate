@echo off
title MealMate Launcher

cd /d "C:\Users\nrnay\Documents\MealMate\MealMate-Full-Website"

echo ==========================================
echo          Starting MealMate...
echo ==========================================
echo.

echo Checking database setup...
py manage.py setup_mealmate

if errorlevel 1 (
    echo.
    echo Database setup failed.
    echo Please check the error above.
    pause
    exit /b
)

echo.
echo Checking Django project...
py manage.py check

if errorlevel 1 (
    echo.
    echo Django check failed.
    echo Please check the error above.
    pause
    exit /b
)

echo.
echo Starting Django server...
echo.

start "MealMate Django Server" cmd /k "cd /d C:\Users\nrnay\Documents\MealMate\MealMate-Full-Website && py manage.py runserver"

timeout /t 3 /nobreak >nul

start "" "http://127.0.0.1:8000/"

exit