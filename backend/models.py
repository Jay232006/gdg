from sqlalchemy import Column, Integer, Float, String, DateTime, Text
from datetime import datetime
from backend.database import Base

class PlayerProfile(Base):
    __tablename__ = "player_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="Cricket Athlete")
    role = Column(String, default="All-rounder")       # Fast Bowler, Spinner, Wicketkeeper, Batter, All-rounder
    weight = Column(Float, default=75.0)                # in kg
    height = Column(Float, default=178.0)               # in cm
    age = Column(Integer, default=24)
    format_type = Column(String, default="ODI")         # Test, ODI, T20, Training, Recovery
    active_injury = Column(String, default="None")      # shoulder_impingement, lower_back_stress_fracture, side_strain, hamstring_strain, None

class WellnessLog(Base):
    __tablename__ = "wellness_logs"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, default=lambda: datetime.utcnow().strftime("%Y-%m-%d"))
    sleep_hours = Column(Float, default=8.0)
    soreness_level = Column(Integer, default=2)         # 1 to 10
    fatigue_level = Column(Integer, default=2)          # 1 to 10
    training_hours = Column(Float, default=2.0)
    workload = Column(Float, default=12.0)              # Overs bowled or duration * intensity RPE

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String)                             # "user" or "coach"
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
