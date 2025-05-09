import os
import re
from core import config
import logging
from datetime import datetime

# Stelle sicher, dass die Konfiguration vor allem anderen geladen wird
if not config.CURRENT_PLAYER_NAME and os.path.exists(config.CONFIG_FILE):
    config.load_config()

# Erst NACH dem Laden der Konfiguration weitere Module importieren
from data import database
from log_processing import npc_handler

# Initialisiere den Logger korrekt
logger = logging.getLogger(__name__)

# Stelle sicher, dass die Datenbank initialisiert ist
try:
    database.ensure_db_initialized()
except Exception as e:
    logger.error(f"Fehler bei der DB-Initialisierung: {str(e)}")

ACTOR_DEATH_REGEX = re.compile(
    r"^<(?P<timestamp>[^>]+)>.*?<Actor Death>.*?'(?P<killed_player>[^']+)' \[\d+\].*?"
    r"in zone '(?P<zone>[^']+)'"
    r".*?killed by '(?P<killer>[^']+)' \[\d+\].*?using '(?P<weapon>[^']+)' \[Class (?P<class>[^]]+)\].*?"
    r"with damage type '(?P<damage_type>[^']+)'",
    re.IGNORECASE
)

def parse_log_line(line):
    """Parses a single log line using ACTOR_DEATH_REGEX, returns dict if matched."""
    match = ACTOR_DEATH_REGEX.match(line)
    if match:
        return match.groupdict()
    return None

def process_log_file(file_path):
    """Reads new lines from file_path, extracts kill events for the current player, saves to DB."""
    if not os.path.exists(file_path):
        logger.warning(f"Log-Datei existiert nicht: {file_path}")
        return

    # Log start
    logger.info(f"Starting to read log: {file_path}")

    try:
        from data.models import Kill, FilePosition
        session = database.get_session()
        offset_obj = session.query(FilePosition).filter_by(file_path=file_path).first()
        offset = offset_obj.last_offset if offset_obj else 0

        new_events = []
        player = config.CURRENT_PLAYER_NAME.strip().lower() if config.CURRENT_PLAYER_NAME else ""
        if not player:
            logger.warning("Kein Spielername konfiguriert, überspringe Log-Verarbeitung")
            session.close()
            return

        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            f.seek(offset)
            for line in f:
                event = parse_log_line(line.strip())
                if event:
                    killer = event["killer"].strip().lower()
                    victim = event["killed_player"].strip().lower()
                    # Only store events where the current player is killer or victim
                    if killer == player or victim == player:
                        logger.debug(f"Kill-Event gefunden: {victim} getötet von {killer} in {event['zone']}")
                        # Auto-categorize NPCs - erweitert um weitere NPC-Präfixe
                        for key in ("killed_player", "killer"):
                            val = event[key].strip().lower()
                            if val.startswith(("pu_", "vlk_", "kopion_", "quasigrazer_")):
                                try:
                                    npc_handler.save_npc_category(val, "uncategorized")
                                except Exception as e:
                                    logger.error(f"Fehler bei NPC-Kategorisierung: {str(e)}")

                        new_events.append(Kill(
                            timestamp=event["timestamp"],
                            killed_player=event["killed_player"],
                            killer=event["killer"],
                            zone=event["zone"],
                            weapon=event["weapon"],
                            damage_class=event["class"],
                            damage_type=event["damage_type"]
                        ))

        if new_events:
            try:
                session.add_all(new_events)
                session.commit()
                logger.info(f"Stored {len(new_events)} new events from {file_path}")
            except Exception as e:
                session.rollback()
                logger.error(f"Fehler beim Speichern von Ereignissen: {str(e)}")
                # Tabellen neu initialisieren und erneut versuchen
                try:
                    database.init_db()
                    session.add_all(new_events)
                    session.commit()
                    logger.info(f"Nach Neuinitialisierung: {len(new_events)} Ereignisse gespeichert")
                except Exception as retry_error:
                    session.rollback()
                    logger.error(f"Speichern nach Neuinitialisierung fehlgeschlagen: {str(retry_error)}")
                    session.close()
                    return  # Beenden, wenn auch nach Neuinitialisierung ein Fehler auftritt

        new_offset = os.path.getsize(file_path)
        try:
            file_pos = session.query(FilePosition).filter_by(file_path=file_path).first()
            if file_pos:
                file_pos.last_offset = new_offset
            else:
                file_pos = FilePosition(file_path=file_path, last_offset=new_offset)
                session.add(file_pos)
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Fehler beim Aktualisieren der Dateiposition: {str(e)}")
            # Tabellen neu initialisieren und erneut versuchen
            try:
                database.init_db()
                file_pos = session.query(FilePosition).filter_by(file_path=file_path).first()
                if file_pos:
                    file_pos.last_offset = new_offset
                else:
                    file_pos = FilePosition(file_path=file_path, last_offset=new_offset)
                    session.add(file_pos)
                session.commit()
            except Exception as retry_error:
                session.rollback()
                logger.error(f"Positionsaktualisierung nach Neuinitialisierung fehlgeschlagen: {str(retry_error)}")
        session.close()
    except Exception as e:
        logger.error(f"Allgemeiner Fehler bei der Verarbeitung von {file_path}: {str(e)}", exc_info=True)
        # Stellen Sie sicher, dass die Datenbank in einem konsistenten Zustand ist
        try:
            database.init_db()
        except Exception as db_error:
            logger.error(f"Datenbank-Neuinitialisierung nach Fehler fehlgeschlagen: {str(db_error)}")

    # Log finish
    logger.info(f"Finished reading log: {file_path}")

def parse_all_backup_logs():
    """Reads all backup logs once, so only new lines are processed for each."""
    if not os.path.isdir(config.BACKUP_FOLDER):
        logger.warning(f"Backup-Ordner existiert nicht: {config.BACKUP_FOLDER}")
        return
        
    logs = [f for f in os.listdir(config.BACKUP_FOLDER) if f.lower().endswith(".log")]
    logs.sort()
    
    logger.info(f"Parsing {len(logs)} backup logs from {config.BACKUP_FOLDER}")
    
    for lf in logs:
        full_path = os.path.join(config.BACKUP_FOLDER, lf)
        try:
            process_log_file(full_path)
        except Exception as e:
            logger.error(f"Fehler beim Verarbeiten von Backup-Log {lf}: {str(e)}")
            # Fahre mit dem nächsten Log fort, auch wenn dieses fehlschlägt

def get_backup_log_progress():
    """
    Returns a tuple (imported, total) representing how many backup logs
    have been processed (offset > 0) and total log files in BACKUP_FOLDER.
    """
    if not os.path.isdir(config.BACKUP_FOLDER):
        logger.warning(f"Backup-Ordner existiert nicht: {config.BACKUP_FOLDER}")
        return (0, 0)
        
    logs = [f for f in os.listdir(config.BACKUP_FOLDER) if f.lower().endswith(".log")]
    total = len(logs)
    imported = 0
    
    try:
        from data.models import FilePosition
        session = database.get_session()
        for lf in logs:
            full_path = os.path.join(config.BACKUP_FOLDER, lf)
            file_pos = session.query(FilePosition).filter_by(file_path=full_path).first()
            if file_pos and file_pos.last_offset and file_pos.last_offset > 0:
                imported += 1
        session.close()
    except Exception as e:
        logger.error(f"Fehler beim Abrufen des Backup-Log-Fortschritts: {str(e)}")
    return imported, total
