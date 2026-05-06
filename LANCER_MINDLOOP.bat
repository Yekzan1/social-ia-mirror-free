@echo off
title MindLoop Pro V5.0 - Premium Social Network
echo ==========================================
echo    🌀 INITIALISATION DE MINDLOOP PRO 🌀
echo ==========================================
echo.
cd /d "%~dp0"
echo [1/2] Verification des dependances...
pip install -r requirements.txt
echo.
echo [2/2] Lancement de MindLoop...
streamlit run main.py
pause
