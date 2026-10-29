@echo off
title Hotspot VPN Proxy Router
cd /d "%~dp0"
echo ============================================================
echo         Hotspot VPN Proxy Server for Mobile Phone
echo ============================================================
echo.
echo Hotspot IP : 192.168.137.1
echo Proxy Port : 8080
echo.
echo Make sure on your phone's Wi-Fi settings (Advanced):
echo   Proxy: Manual
echo   Host : 192.168.137.1
echo   Port : 8080
echo.
echo Starting proxy server (keep this window open while using)...
echo ============================================================
python "%~dp0proxy_router.py"
pause
