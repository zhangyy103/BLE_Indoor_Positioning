@echo off

setlocal enableextensions enabledelayedexpansion

@echo Executing:  %~fn0

set PYTHON3=D:\env\python\ti_rtls
set PIP3=D:\env\python\ti_rtls\Scripts\pip

set RTLS_AGENT_DIR=%~dp0
set RTLS_DIR=%RTLS_AGENT_DIR%\rtls
set RTLS_UTIL_DIR=%RTLS_AGENT_DIR%\rtls_util
set UNPI_DIR=%RTLS_AGENT_DIR%\unpi

:LOOP
IF "%1"=="" GOTO EOF
GOTO %1


:-c
@echo "CLEAN"

@pushd %RTLS_DIR%

@echo.
@echo ==================================================
@echo               Removing dist and build
@echo ==================================================
rmdir /S /Q dist
rmdir /S /Q build
for /d %%G in ("%RTLS_DIR%\ti_simplelink*") do rd /S /Q "%%G"

@popd


@pushd %RTLS_UTIL_DIR%

@echo.
@echo ==================================================
@echo               Removing dist and build
@echo ==================================================
rmdir /S /Q dist
rmdir /S /Q build
for /d %%G in ("%RTLS_UTIL_DIR%\ti_simplelink*") do rd /S /Q "%%G"

@popd

@pushd %UNPI_DIR%

@echo.
@echo ==================================================
@echo               Removing dist and build
@echo ==================================================
rmdir /S /Q dist
rmdir /S /Q build
for /d %%G in ("%UNPI_DIR%\ti_simplelink*") do rd /S /Q "%%G"

@popd

SHIFT
GOTO LOOP


:-b
@echo "BUILD"

@pushd %RTLS_DIR%

@echo.
@echo ==================================================
@echo              Build rtls package
@echo ==================================================

%PYTHON3% setup.py sdist bdist_egg

@popd

@pushd %RTLS_UTIL_DIR%

@echo.
@echo ==================================================
@echo              Build rtls_util package
@echo ==================================================

%PYTHON3% setup.py sdist bdist_egg

@popd

@pushd %UNPI_DIR%

@echo.
@echo ==================================================
@echo              Build unpi package
@echo ==================================================

%PYTHON3% setup.py sdist bdist_egg

@popd

SHIFT
GOTO LOOP

:-i
@echo "INSTALL"

@echo.
@echo ==================================================
@echo            Installing unpi package
@echo ==================================================

%PIP3% install %UNPI_DIR%\dist\ti-simplelink-unpi-0.2.tar.gz

@echo.
@echo ==================================================
@echo            Installing rtls package
@echo ==================================================

%PIP3% install %RTLS_DIR%\dist\ti-simplelink-rtls-0.2.tar.gz

@echo.
@echo ==================================================
@echo            Installing rtls-util package
@echo ==================================================

%PIP3% install %RTLS_UTIL_DIR%\dist\ti-simplelink-rtls-util-0.2.tar.gz

SHIFT
GOTO LOOP


:-u
@echo "UNINSTALL"

@echo.
@echo ==================================================
@echo            Uninstalling rtls-util package
@echo ==================================================

%PIP3% uninstall -y ti-simplelink-rtls-util

@echo.
@echo ==================================================
@echo            Uninstalling rtls package
@echo ==================================================

%PIP3% uninstall -y ti-simplelink-rtls

@echo.
@echo ==================================================
@echo            Uninstalling unpi package
@echo ==================================================

%PIP3% uninstall -y ti-simplelink-unpi

SHIFT
GOTO LOOP

:-h

@echo.
@echo package.bat [-h HELP] [-c CLEAN] [-b BUILD] [-i INSTALL] [-u UNINSTALL]
@echo.
@echo Description:
@echo       This script is used to basic action on python packages such as clean / build / install / uninstall
@echo.
@echo Parameter List:
@echo       -c      Clean packages folder from "build" / "dist" / "*.egg-info"
@echo       -b      Build packages
@echo       -i      Install packages from "dist" folder using pip command
@echo       -u      Uninstall packages using pip command
@echo       -h      Help
@echo.
@echo Examples:
@echo       package.bat -h              For Help
@echo       package.bat -c -b           For clean and build packages
@echo       package.bat -u -i           For uninstall old packages and install new packages
@echo       package.bat -c -b -u -i     For whole process

:EOF
@echo on
