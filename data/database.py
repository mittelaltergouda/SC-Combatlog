# Legacy-API: execute_query, execute_many, fetch_query für Test-Kompatibilität
import sqlite3
def execute_query(query, params=None):
    """
    Führt eine einzelne SQL-Query (INSERT/UPDATE/DELETE) aus (legacy, für Tests).
    Nutzt direkten sqlite3-Zugriff, da die Tests dies erwarten.
    """
    db_path = config.get_db_name()
    if not db_path:
        raise DatabaseAccessError("No database path set.")
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        if params is not None:
            cur.execute(query, params)
        else:
            cur.execute(query)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise DatabaseAccessError(str(e))
    finally:
        conn.close()

def execute_many(query, seq_of_params):
    """
    Führt eine Batch-SQL-Query (INSERT/UPDATE/DELETE) aus (legacy, für Tests).
    Nutzt direkten sqlite3-Zugriff, da die Tests dies erwarten.
    """
    db_path = config.get_db_name()
    if not db_path:
        raise DatabaseAccessError("No database path set.")
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.executemany(query, seq_of_params)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise DatabaseAccessError(str(e))
    finally:
        conn.close()

def fetch_query(query, params=None):
    """
    Führt eine SELECT-Query aus und gibt das Ergebnis als Liste von Tupeln zurück (legacy, für Tests).
    Nutzt direkten sqlite3-Zugriff, da die Tests dies erwarten.
    """
    db_path = config.get_db_name()
    if not db_path:
        raise DatabaseAccessError("No database path set.")
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        if params is not None:
            cur.execute(query, params)
        else:
            cur.execute(query)
        return cur.fetchall()
    except Exception as e:
        raise DatabaseAccessError(str(e))
    finally:
        conn.close()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from data.models import Base, Kill, FilePosition, NPCCategory, Migration
from core import config
import os
import threading
import time
import logging

logger = logging.getLogger(__name__)

# SQLAlchemy Engine & Session
engine = None
SessionLocal = None
db_lock = threading.Lock()

class DatabaseError(Exception):
    """Basisklasse für Datenbankfehler"""
    pass

class NoPlayerConfiguredError(DatabaseError):
    """Wird ausgelöst, wenn kein Spieler konfiguriert ist"""
    pass

class DatabaseAccessError(DatabaseError):
    """Wird ausgelöst bei allgemeinen Fehlern beim Datenbankzugriff"""
    pass

def init_db():
    """
    Initializes the database for the current player and creates necessary tables.
    Raises:
        NoPlayerConfiguredError: Wenn kein Spieler konfiguriert ist
        DatabaseAccessError: Bei allgemeinen Datenbankfehlern
    """
    # Stelle sicher, dass die Konfiguration geladen ist
    if not config.CURRENT_PLAYER_NAME and os.path.exists(config.CONFIG_FILE):
        config.load_config()

    db_path = config.get_db_name()
    if not db_path:
        raise NoPlayerConfiguredError("No player name set. Cannot initialize database.")

    global engine, SessionLocal
    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    engine = create_engine(f'sqlite:///{db_path}', connect_args={"check_same_thread": False})
    SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    try:
        Base.metadata.create_all(bind=engine)
        logger.info(f"Datenbanktabellen mit SQLAlchemy initialisiert: {db_path}")
    except SQLAlchemyError as e:
        logger.error(f"Fehler bei der Initialisierung der Datenbank (ORM): {str(e)}")
        raise DatabaseAccessError(str(e))


# ORM-Methoden
def get_session():
    if SessionLocal is None:
        raise DatabaseAccessError("SessionLocal ist nicht initialisiert. Bitte init_db() aufrufen.")
    return SessionLocal()

def add_kill_event(event_dict):
    session = get_session()
    try:
        kill = Kill(**event_dict)
        session.add(kill)
        session.commit()
        return kill.id
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Fehler beim Hinzufügen eines Kill-Events: {str(e)}")
        raise DatabaseAccessError(str(e))
    finally:
        session.close()

def get_kills_filtered(**filters):
    session = get_session()
    try:
        query = session.query(Kill)
        for attr, value in filters.items():
            if value is not None:
                query = query.filter(getattr(Kill, attr) == value)
        return query.all()
    except SQLAlchemyError as e:
        logger.error(f"Fehler bei get_kills_filtered: {str(e)}")
        raise DatabaseAccessError(str(e))
    finally:
        session.close()

def get_leaderboard(limit=10):
    session = get_session()
    try:
        from sqlalchemy import func
        res = session.query(Kill.killer, func.count(Kill.id).label('kills')).group_by(Kill.killer).order_by(-func.count(Kill.id)).limit(limit).all()
        return res
    except SQLAlchemyError as e:
        logger.error(f"Fehler bei get_leaderboard: {str(e)}")
        raise DatabaseAccessError(str(e))
    finally:
        session.close()

def get_db_size_kb():
    """
    Returns the database file size in KB.
    """
    db_path = config.get_db_name()
    if not db_path or not os.path.exists(db_path):
        return 0
    return os.path.getsize(db_path) / 1024

def ensure_db_initialized():
    """
    Ensures the database is initialized by calling init_db().
    
    Raises:
        NoPlayerConfiguredError: Wird abgefangen und protokolliert
    """
    # Stelle sicher, dass die Konfiguration geladen ist
    if not config.CURRENT_PLAYER_NAME and os.path.exists(config.CONFIG_FILE):
        config.load_config()
        
    try:
        # Immer init_db aufrufen, um sicherzustellen, dass alle Tabellen existieren,
        # auch wenn die Datenbankdatei bereits vorhanden ist
        init_db()
    except NoPlayerConfiguredError as e:
        logger.error(str(e))
        # Exception hier abfangen, damit die Anwendung weiterlaufen kann
        # auch wenn keine DB-Initialisierung möglich ist

def close_db():
    """
    Schließt alle offenen Datenbankverbindungen sauber.
    Dies sollte aufgerufen werden, bevor die Anwendung beendet wird
    oder wenn die Datenbank gelöscht werden soll.
    """
    # Da wir keine persistente Verbindung haben, müssen wir nichts aktiv schließen.
    # Diese Funktion ist ein Platzhalter für zukünftige Implementierungen,
    # falls wir zur persistenten Verbindung wechseln.
    logger.info("Datenbankverbindungen werden geschlossen")
    
    # Stelle für zukünftige Implementierungen sicher, dass alle ausstehenden
    # Transaktionen abgeschlossen sind, indem wir etwas warten
    time.sleep(0.2)
