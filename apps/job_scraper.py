# job_scraper.py (Selenium + Anti-blocking)

import time
import tempfile
import random
import os
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from urllib.parse import quote_plus

# Optional proxy
PROXY = None  # Example: "username:password@proxy-ip:port"

def get_driver():
    temp_dir = tempfile.mkdtemp()
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")

    return uc.Chrome(options=options, user_data_dir=temp_dir)

def build_url(base_url, keywords, location):
    clean_keywords = keywords.replace(",", " ").replace(" or ", " ")
    return f"{base_url}?q={quote_plus(clean_keywords)}&l={quote_plus(location)}"

class IndeedScraper:
    def search(self, keywords: str, location: str) -> list[dict]:
        print(f"Scraping Indeed for '{keywords}' in '{location}'...")
        jobs = []
        try:
            driver = get_driver()
            url = build_url("https://www.indeed.com/jobs", keywords, location)
            driver.get(url)
            time.sleep(random.uniform(2, 4))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            job_cards = soup.find_all('div', class_='job_seen_beacon')

            for card in job_cards[:10]:
                try:
                    title_element = card.find('h2', class_='jobTitle').find('a')
                    title = title_element.get_text(strip=True)
                    job_url = "https://www.indeed.com" + title_element['href']
                    company = card.find('span', class_='companyName').get_text(strip=True)
                    job_location = card.find('div', class_='companyLocation').get_text(strip=True)
                    description_snippet = card.find('div', class_='job-snippet').get_text(strip=True)

                    jobs.append({
                        "id": f"indeed_{title_element.get('data-jk', '')}",
                        "title": title,
                        "company": company,
                        "location": job_location,
                        "description": description_snippet,
                        "url": job_url
                    })
                except AttributeError:
                    continue

        except Exception as e:
            print(f"Indeed scraping error: {e}")
        finally:
            driver.quit()

        print(f"Found {len(jobs)} jobs on Indeed.")
        return jobs

class ZipRecruiterScraper:
    def search(self, keywords: str, location: str) -> list[dict]:
        print(f"Scraping ZipRecruiter for '{keywords}' in '{location}'...")
        jobs = []
        try:
            driver = get_driver()
            url = build_url("https://www.ziprecruiter.com/jobs-search", keywords, location)
            driver.get(url)
            time.sleep(random.uniform(2, 4))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            job_cards = soup.find_all('div', class_='job_content')

            for card in job_cards[:10]:
                try:
                    title_element = card.find('h2', class_='title').find('a')
                    title = title_element.get_text(strip=True)
                    job_url = title_element['href']
                    company = card.find('a', class_='company_name').get_text(strip=True)
                    job_location = card.find('p', class_='location').get_text(strip=True)
                    description_snippet = card.find('p', class_='job_snippet').get_text(strip=True)

                    jobs.append({
                        "id": f"zip_{card.get('data-job-id', '')}",
                        "title": title,
                        "company": company,
                        "location": job_location,
                        "description": description_snippet,
                        "url": job_url
                    })
                except AttributeError:
                    continue

        except Exception as e:
            print(f"ZipRecruiter scraping error: {e}")
        finally:
            driver.quit()

        print(f"Found {len(jobs)} jobs on ZipRecruiter.")
        return jobs

class LinkedInScraper:
    def search(self, keywords: str, location: str) -> list[dict]:
        print("Skipping LinkedIn: Scraping restricted.")
        return []

class GlassdoorScraper:
    def search(self, keywords: str, location: str) -> list[dict]:
        print("Skipping Glassdoor: Scraping restricted.")
        return []

class GoogleJobsAPI:
    def search(self, keywords: str, location: str) -> list[dict]:
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            print("Missing SERPAPI_API_KEY")
            return []
        return []

class JSearchAPI:
    def search(self, keywords: str, location: str) -> list[dict]:
        api_key = os.getenv("JSEARCH_API_KEY")
        if not api_key:
            print("Missing JSEARCH_API_KEY")
            return []
        return []

class MonsterScraper:
    def search(self, keywords: str, location: str) -> list[dict]:
        return []

# --- Instantiate scrapers ---
indeed_api = IndeedScraper()
ziprecruiter_api = ZipRecruiterScraper()
monster_api = MonsterScraper()
google_jobs_api = GoogleJobsAPI()
jsearch_api = JSearchAPI()
linkedin_api = LinkedInScraper()
glassdoor_api = GlassdoorScraper()
