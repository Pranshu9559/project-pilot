from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, JSON, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    goal = Column(String, nullable=True) # academic, portfolio, learning
    level = Column(String, nullable=True) # beginner, intermediate, advanced
    skills = Column(JSON, default=[]) # list of strings
    target_role = Column(String, nullable=True)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    problem = Column(Text, nullable=False)
    domain = Column(String, nullable=False, index=True) # Web, Data Science, AI/ML, Mobile, IoT
    difficulty = Column(String, nullable=False) # Beginner, Intermediate, Advanced
    duration_weeks = Column(Integer, nullable=False)
    skills_required = Column(JSON, default=[])
    tech_stack = Column(JSON, default=[])
    dataset_or_api = Column(String, nullable=True)
    mvp = Column(JSON, default=[])
    layer2 = Column(JSON, default=[])
    stretch = Column(JSON, default=[])
    career_fit = Column(JSON, default=[])
    key_points = Column(JSON, default=[])
    common_mistakes = Column(JSON, default=[])
    status = Column(String, default="approved") # pending, approved

class SavedPlan(Base):
    __tablename__ = "saved_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    idea = Column(Text, nullable=False)
    goal = Column(String, nullable=False)
    feasibility_score = Column(Float, nullable=False)
    plan_json = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Completion(Base):
    __tablename__ = "completions"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    repo_url = Column(String, nullable=True)
