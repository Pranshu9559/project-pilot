from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
import crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ProjectPilot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    db = next(get_db())
    crud.seed_database(db)

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "ProjectPilot API"}

@app.get("/api/projects", response_model=List[schemas.ProjectResponse])
def list_projects(
    domain: Optional[str] = None,
    difficulty: Optional[str] = None,
    duration_max: Optional[int] = None,
    skill: Optional[str] = None,
    goal: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    projects = crud.get_projects(
        db=db,
        domain=domain,
        difficulty=difficulty,
        duration_max=duration_max,
        skill=skill,
        goal=goal,
        search=search,
        skip=skip,
        limit=limit
    )
    return projects

@app.get("/api/projects/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: int, db: Session: Session = Depends(get_db)):
    project = crud.get_project_by_id(db=db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
