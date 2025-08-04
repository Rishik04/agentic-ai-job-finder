class JobMarketIntelligence:
    async def generate_market_insights(self, user_skills, target_roles):
        return {
            "salary_insights": {
                "median_salary": 120000,
                "salary_range": [90000, 150000],
                "growth_trend": "+12% YoY"
            },
            "skill_gaps": {
                "high_demand_skills": ["ML Ops", "Data Engineering"],
                "declining_skills": ["Flash"],
                "recommended_to_learn": ["LangChain", "Docker"]
            },
            "location_insights": {
                "best_markets": ["Bangalore", "Hyderabad"],
                "remote_percentage": 65,
                "competition_level": "Moderate"
            },
            "hiring_trends": {
                "top_hiring_companies": ["Google", "TCS", "Infosys"],
                "industry_growth": ["AI", "Healthcare Tech"],
                "hiring_timeline": "Peak in Q1/Q3"
            }
        }