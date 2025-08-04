# tools.py (Corrected and Enhanced)
from typing import List, Set
from langchain.tools import tool
from pydantic import BaseModel, Field
from transformers import pipeline
from config import settings
from apps.job_scraper import (
    indeed_api, linkedin_api, glassdoor_api, google_jobs_api,
    jsearch_api, monster_api, ziprecruiter_api
)
import asyncio
from apps.services import ResumeOptimizer, ATSChecker, JobMatchResumeMCP, JobMarketIntelligence


# Load Hugging Face model
try:
    skill_extractor = pipeline("ner", model=settings.SKILL_EXTRACTION_MODEL)
except Exception as e:
    print(f"Warning: Failed to load skill extractor. Using fallback. Error: {e}")
    skill_extractor = None

# Helper function
async def _internal_extract_skills(text: str) -> Set[str]:
    def extract():
        if not skill_extractor:
            return {"Python", "FastAPI", "SQL"}
        skills = skill_extractor(text)
        return set(
            skill.get("word", "").strip()
            for skill in skills
            if isinstance(skill.get("word", ""), str) and "SKILL" in skill.get("entity", "")
        )
    return await asyncio.to_thread(extract)

# Pydantic Models for Tool Inputs
class ResumeInput(BaseModel):
    text: str = Field(..., description="Text content of resume or job description")

class JobSearchInput(BaseModel):
    keywords: str = Field(..., description="The job title(s) to search for")
    location: str = Field(..., description="The city or region to search in")

class ResumeJobCompareInput(BaseModel):
    resume_text: str = Field(..., description="The text content of the resume")
    job_description: str = Field(..., description="The job description to compare")

class MarketInsightInput(BaseModel):
    job_title: str = Field(..., description="The job title to get market insights for")

class ResumeOptimizationInput(BaseModel):
    resume: str = Field(...)
    job_description: str = Field(...)

class ATSCheckInput(BaseModel):
    resume: str = Field(...)
    job_description: str = Field(...)

class JobMatchInput(BaseModel):
    resume_text: str = Field(...)
    preferences: dict = Field(...)

# --- Tools ---
@tool
def extract_skills_from_text(input: ResumeInput) -> List[str]:
    """Extract a list of technical skills from a block of text."""
    skills = asyncio.run(_internal_extract_skills(input.text))
    return list(skills)

@tool
def search_for_jobs(input: JobSearchInput) -> str:
    """Search for jobs on multiple platforms using keywords and location."""
    keywords = input.keywords
    location = input.location

    search_tasks = [
        asyncio.to_thread(jsearch_api.search, keywords, location),
        asyncio.to_thread(google_jobs_api.search, keywords, location),
        asyncio.to_thread(indeed_api.search, keywords, location),
        asyncio.to_thread(ziprecruiter_api.search, keywords, location),
        asyncio.to_thread(monster_api.search, keywords, location),
        asyncio.to_thread(linkedin_api.search, keywords, location),
        asyncio.to_thread(glassdoor_api.search, keywords, location),
    ]

    results = asyncio.run(asyncio.gather(*search_tasks, return_exceptions=True))

    all_jobs = [job for res in results if isinstance(res, list) for job in res]
    unique_jobs = []
    seen_urls = set()
    for job in all_jobs:
        url = job.get("url")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_jobs.append(job)

    if not unique_jobs:
        return "No jobs found."

    output = "Top job listings:\n\n"
    for i, job in enumerate(unique_jobs[:5], 1):
        output += (
            f"{i}. Title: {job.get('title', 'N/A')}\n"
            f"   Company: {job.get('company', 'N/A')}\n"
            f"   Location: {job.get('location', 'N/A')}\n"
            f"   URL: {job.get('url', 'N/A')}\n\n"
        )
    return output

@tool
def analyze_resume_against_job(input: ResumeJobCompareInput) -> str:
    """Analyze a resume against a job description to find matching/missing skills."""
    resume_skills = asyncio.run(_internal_extract_skills(input.resume_text))
    job_skills = asyncio.run(_internal_extract_skills(input.job_description))

    matching = list(resume_skills & job_skills)
    missing = list(job_skills - resume_skills)

    return (
        f"Matching Skills: {', '.join(matching) or 'None'}\n"
        f"Missing Skills: {', '.join(missing) or 'None'}\n"
        f"Tip: Highlight {matching[0] if matching else 'key skills'} in your summary. "
        f"Consider learning {missing[0] if missing else 'relevant skills'}."
    )

@tool
def get_market_insights(input: MarketInsightInput) -> dict:
    """Provides salary and skill demand insights for a job title."""
    insight = JobMarketIntelligence()
    result = asyncio.run(insight.generate_market_insights([input.job_title], [input.job_title]))
    return result

@tool
def optimize_resume_for_job(input: ResumeOptimizationInput) -> dict:
    """Optimizes a resume for a specific job description."""
    optimizer = ResumeOptimizer()
    result = asyncio.run(optimizer.optimize_resume_for_job(input.resume, {"description": input.job_description}))
    return result

@tool
def ats_check_resume(input: ATSCheckInput) -> dict:
    """Performs ATS compatibility analysis."""
    checker = ATSChecker()
    return asyncio.run(checker.analyze_ats_compatibility(input.resume, input.job_description))

@tool
def match_jobs_to_resume(input: JobMatchInput) -> dict:
    """Find and optimize best-matching jobs from resume and preferences."""
    matcher = JobMatchResumeMCP()
    return asyncio.run(matcher.find_and_optimize_jobs(input.resume_text, input.preferences))
