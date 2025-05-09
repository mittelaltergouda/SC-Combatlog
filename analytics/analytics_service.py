"""
analytics_service.py

Kapselt alle Datenbankabfragen für Statistik- und Leaderboard-Berechnungen.
Ermöglicht die Entkopplung der Statistiklogik von der Datenbank.
"""
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple
from data import database
from log_processing import npc_handler
from core import config

class AnalyticsService:
    @staticmethod
    def get_kills_by_me(player_lower: str, *_args, **_kwargs) -> int:
        session = database.get_session()
        try:
            count = session.query(database.Kill).filter(
                database.Kill.killer.ilike(player_lower),
                database.Kill.killed_player != player_lower
            ).count()
            return count
        finally:
            session.close()

    @staticmethod
    def get_deaths_total(player_lower: str, *_args, **_kwargs) -> int:
        session = database.get_session()
        try:
            count = session.query(database.Kill).filter(
                database.Kill.killed_player.ilike(player_lower)
            ).count()
            return count
        finally:
            session.close()

    @staticmethod
    def get_suicides(player_lower: str, *_args, **_kwargs) -> int:
        session = database.get_session()
        try:
            count = session.query(database.Kill).filter(
                database.Kill.killer.ilike(player_lower),
                database.Kill.killed_player.ilike(player_lower)
            ).count()
            return count
        finally:
            session.close()

    @staticmethod
    def get_kills_detail(player_lower: str, *_args, **_kwargs) -> List[str]:
        session = database.get_session()
        try:
            kills = session.query(database.Kill.killed_player).filter(
                database.Kill.killer.ilike(player_lower),
                database.Kill.killed_player != player_lower
            ).all()
            return [k[0] for k in kills]
        finally:
            session.close()

    @staticmethod
    def get_deaths_detail(player_lower: str, *_args, **_kwargs) -> List[str]:
        session = database.get_session()
        try:
            deaths = session.query(database.Kill.killer).filter(
                database.Kill.killed_player.ilike(player_lower),
                database.Kill.killer != player_lower
            ).all()
            return [d[0] for d in deaths]
        finally:
            session.close()

    @staticmethod
    def get_all_kills(player_lower: str, *_args, **_kwargs) -> List[tuple]:
        session = database.get_session()
        from sqlalchemy import func
        try:
            res = session.query(database.Kill.killed_player, func.count(database.Kill.id).label('cnt'))\
                .filter(database.Kill.killer.ilike(player_lower), database.Kill.killed_player != player_lower)\
                .group_by(database.Kill.killed_player)\
                .order_by(func.count(database.Kill.id).desc())\
                .all()
            return res
        finally:
            session.close()

    @staticmethod
    def get_all_deaths(player_lower: str, *_args, **_kwargs) -> List[tuple]:
        session = database.get_session()
        from sqlalchemy import func
        try:
            res = session.query(database.Kill.killer, func.count(database.Kill.id).label('cnt'))\
                .filter(database.Kill.killed_player.ilike(player_lower), database.Kill.killer != player_lower)\
                .group_by(database.Kill.killer)\
                .order_by(func.count(database.Kill.id).desc())\
                .all()
            return res
        finally:
            session.close()

    @staticmethod
    def get_recent_events(params: tuple, *_args, **_kwargs) -> List[tuple]:
        session = database.get_session()
        try:
            player1, player2, player3, player4 = params
            q = session.query(
                database.Kill.timestamp,
                database.Kill.killed_player,
                database.Kill.killer,
                database.Kill.zone,
                database.Kill.weapon,
                database.Kill.damage_class,
                database.Kill.damage_type
            ).filter(
                ((database.Kill.killer.ilike(player1)) | (database.Kill.killed_player.ilike(player2))) &
                ~((database.Kill.killer.ilike(player3)) & (database.Kill.killed_player.ilike(player4)))
            ).order_by(database.Kill.timestamp.desc()).limit(1000)
            return q.all()
        finally:
            session.close()

    @staticmethod
    def get_all_entities() -> List[str]:
        session = database.get_session()
        try:
            killed = session.query(database.Kill.killed_player).distinct().all()
            killer = session.query(database.Kill.killer).distinct().all()
            return list(set([k[0] for k in killed] + [k[0] for k in killer]))
        finally:
            session.close()
