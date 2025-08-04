# config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Hugging Face Models
    TEXT_SIMILARITY_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    SKILL_EXTRACTION_MODEL: str = "jjzha/jobbert_skill_extraction"
    TEXT_GENERATION_MODEL: str = "microsoft/DialoGPT-large"

settings = Settings()