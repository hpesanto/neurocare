@echo off
REM Script para fazer push de todas as alterações locais

echo.
echo ======================================================================
echo.
echo Fazendo push de alteracoes locais para repositorio remoto...
echo.
echo ======================================================================
echo.

REM Executar o script Python
python push_changes.py

if %errorlevel% neq 0 (
    echo.
    echo ======================================================================
    echo.
    echo ERRO: Falha ao fazer push das alteracoes!
    echo.
    echo ======================================================================
    echo.
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo.
echo OK - Push realizado com sucesso!
echo.
echo Acesse seu repositorio remoto para criar uma Pull Request.
echo.
echo ======================================================================
echo.
pause
