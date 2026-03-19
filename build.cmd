@echo off
echo ======================================================
echo   CONFIANZA23 - Generador SIFAS Naval - BUILD
echo ======================================================
echo.
echo [1/2] Instalando/Actualizando dependencias...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Hubo un problema instalando las dependencias.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/2] Lanzando aplicacion Streamlit...
streamlit run app.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] No se pudo iniciar Streamlit.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Proceso finalizado.
pause
