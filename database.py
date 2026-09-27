from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./fitbuddy.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    goal = Column(String)
    intensity = Column(String)
    schedule = Column(Integer, default=7)


class WorkoutPlan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    original_plan = Column(String)
    updated_plan = Column(String, nullable=True)
    nutrition_tip = Column(String, nullable=True)


Base.metadata.create_all(bind=engine)


def save_user(user_id: int, name: str, age: int, weight: float, goal: str, intensity: str):
    db = SessionLocal()
    existing = db.query(User).filter_by(id=user_id).first()
    if existing:
        existing.name, existing.age, existing.weight = name, age, weight
        existing.goal, existing.intensity = goal, intensity
    else:
        db.add(User(id=user_id, name=name, age=age, weight=weight, goal=goal, intensity=intensity, schedule=7))
    db.commit()
    db.close()


def save_plan(user_id: int, plan: str, nutrition_tip: str = ""):
    db = SessionLocal()
    db.add(WorkoutPlan(user_id=user_id, original_plan=plan, nutrition_tip=nutrition_tip))
    db.commit()
    db.close()


def update_plan(user_id: int, updated_text: str):
    db = SessionLocal()
    workout = db.query(WorkoutPlan).filter_by(user_id=user_id).first()
    if workout:
        workout.updated_plan = updated_text
        db.commit()
    db.close()


def get_original_plan(user_id: int):
    db = SessionLocal()
    plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
    db.close()
    return plan.original_plan if plan else None


def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    return user


def get_all_users_with_plans():
    db = SessionLocal()
    users = db.query(User).all()
    data = []
    for user in users:
        plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user.id).first()
        data.append({
            "id": user.id, "name": user.name, "age": user.age, "weight": user.weight,
            "goal": user.goal, "intensity": user.intensity,
            "original_plan": plan.original_plan if plan else "N/A",
            "updated_plan": plan.updated_plan if plan and plan.updated_plan else "Not updated",
            "nutrition_tip": plan.nutrition_tip if plan else "",
        })
    db.close()
    return data
