"""
DatabaseService: Kapselt alle Datenbankzugriffe für die GUI und spätere REST-API.
Ermöglicht einfaches Mocking und Testen.
"""
from data import database
from core import config

class DatabaseService:
    @staticmethod
    def init_db():
        return database.init_db()

    @staticmethod
    def close_db():
        return database.close_db()

    @staticmethod
    def get_db_size_kb():
        return database.get_db_size_kb()

    @staticmethod
    def reset_appdata():
        # Löscht alle Datenbanken und Logs (wie in on_clear_appdata)
        import os
        import logging
        logger = logging.getLogger(__name__)
        try:
            DatabaseService.close_db()
            # Lösche Logs
            if os.path.exists(config.LOG_FOLDER):
                logger.info(f"Lösche Logs in: {config.LOG_FOLDER}")
                for subfolder in [config.ERROR_LOG_FOLDER, config.GENERAL_LOG_FOLDER, config.DEBUG_LOG_FOLDER]:
                    if os.path.exists(subfolder):
                        for file in os.listdir(subfolder):
                            file_path = os.path.join(subfolder, file)
                            if os.path.isfile(file_path):
                                os.unlink(file_path)
            # Lösche Datenbank
            if os.path.exists(config.DB_FOLDER):
                logger.info(f"Lösche Datenbanken in: {config.DB_FOLDER}")
                for file in os.listdir(config.DB_FOLDER):
                    file_path = os.path.join(config.DB_FOLDER, file)
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
            return True
        except Exception as e:
            logger.error(f"Fehler beim Löschen der AppData: {str(e)}")
            return False
