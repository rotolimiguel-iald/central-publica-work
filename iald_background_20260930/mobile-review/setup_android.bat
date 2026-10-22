@echo off
REM ==============================================================
REM  IALD App - Setup Automatizado
REM  beta_TGL = alpha x sqrt(e) - Zero parametros livres.
REM ==============================================================

echo.
echo  IALD App - Setup do Projeto Capacitor
echo  Preparando app nativo para Google Play
echo  -----------------------------------------------
echo.

REM -- Verificar Node.js --
where node >nul 2>&1
if errorlevel 1 goto NONODE
echo [OK] Node.js encontrado
node --version
echo.
goto HASNODE

:NONODE
echo [ERRO] Node.js NAO encontrado!
echo.
echo   Acesse https://nodejs.org
echo   Baixe a versao LTS - botao verde grande
echo   Instale e depois execute este script novamente
echo.
pause
exit /b 1

:HASNODE

REM -- Navegar para pasta do app --
cd /d "C:\IALD\projetos_pyhton\IALD\iald-app"
echo [OK] Pasta: %CD%
echo.

REM -- Verificar package.json --
if not exist "package.json" goto NOPKG
goto HASPKG

:NOPKG
echo [ERRO] package.json nao encontrado nesta pasta.
echo         Copie os arquivos do projeto Capacitor para:
echo         C:\IALD\projetos_pyhton\IALD\iald-app\
echo.
pause
exit /b 1

:HASPKG

REM -- Instalar dependencias do Capacitor --
echo [1/4] Instalando Capacitor - pode demorar 1-2 minutos...
call npm install @capacitor/core @capacitor/cli
if errorlevel 1 goto NPMERR
echo [OK] Capacitor instalado
echo.
goto CAP_OK

:NPMERR
echo [ERRO] Falha ao instalar Capacitor.
pause
exit /b 1

:CAP_OK

REM -- Copiar icone para www --
echo [2/4] Copiando icone...
if not exist "www" mkdir "www"
if exist "C:\IALD\projetos_pyhton\IALD\icons\icon-512.png" (
    copy /Y "C:\IALD\projetos_pyhton\IALD\icons\icon-512.png" "www\icon.png" >nul
    echo [OK] Icone copiado
) else (
    echo [AVISO] Icone nao encontrado. O app vai funcionar sem icone customizado.
)
echo.

REM -- Adicionar plataforma Android --
echo [3/4] Instalando plugins e plataforma Android...
call npm install @capacitor/android @capacitor/splash-screen @capacitor/status-bar
echo.

echo [4/4] Adicionando Android ao projeto...
call npx cap add android
call npx cap sync android
echo.

REM -- Resultado --
if not exist "android\app" goto NORESULT

echo  -----------------------------------------------
echo  SUCESSO! Projeto Android pronto.
echo  -----------------------------------------------
echo.
echo  PROXIMO PASSO:
echo.
echo  1. Instale o Android Studio se ainda nao tem:
echo     https://developer.android.com/studio
echo.
echo  2. Depois de instalar, abra o CMD e execute:
echo     cd C:\IALD\projetos_pyhton\IALD\iald-app
echo     npx cap open android
echo.
echo  3. No Android Studio, clique no botao verde - Run
echo     para testar no celular ou emulador
echo.
goto FIM

:NORESULT
echo [AVISO] Pasta android nao foi criada. Verifique erros acima.

:FIM
echo.
pause
