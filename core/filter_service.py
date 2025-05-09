"""
FilterService für zentrale Filterlogik (Datum, Entity, NPC-Kategorien etc.)
Ermöglicht Wiederverwendung der Filterlogik für GUI, REST-API und Tests.
"""
from typing import Optional, Dict, Any
from datetime import datetime

class FilterService:
    @staticmethod
    def build_entity_filter_dict(entity_vars: Dict[str, Any]) -> Dict[str, bool]:
        """
        Wandelt ein Dict von tkinter.BooleanVar oder bool in ein reines Dict[str, bool] um.
        """
        result = {}
        for key, var in entity_vars.items():
            # Unterstützt sowohl tk.BooleanVar als auch bool
            if hasattr(var, 'get'):
                result[key] = var.get()
            else:
                result[key] = bool(var)
        return result

    @staticmethod
    def validate_date(date_str: str) -> Optional[datetime]:
        """
        Validiert und parst ein Datum im Format YYYY-MM-DD. Gibt None zurück, wenn leer.
        Wirft ValueError bei ungültigem Format.
        """
        if not date_str:
            return None
        return datetime.strptime(date_str, '%Y-%m-%d')

    @staticmethod
    def is_entity_selected(entity_filters: Dict[str, bool], entity_key: str) -> bool:
        """
        Prüft, ob ein bestimmter Entity-Filter aktiv ist.
        """
        return entity_filters.get(entity_key, False)
