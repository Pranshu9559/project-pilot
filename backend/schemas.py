from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProjectResponse(BaseModel):
    id: int
    title: str
    problem: str
    domain: str
    difficulty: str
    duration_weeks: int
    skills_required: List[str]
    tech_stack: List[str]
    dataset_or_api: Optional[str] = None
    mvp: List[str]
    layer2: List[str]
    stretch: List[str]
    career_fit: List[str]
    key_points: List[str]
    common_mistakes: List[str]
    status: str

    class Config:
        from_attributes = True
