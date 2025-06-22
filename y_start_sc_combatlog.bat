@echo off
REM Starte das Griefing Counter Backend und Electron-Frontend

REM Wechsel ins Scriptverzeichnis (Projekt-Hauptordner)
cd /d %~dp0

REM Prüfe, ob Python installiert ist
where python >nul 2>nul
if errorlevel 1 (
    echo Python ist nicht installiert. Bitte installiere Python 3.x und versuche es erneut.
    pause
    exit /b
)

REM Prüfe, ob Node.js installiert ist
where node >nul 2>nul
if errorlevel 1 (
    echo Node.js ist nicht installiert. Bitte installiere Node.js und versuche es erneut.
    pause
    exit /b
)

REM Backend starten (im Hintergrund, Fehlerausgabe sichtbar)
start "" cmd /k python main.py

REM Kurze Wartezeit, damit das Backend hochfahren kann
timeout /t 3 /nobreak >nul

REM Prüfe, ob das Frontend-Verzeichnis existiert
if not exist frontend (
    echo Das Verzeichnis "frontend" wurde nicht gefunden!
    pause
    exit /b
)

REM Wechsel ins Frontend-Verzeichnis
cd frontend

REM Installiere Node-Abhängigkeiten
if exist package.json (
    npm install
) else (
    echo package.json nicht gefunden. Stelle sicher, dass du im frontend-Ordner bist.
    pause
    exit /b
)

REM Starte Electron-Frontend
npx electron .

pause
