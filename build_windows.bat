@echo off
echo ================================================
echo   SOC Log Sanitizer - Build para Windows
echo ================================================
echo.

echo Verificando se PyInstaller esta instalado...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller nao encontrado. Instalando...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERRO: Falha ao instalar PyInstaller
        pause
        exit /b 1
    )
)

echo.
echo Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "SOC Log Sanitizer.spec" del /q "SOC Log Sanitizer.spec"

echo.
echo Gerando executavel...
echo Isso pode levar alguns minutos...
echo.

pyinstaller --onefile --windowed ^
    --name "SOC Log Sanitizer" ^
    --icon=NONE ^
    --add-data "sanitize_soc_logs.py;." ^
    --noconsole ^
    sanitizer_gui.py

if errorlevel 1 (
    echo.
    echo ERRO: Falha ao gerar executavel
    pause
    exit /b 1
)

echo.
echo ================================================
echo   Build concluido com sucesso!
echo ================================================
echo.
echo O executavel esta em: dist\SOC Log Sanitizer.exe
echo.
echo Tamanho aproximado:
dir "dist\SOC Log Sanitizer.exe" | find "SOC Log Sanitizer.exe"
echo.
echo Voce pode distribuir apenas o arquivo .exe
echo Nao precisa de Python instalado para executar!
echo.

pause
