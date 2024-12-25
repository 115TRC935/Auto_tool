@echo off
setlocal enabledelayedexpansion

:: Estableciendo el directorio de trabajo en el script actual
cd /d "%~dp0"

:: Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python no está instalado. Por favor, instale Python y asegúrese de agregarlo al PATH.
    pause
    exit /b 1
)

:: Verificar si pip está instalado
python -m ensurepip >nul 2>&1
if %errorlevel% neq 0 (
    echo Pip no está disponible. Intentando instalar pip...
    python -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo Error instalando pip. Por favor, instale pip manualmente.
        pause
        exit /b 1
    )
)

:: Actualizando pip a la última versión
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo Error actualizando pip.
    pause
    exit /b 1
)

:: Creando entorno virtual
python -m venv venv
if %errorlevel% neq 0 (
    echo Error creando entorno virtual.
    pause
    exit /b 1
)

:: Activando entorno virtual
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo Error activando entorno virtual.
    pause
    exit /b 1
)

:: Instalando dependencias
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error instalando dependencias.
    pause
    exit /b 1
)

:: Verificar si pyinstaller está instalado
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller no está instalado. Instalando PyInstaller...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo Error instalando PyInstaller.
        pause
        exit /b 1
    )
)

:: Generando ejecutable
pyinstaller --clean ^
--noconfirm ^
--onefile ^
--windowed ^
--icon="%cd%\config\brand-amigo.ico" ^
--add-data "%cd%\config\brand-amigo.ico;config" ^
--add-data "%cd%\config\colors.json;config" ^
--paths src ^
--workpath build ^
--specpath build ^
--distpath dist ^
--exclude-module pytest ^
src\AutoTool.py
if %errorlevel% neq 0 (
    echo Error generando ejecutable.
    pause
    exit /b 1
)

:: Moviendo ejecutable a la raiz
move /y dist\AutoTool.exe AutoTool.exe
if %errorlevel% neq 0 (
    echo Error moviendo ejecutable.
    pause
    exit /b 1
)

:: Limpiando archivos temporales
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
if exist src\__pycache__ rmdir /s /q src\__pycache__
if exist AutoTool.spec del /q AutoTool.spec
if exist venv rmdir /s /q venv

:: Mensaje final
echo Instalacion completada!
pause
