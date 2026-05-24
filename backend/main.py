from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from backend.database import engine, Base, get_db
from backend.models import PlayerProfile, WellnessLog, ChatMessage
from agent.engine import CricketHealthAgent
from agent.tools.rehab import get_cricket_rehab_guide

# Initialize Database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CrickHealth AI Backend", version="1.0.0")

# Setup CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Cricketer Health Agent
agent = CricketHealthAgent()

# Seed database with sample data if empty
@app.on_event("startup")
def seed_data():
    db = next(get_db())
    try:
        # Check if profile exists, if not, create default
        profile = db.query(PlayerProfile).first()
        if not profile:
            profile = PlayerProfile(
                name="Jasprit Singh",
                role="Fast Bowler",
                weight=80.0,
                height=183.0,
                age=27,
                format_type="Test",
                active_injury="None"
            )
            db.add(profile)
            db.commit()
            print("Default player profile seeded.")

        # Check if logs exist, if not, seed 28 days of realistic workload logs for a fast bowler
        log_count = db.query(WellnessLog).count()
        if log_count == 0:
            today = datetime.utcnow()
            logs = []
            
            # Create 28 days of logs
            for i in range(27, -1, -1):
                date_str = (today - timedelta(days=i)).strftime("%Y-%m-%d")
                
                # Bowler workload: let's model some variance.
                # A fast bowler might bowl 6-10 overs in training, and rest on some days.
                # Workload units = (overs bowled * 10) + gym session duration (mins) * RPE / 10
                # Let's keep it simple: workload between 5.0 and 25.0
                # Introduce a rest day every 4-5 days (workload 0-2)
                if i % 5 == 0:
                    workload = random.uniform(0.0, 3.0)
                    training_hours = 0.5
                    soreness = max(1, random.randint(1, 3))
                    fatigue = max(1, random.randint(1, 3))
                else:
                    workload = random.uniform(10.0, 22.0)
                    training_hours = random.uniform(1.5, 3.0)
                    soreness = random.randint(2, 4)
                    fatigue = random.randint(2, 4)
                    
                log = WellnessLog(
                    date=date_str,
                    sleep_hours=random.uniform(7.0, 9.0),
                    soreness_level=soreness,
                    fatigue_level=fatigue,
                    training_hours=round(training_hours, 1),
                    workload=round(workload, 1)
                )
                logs.append(log)
                
            db.bulk_save_objects(logs)
            db.commit()
            print("28 days of wellness logs seeded.")
            
        # Seed welcome message if empty
        chat_count = db.query(ChatMessage).count()
        if chat_count == 0:
            welcome = ChatMessage(
                sender="coach",
                message="Hello Athlete! I am CrickHealth AI, your specialized health and recovery coach. I've analyzed your profile as a Fast Bowler. Ask me anything about your nutrition targets, shoulder/back rehabilitation, or check your injury risk (ACWR)!"
            )
            db.add(welcome)
            db.commit()
    except Exception as e:
        print(f"Error seeding DB: {e}")
    finally:
        db.close()


@app.get("/api/profile")
def get_profile(db: Session = Depends(get_db)):
    profile = db.query(PlayerProfile).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@app.post("/api/profile")
def update_profile(updated: dict, db: Session = Depends(get_db)):
    profile = db.query(PlayerProfile).first()
    if not profile:
        profile = PlayerProfile()
        db.add(profile)

    profile.name = updated.get("name", profile.name)
    profile.role = updated.get("role", profile.role)
    profile.weight = float(updated.get("weight", profile.weight))
    profile.height = float(updated.get("height", profile.height))
    profile.age = int(updated.get("age", profile.age))
    profile.format_type = updated.get("format_type", profile.format_type)
    profile.active_injury = updated.get("active_injury", profile.active_injury)

    db.commit()
    db.refresh(profile)
    return profile


@app.get("/api/wellness")
def get_wellness(db: Session = Depends(get_db)):
    # Get last 28 logs sorted by date ascending
    logs = db.query(WellnessLog).order_index = WellnessLog.date.asc()
    logs = db.query(WellnessLog).order_by(WellnessLog.date.desc()).limit(28).all()
    # Reverse so they are chronological
    logs.reverse()
    
    # Calculate current ACWR
    workload_list = [log.workload for log in logs]
    agent_inst = CricketHealthAgent()
    profile = db.query(PlayerProfile).first()
    profile_dict = {
        "role": profile.role if profile else "All-rounder",
        "weight": profile.weight if profile else 75,
        "height": profile.height if profile else 178,
        "age": profile.age if profile else 24,
        "format_type": profile.format_type if profile else "ODI",
        "active_injury": profile.active_injury if profile else "None",
    }
    
    # Compute ACWR utilizing tool
    from agent.tools.workload import calculate_acwr
    acwr_report = calculate_acwr(workload_list)

    return {
        "logs": logs,
        "acwr": acwr_report
    }


@app.post("/api/wellness")
def log_wellness(data: dict, db: Session = Depends(get_db)):
    # Check if there is already a log for today, if so, update it.
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    log = db.query(WellnessLog).filter(WellnessLog.date == today_str).first()
    
    # Workload calculation: training_hours * RPE (1-10 rate of perceived exertion)
    training_hours = float(data.get("training_hours", 2.0))
    rpe = float(data.get("rpe", 6.0))
    # Standard Session-RPE workload unit = duration (mins) * RPE
    calculated_workload = (training_hours * 60.0) * rpe / 10.0  # Normalized scale

    if not log:
        log = WellnessLog(date=today_str)
        db.add(log)
        
    log.sleep_hours = float(data.get("sleep_hours", 8.0))
    log.soreness_level = int(data.get("soreness_level", 2))
    log.fatigue_level = int(data.get("fatigue_level", 2))
    log.training_hours = training_hours
    log.workload = round(calculated_workload, 1)

    db.commit()
    db.refresh(log)
    
    return log


@app.get("/api/chat/history")
def get_chat_history(db: Session = Depends(get_db)):
    messages = db.query(ChatMessage).order_by(ChatMessage.timestamp.asc()).all()
    return messages


@app.post("/api/chat")
def chat_with_coach(payload: dict, db: Session = Depends(get_db)):
    user_message = payload.get("message", "").strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Empty message")

    # 1. Fetch current player state
    profile = db.query(PlayerProfile).first()
    if not profile:
        profile = PlayerProfile()
        db.add(profile)
        db.commit()
        db.refresh(profile)

    profile_dict = {
        "role": profile.role,
        "weight": profile.weight,
        "height": profile.height,
        "age": profile.age,
        "format_type": profile.format_type,
        "active_injury": profile.active_injury,
        "sleep_hours": 8.0,
        "soreness_level": 2,
        "fatigue_level": 2,
        "training_hours": 2.0,
    }

    # Fetch last wellness log to get today's feel
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    latest_log = db.query(WellnessLog).filter(WellnessLog.date == today_str).first()
    if not latest_log:
        latest_log = db.query(WellnessLog).order_by(WellnessLog.date.desc()).first()
        
    if latest_log:
        profile_dict.update({
            "sleep_hours": latest_log.sleep_hours,
            "soreness_level": latest_log.soreness_level,
            "fatigue_level": latest_log.fatigue_level,
            "training_hours": latest_log.training_hours,
        })

    # 2. Get past 28 days of workload logs
    logs = db.query(WellnessLog).order_by(WellnessLog.date.desc()).limit(28).all()
    logs.reverse()
    workload_history = [log.workload for log in logs]

    # 3. Save User message to history
    user_msg_db = ChatMessage(sender="user", message=user_message)
    db.add(user_msg_db)
    db.commit()

    # 4. Call CrickHealth AI Agent
    agent_response = agent.run(profile_dict, workload_history, user_message)
    coach_text = agent_response["response"]

    # 5. Save Coach reply to history
    coach_msg_db = ChatMessage(sender="coach", message=coach_text)
    db.add(coach_msg_db)
    db.commit()

    return {
        "response": coach_text,
        "tool_data": agent_response["tool_data"]
    }


@app.get("/api/rehab/{injury_key}")
def get_rehab(injury_key: str):
    res = get_cricket_rehab_guide(injury_key)
    if res.get("status") == "error":
        raise HTTPException(status_code=404, detail=res.get("message"))
    return res


@app.post("/api/reset")
def reset_db(db: Session = Depends(get_db)):
    """Clears history and wellness logs, keeps profile."""
    try:
        db.query(ChatMessage).delete()
        db.query(WellnessLog).delete()
        
        # Reset profile to default
        profile = db.query(PlayerProfile).first()
        if profile:
            profile.name = "Jasprit Singh"
            profile.role = "Fast Bowler"
            profile.weight = 80.0
            profile.height = 183.0
            profile.age = 27;
            profile.format_type = "Test"
            profile.active_injury = "None"
            
        # Re-seed welcome message
        welcome = ChatMessage(
            sender="coach",
            message="Hello Athlete! All records have been cleared. I'm ready to start fresh. Ask me about your cricket nutrition or injury recovery!"
        )
        db.add(welcome)
        db.commit()
        return {"status": "success", "message": "Database reset completed successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
