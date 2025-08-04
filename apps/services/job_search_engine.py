from apps.job_scraper import (
    indeed_api, ziprecruiter_api, monster_api,
    google_jobs_api, jsearch_api, linkedin_api, glassdoor_api
)
import asyncio
import hashlib

class JobSearchEngine:
    def __init__(self):
        self.scrapers = [
            indeed_api,
            ziprecruiter_api,
            monster_api,
            google_jobs_api,
            jsearch_api,
            linkedin_api,
            glassdoor_api
        ]

    async def search_all_platforms(self, keywords: str, location: str) -> list[dict]:
        print("Starting aggregated job search...")
        results = await asyncio.gather(
            *[self._run_scraper(scraper, keywords, location) for scraper in self.scrapers],
            return_exceptions=True
        )

        jobs = []
        for result in results:
            if isinstance(result, list):
                jobs.extend(result)

        return await self._deduplicate_jobs(jobs)

    async def _run_scraper(self, scraper, keywords, location):
        try:
            return scraper.search(keywords, location)
        except Exception as e:
            print(f"Error from {scraper.__class__.__name__}: {e}")
            return []

    async def _deduplicate_jobs(self, jobs: list[dict]) -> list[dict]:
        seen = set()
        unique_jobs = []
        for job in jobs:
            job_hash = hashlib.md5(f"{job['title']}{job['company']}{job['location']}".encode()).hexdigest()
            if job_hash not in seen:
                seen.add(job_hash)
                unique_jobs.append(job)
        return unique_jobs
