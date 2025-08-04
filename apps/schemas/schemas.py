from pydantic import BaseModel
from typing import List, Dict, Any

class Preferences(BaseModel):
    location: str
    job_titles: List[str]
    experience_level: str

class ResumeRequest(BaseModel):
    resume_text: str
    preferences: Preferences

class OptimizedResume(BaseModel):
    job: Dict[str, Any]
    optimized_resume: Dict[str, Any]
    match_score: float
    missing_skills: List[str]
    recommendations: List[str]

class JobMatchResult(BaseModel):
    total_jobs_found: int
    top_matches: List[OptimizedResume]
    market_insights: Dict[str, Any]
    skill_gaps: Dict[str, Any]
