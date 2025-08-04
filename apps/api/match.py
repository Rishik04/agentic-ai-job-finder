from fastapi import APIRouter
from app.schemas import ResumeRequest, JobMatchResult
from app.services.match_engine import JobMatchResumeMCP

router = APIRouter()

@router.post("/job-match", response_model=JobMatchResult)
async def match_jobs(payload: ResumeRequest):
    engine = JobMatchResumeMCP()
    result = await engine.find_and_optimize_jobs(payload.resume_text, payload.preferences)
    return result