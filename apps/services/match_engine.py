from transformers import pipeline
from apps.services.resume_optimizer import ResumeOptimizer
from apps.services.job_search_engine import JobSearchEngine
from apps.services.market_insight import JobMarketIntelligence
from config import settings

class JobMatchResumeMCP:
    def __init__(self):
        self.text_similarity = pipeline("feature-extraction", model=settings.TEXT_SIMILARITY_MODEL)
        self.skill_extractor = pipeline("ner", model=settings.SKILL_EXTRACTION_MODEL)
        self.text_generator = pipeline("text-generation", model=settings.TEXT_GENERATION_MODEL)

        self.job_engine = JobSearchEngine()
        self.resume_optimizer = ResumeOptimizer()
        self.market_intelligence = JobMarketIntelligence()

    async def find_and_optimize_jobs(self, resume_text, preferences):
        resume_analysis = {"text": resume_text}  # TODO: Implement actual analysis
        jobs = await self.job_engine.search_all_platforms(
            preferences.job_titles, preferences.location, preferences.experience_level
        )

        top_matches = []
        for job in jobs[:5]:
            optimized = await self.resume_optimizer.optimize_resume_for_job(resume_text, job)
            top_matches.append({
                "job": job,
                "optimized_resume": optimized["optimized_resume"],
                "match_score": 0.87,  # TODO: Calculate real score
                "missing_skills": optimized["improvements"]["missing_skills"],
                "recommendations": optimized["recommendations"]
            })

        return {
            "total_jobs_found": len(jobs),
            "top_matches": top_matches,
            "market_insights": await self.market_intelligence.generate_market_insights(resume_analysis, preferences.job_titles),
            "skill_gaps": {"todo": True}  # TODO: Implement
        }