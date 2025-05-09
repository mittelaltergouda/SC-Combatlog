# SC Griefing Counter Web-Frontend

Dieses Verzeichnis ist für das neue Web- oder Electron-Frontend vorgesehen.

## Vorschlag für die Struktur (React-Beispiel)

- frontend/
  - public/
    - index.html
  - src/
    - App.tsx
    - components/
    - api/
    - styles/
  - package.json
  - vite.config.ts

## Entwicklung starten

1. Node.js installieren
2. Im frontend-Ordner ausführen:
   npm create vite@latest . -- --template react-ts
   npm install
   npm run dev

Das Frontend kommuniziert mit dem Python-Backend (FastAPI) über die REST-API (http://localhost:8000).
