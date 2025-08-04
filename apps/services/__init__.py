# services/__init__.py

# Re-export key classes to simplify imports
from .match_engine import JobMatchResumeMCP
from .resume_optimizer import ResumeOptimizer
from .ats_checker import ATSChecker
from .market_insight import JobMarketIntelligence

__all__ = [
    "JobMatchResumeMCP",
    "ResumeOptimizer",
    "ATSChecker",
    "JobMarketIntelligence"
]
