def main():

"""
Star Citizen Griefing Counter REST-API Backend (FastAPI)
- Endpunkte für Statistiken, Filter, Leaderboards, Events
- Bereit für Electron/Web-Frontend
"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional
from analytics import stats
from core.filter_service import FilterService
import uvicorn

app = FastAPI(title="SC Griefing Counter API")

# CORS für lokale Electron/Web-Entwicklung erlauben
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/stats")
def get_stats(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    players: Optional[bool] = True,
    unknown: Optional[bool] = True,
    npc_pilot: Optional[bool] = True,
    npc_civilian: Optional[bool] = True,
    npc_worker: Optional[bool] = True,
    npc_lawenforcement: Optional[bool] = True,
    npc_gunner: Optional[bool] = True,
    npc_technical: Optional[bool] = True,
    npc_test: Optional[bool] = True,
    npc_pirate: Optional[bool] = True,
    npc_ground: Optional[bool] = True,
    npc_animal: Optional[bool] = True,
    npc_uncategorized: Optional[bool] = True,
):
    filter_dict = {
        "players": players,
        "unknown": unknown,
        "npc_pilot": npc_pilot,
        "npc_civilian": npc_civilian,
        "npc_worker": npc_worker,
        "npc_lawenforcement": npc_lawenforcement,
        "npc_gunner": npc_gunner,
        "npc_technical": npc_technical,
        "npc_test": npc_test,
        "npc_pirate": npc_pirate,
        "npc_ground": npc_ground,
        "npc_animal": npc_animal,
        "npc_uncategorized": npc_uncategorized,
    }
    s_date = FilterService.validate_date(start_date) if start_date else None
    e_date = FilterService.validate_date(end_date) if end_date else None
    # Caching-Parameter vorbereiten
    s_date_str = s_date.strftime("%Y-%m-%d") if s_date else None
    e_date_str = e_date.strftime("%Y-%m-%d") if e_date else None
    filter_tuple = tuple(sorted(filter_dict.items())) if filter_dict else None
    stats_text, recent_text = stats.get_stats_cached(s_date_str, e_date_str, filter_tuple)
    return {"stats": stats_text, "recent": recent_text}

@app.get("/api/leaderboards")
def get_leaderboards(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    players: Optional[bool] = True,
    unknown: Optional[bool] = True,
    npc_pilot: Optional[bool] = True,
    npc_civilian: Optional[bool] = True,
    npc_worker: Optional[bool] = True,
    npc_lawenforcement: Optional[bool] = True,
    npc_gunner: Optional[bool] = True,
    npc_technical: Optional[bool] = True,
    npc_test: Optional[bool] = True,
    npc_pirate: Optional[bool] = True,
    npc_ground: Optional[bool] = True,
    npc_animal: Optional[bool] = True,
    npc_uncategorized: Optional[bool] = True,
):
    filter_dict = {
        "players": players,
        "unknown": unknown,
        "npc_pilot": npc_pilot,
        "npc_civilian": npc_civilian,
        "npc_worker": npc_worker,
        "npc_lawenforcement": npc_lawenforcement,
        "npc_gunner": npc_gunner,
        "npc_technical": npc_technical,
        "npc_test": npc_test,
        "npc_pirate": npc_pirate,
        "npc_ground": npc_ground,
        "npc_animal": npc_animal,
        "npc_uncategorized": npc_uncategorized,
    }
    s_date = FilterService.validate_date(start_date) if start_date else None
    e_date = FilterService.validate_date(end_date) if end_date else None
    s_date_str = s_date.strftime("%Y-%m-%d") if s_date else None
    e_date_str = e_date.strftime("%Y-%m-%d") if e_date else None
    filter_tuple = tuple(sorted(filter_dict.items())) if filter_dict else None
    kill_lb, death_lb = stats.get_leaderboards_cached(s_date_str, e_date_str, filter_tuple)
    return {"kill_leaderboard": kill_lb, "death_leaderboard": death_lb}

@app.get("/api/events")
def get_events(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    players: Optional[bool] = True,
    unknown: Optional[bool] = True,
    npc_pilot: Optional[bool] = True,
    npc_civilian: Optional[bool] = True,
    npc_worker: Optional[bool] = True,
    npc_lawenforcement: Optional[bool] = True,
    npc_gunner: Optional[bool] = True,
    npc_technical: Optional[bool] = True,
    npc_test: Optional[bool] = True,
    npc_pirate: Optional[bool] = True,
    npc_ground: Optional[bool] = True,
    npc_animal: Optional[bool] = True,
    npc_uncategorized: Optional[bool] = True,
):
    filter_dict = {
        "players": players,
        "unknown": unknown,
        "npc_pilot": npc_pilot,
        "npc_civilian": npc_civilian,
        "npc_worker": npc_worker,
        "npc_lawenforcement": npc_lawenforcement,
        "npc_gunner": npc_gunner,
        "npc_technical": npc_technical,
        "npc_test": npc_test,
        "npc_pirate": npc_pirate,
        "npc_ground": npc_ground,
        "npc_animal": npc_animal,
        "npc_uncategorized": npc_uncategorized,
    }
    s_date = FilterService.validate_date(start_date) if start_date else None
    e_date = FilterService.validate_date(end_date) if end_date else None
    recent_text = stats.get_recent_kill_events(s_date, e_date, filter_dict)
    return {"recent": recent_text}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

# --- Zusätzliche API-Endpunkte für Electron-Frontend ---
import os
import sqlite3
from fastapi.responses import JSONResponse
from core import config as core_config

@app.get("/api/log_status")
def get_log_status():
    """
    Gibt den Fortschritt des Log-Imports zurück (imported, total).
    """
    # Beispielhafte Implementierung: Zähle Logdateien im Log-Ordner und importierte Einträge in der DB
    log_dir = core_config.get_config_value("log_dir", fallback="logs")
    try:
        total = len([f for f in os.listdir(log_dir) if f.endswith(".log")])
    except Exception:
        total = 0
    # Importierte Logs aus der DB zählen (angenommen Tabelle 'imported_logs' existiert)
    db_path = core_config.get_config_value("db_path", fallback="data/dev_placeholder.db")
    imported = 0
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM imported_logs")
        imported = cur.fetchone()[0]
        conn.close()
    except Exception:
        imported = 0
    return {"imported": imported, "total": total}

@app.get("/api/db_size")
def get_db_size():
    """
    Gibt die aktuelle Datenbankgröße in KB zurück.
    """
    db_path = core_config.get_config_value("db_path", fallback="data/dev_placeholder.db")
    try:
        size = os.path.getsize(db_path) // 1024
    except Exception:
        size = 0
    return {"db_size_kb": size}

@app.get("/api/update_check")
def update_check():
    """
    Dummy-Update-Check: Gibt zurück, ob eine neue Version verfügbar ist.
    """
    # In echt: Version online prüfen, hier Dummy
    current_version = "1.0.0"
    latest_version = "1.0.0"  # Simuliere: Keine neue Version
    update_available = current_version != latest_version
    return {"current_version": current_version, "latest_version": latest_version, "update_available": update_available}

@app.post("/api/clear_appdata")
def clear_appdata():
    """
    Dummy-Endpoint: Löscht AppData-Verzeichnis (Platzhalter, in echt über Electron-API).
    """
    # Hier nur Dummy, da Electron das besser kann
    return JSONResponse(content={"status": "ok", "message": "AppData gelöscht (Dummy)"})
