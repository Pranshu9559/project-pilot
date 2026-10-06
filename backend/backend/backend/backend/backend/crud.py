from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
import models

def get_projects(
    db: Session,
    domain: Optional[str] = None,
    difficulty: Optional[str] = None,
    duration_max: Optional[int] = None,
    skill: Optional[str] = None,
    goal: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50
):
    query = db.query(models.Project).filter(models.Project.status == "approved")

    if domain:
        query = query.filter(models.Project.domain.ilike(f"%{domain}%"))
    if difficulty:
        query = query.filter(models.Project.difficulty.ilike(f"%{difficulty}%"))
    if duration_max:
        query = query.filter(models.Project.duration_weeks <= duration_max)
    if goal:
        query = query.filter(models.Project.career_fit.has_key(goal) | models.Project.domain.ilike(f"%{goal}%"))
    if search:
        search_filter = or_(
            models.Project.title.ilike(f"%{search}%"),
            models.Project.problem.ilike(f"%{search}%"),
            models.Project.domain.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Python-side filtering for JSON lists if needed or SQL operators
    projects = query.offset(skip).limit(limit).all()

    if skill:
        skill_lower = skill.lower()
        projects = [
            p for p in projects 
            if any(skill_lower in s.lower() for s in (p.skills_required or [])) or
               any(skill_lower in t.lower() for t in (p.tech_stack or []))
        ]

    return projects

def get_project_by_id(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def seed_database(db: Session):
    existing = db.query(models.Project).first()
    if not existing:
        for p_data in SAMPLE_PROJECTS:
            project = models.Project(**p_data)
            db.add(project)
        db.commit()
