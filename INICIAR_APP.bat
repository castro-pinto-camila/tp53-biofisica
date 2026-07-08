@echo off
title Evaluador Biofisico TP53
cd /d "%~dp0"
echo ============================================================
echo   Iniciando la aplicacion... se abrira sola en tu navegador.
echo.
echo   NO cierres esta ventana mientras uses la app.
echo   Para apagarla: cierra esta ventana (o pulsa Ctrl + C).
echo ============================================================
echo.
py -m streamlit run app.py
echo.
echo La app se detuvo. Puedes cerrar esta ventana.
pause
