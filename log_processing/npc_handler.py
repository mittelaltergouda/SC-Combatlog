import re
from data import database
import logging

# Logger für diese Datei einrichten
logger = logging.getLogger(__name__)

def clean_npc_name(npc_name):
    """
    Removes trailing numeric IDs from an NPC name.
    Example: "pu_human_enemy_npc_juggernaut_12345" -> "pu_human_enemy_npc_juggernaut"
    """
    return re.sub(r'_\d+$', '', npc_name.strip().lower())

def auto_categorize_npc(npc_name):
    """
    Automatically determines a category for an NPC based on keywords in the cleaned name.
    Returns one of: pilot, gunner, ground, civilian, worker, lawenforcement, pirate, technical, test, animal, or uncategorized.
    """
    name = clean_npc_name(npc_name).lower()
    
    # Spezielle Regel für ARGO_ATLS_GEO - als "unknown" kategorisieren
    if "argo_atls_geo" in name:
        logger.debug(f"NPC {npc_name} als 'unknown' kategorisiert (ARGO_ATLS_GEO)")
        return "unknown"
    
    # Erweiterte Kategorisierung: Alle Namen mit "hangar" und "unknown" als "unknown" klassifizieren
    if "hangar" in name.lower() and "unknown" in name.lower():
        logger.debug(f"NPC {npc_name} als 'unknown' kategorisiert (enthält 'hangar' und 'unknown')")
        return "unknown"
    
    # Tierkategorisierung basierend auf Präfixen
    if any(name.startswith(prefix) for prefix in ["vlk_", "kopion_", "quasigrazer_"]):
        return "animal"
        
    # NPC_Archetypes-Kategorisierung - diese sollten NIEMALS als Spieler klassifiziert werden
    if "npc_archetypes" in name:
        if "soldier" in name or "juggernaut" in name:
            return "ground"
        elif "pilot" in name:
            return "pilot"
        elif "techie" in name or "technical" in name:
            return "technical"
        elif "prisoner" in name or "civilian" in name:
            return "civilian"
        else:
            # Allgemeine NPC_Archetypes als Grundeinheit einstufen
            return "ground"
    
    # Hazard-Dungeon-NPCs erkennen (außer den speziell behandelten Fall)
    if "hazard" in name and "dungeon" in name:
        if "exec" in name:
            return "ground"  # Executive NPCs in Hazard-Dungeons
        elif "medic" in name or "med" in name:
            return "technical"  # Medics in Hazard-Dungeons
        else:
            return "ground"  # Standard-Einstufung für Hazard-Dungeon-NPCs
    
    if "pilot" in name:
        return "pilot"
    if "gunner" in name:
        return "gunner"
    if any(k in name for k in ["ground", "soldier", "cqc", "juggernaut", "sniper",
                               "gangster", "grunt", "kareah", "militia", "superboss",
                               "exec", "executive"]):
        return "ground"
    if "civilian" in name or ("populace" in name and "worker" not in name):
        return "civilian"
    if any(k in name for k in ["worker", "shopkeeper", "vendor", "gardener", "farmer"]):
        return "worker"
    if any(k in name for k in ["law", "security", "guard"]):
        return "lawenforcement"
    if "pirate" in name:
        return "pirate"
    if any(k in name for k in ["engineer", "technical", "techie", "medic"]):
        return "technical"
    if "test" in name:
        return "test"
    # Allgemeine Cheesecake-Archetypes als Grundeinheit einstufen
    if "cheesecake" in name:
        return "ground"
    # Wenn 'hazard' im Namen ist, aber nicht genauer kategorisiert werden kann
    if "hazard" in name:
        return "ground"
    return "uncategorized"

def get_npc_category(npc_name):
    """
    Returns the category for the cleaned NPC name from DB, or None if not found.
    """
    try:
        from data.models import NPCCategory
        session = database.get_session()
        cleaned = clean_npc_name(npc_name)
        cat = session.query(NPCCategory).filter_by(name=cleaned).first()
        session.close()
        if cat:
            return cat.category
        return None
    except Exception as e:
        logger.error(f"Fehler beim Abrufen der NPC-Kategorie für {npc_name}: {str(e)}")
        return None

def load_all_npc_categories():
    """
    Loads all npc_name->category from the DB into a dictionary.
    """
    try:
        from data.models import NPCCategory
        session = database.get_session()
        rows = session.query(NPCCategory).all()
        out_dict = {row.name: row.category for row in rows}
        session.close()
        return out_dict
    except Exception as e:
        logger.error(f"Fehler beim Laden aller NPC-Kategorien: {str(e)}")
        return {}

def recategorize_uncategorized():
    """
    Checks all NPCs in npc_categories that are 'uncategorized' and tries to recategorize them.
    """
    try:
        from data.models import NPCCategory
        session = database.get_session()
        rows = session.query(NPCCategory).filter_by(category='uncategorized').all()
        if not rows:
            session.close()
            return
        updated_count = 0
        for row in rows:
            npc_name = row.name
            old_cat = row.category
            new_cat = auto_categorize_npc(npc_name)
            if new_cat != "uncategorized":
                row.category = new_cat
                logger.info(f"Recategorized {npc_name} from {old_cat} to {new_cat}")
                updated_count += 1
        if updated_count > 0:
            session.commit()
            logger.debug(f"Insgesamt {updated_count} NPCs neu kategorisiert")
        session.close()
    except Exception as e:
        logger.error(f"Fehler bei der Neukategorisierung von NPCs: {str(e)}")

def save_npc_category(npc_name, default_category="uncategorized"):
    """
    If npc_name not in npc_categories, auto-categorize and do INSERT OR IGNORE.
    Afterwards, calls recategorize_uncategorized() once.
    """
    try:
        from data.models import NPCCategory
        session = database.get_session()
        cleaned = clean_npc_name(npc_name)
        existing = session.query(NPCCategory).filter_by(name=cleaned).first()
        if existing is not None:
            session.close()
            return  # Already known

        cat = auto_categorize_npc(cleaned)
        if cat == "uncategorized" and default_category != "uncategorized":
            cat = default_category

        npc = NPCCategory(name=cleaned, category=cat)
        session.add(npc)
        try:
            session.commit()
        except Exception:
            session.rollback()  # Bei Unique-Constraint-Verletzung ("INSERT OR IGNORE")
        logger.info(f"NPC kategorisiert: {cleaned}, Kategorie={cat}")
        # Versuche, unkategorisierte NPCs neu zu kategorisieren
        session.close()
        recategorize_uncategorized()
    except Exception as e:
        logger.error(f"Fehler beim Speichern der NPC-Kategorie für {npc_name}: {str(e)}")
