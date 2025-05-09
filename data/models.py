from sqlalchemy import Column, Integer, String, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Kill(Base):
    __tablename__ = 'kills'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String)
    killed_player = Column(String)
    killer = Column(String)
    zone = Column(String)
    weapon = Column(String)
    damage_class = Column(String)
    damage_type = Column(String)
    __table_args__ = (
        UniqueConstraint('timestamp', 'killed_player', 'killer', 'zone', 'weapon', 'damage_class', 'damage_type', name='uix_kill_event'),
    )

class FilePosition(Base):
    __tablename__ = 'file_positions'
    file_path = Column(String, primary_key=True)
    last_offset = Column(Integer)

class NPCCategory(Base):
    __tablename__ = 'npc_categories'
    name = Column(String, primary_key=True)
    category = Column(String)

class Migration(Base):
    __tablename__ = 'migrations'
    version = Column(String, primary_key=True)
