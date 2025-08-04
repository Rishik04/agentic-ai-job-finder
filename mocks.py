# mocks.py

import asyncio

class MockJobBoardAPI:
    """A mock API to simulate fetching jobs from platforms like Indeed, LinkedIn, etc."""
    async def search(self, keywords, location):
        print(f"Mock Searching for '{keywords}' in '{location}'...")
        await asyncio.sleep(0.5) # Simulate network latency
        return [
            {
                "id": f"mock_{i}",
                "title": f"Senior {keywords}",
                "company": f"Tech Company {i}",
                "location": location,
                "description": f"Seeking a {keywords} with experience in Python, SQL, and Cloud. Responsibilities include building scalable systems. Knowledge of Docker is a plus.",
                "url": f"https://example.com/job/{i}"
            } for i in range(1, 6)
        ]

# Instantiate mock APIs
indeed_api = MockJobBoardAPI()
linkedin_scraper = MockJobBoardAPI()
glassdoor_api = MockJobBoardAPI()