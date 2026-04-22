# prompts.py

SYSTEM_PROMPT = """You are a world-class Startup Analyst, Product Manager, and Technical Architect.
Your job is to objectively analyze a startup idea and provide a highly detailed, brutally honest evaluation.
You must return the result ONLY as a valid JSON object matching the exact schema requested.
DO NOT wrap the JSON in markdown formatting (like ```json), just return the raw JSON object.
"""

def build_analysis_prompt(startup_dict: dict) -> str:
    return f"""
Analyze the following startup idea:
Name: {startup_dict['name']}
Pitch: {startup_dict['one_line_pitch']}
Description: {startup_dict['description']}
Target Audience: {startup_dict['target_audience']}
Industry: {startup_dict['industry']}
Region: {startup_dict['region']}
Budget: ${startup_dict['budget']}
Team Size: {startup_dict['team_size']}
Tech Skill: {startup_dict['tech_skill_level']}
Business Type: {startup_dict['business_type']}

You must return a single JSON object with the exact keys and structure below. Make the analysis actionable, realistic, and insightful.

{{
    "executive_summary": {{
        "short_summary": "2-3 sentences max",
        "strongest_advantage": "Short phrase",
        "biggest_risk": "Short phrase",
        "recommendation": "Clear actionable advice",
        "pursue_score": 85
    }},
    "feasibility_estimate": {{
        "estimated_mvp_build_time": "e.g., 3 months",
        "estimated_budget_required": "e.g., $10k - $20k",
        "recommended_team_size": 2,
        "difficulty_level": "Medium",
        "estimated_time_to_market": "e.g., 4 months"
    }},
    "scores": {{
        "viability": 75,
        "revenue_potential": 80,
        "market_demand": 70,
        "tech_difficulty": 60,
        "competition": 85,
        "scalability": 90,
        "overall_score": 76,
        "risk_level": "Medium Risk",
        "confidence_level": "High",
        "score_reasoning": {{
            "viability": "Reasoning for viability score",
            "revenue_potential": "Reasoning for revenue potential score",
            "market_demand": "Reasoning for market demand",
            "tech_difficulty": "Reasoning for tech difficulty",
            "competition": "Reasoning for competition",
            "scalability": "Reasoning for scalability"
        }}
    }},
    "founder_readiness": {{
        "score": 65,
        "explanation": "Why this founder (based on team size/skills) is ready or not",
        "solo_founder_viability": "Viable or Challenging",
        "risk_indicator": "Medium"
    }},
    "competitors": [
        {{
            "name": "Competitor 1",
            "type": "Direct or Indirect",
            "strengths": "...",
            "weaknesses": "...",
            "pricing_style": "...",
            "market_positioning": "..."
        }}
    ],
    "business_models": [
        {{
            "name": "SaaS Subscription",
            "fit_score": 90,
            "explanation": "Why it fits",
            "pros": ["pro1", "pro2"],
            "cons": ["con1", "con2"]
        }}
    ],
    "swot": {{
        "strengths": ["s1", "s2"],
        "weaknesses": ["w1", "w2"],
        "opportunities": ["o1", "o2"],
        "threats": ["t1", "t2"]
    }},
    "mvp_features": [
        {{
            "name": "Feature 1",
            "priority": "High",
            "complexity": "Medium",
            "description": "What it does"
        }}
    ],
    "risks": [
        {{
            "risk_name": "Risk 1",
            "severity": "High",
            "mitigation_strategy": "How to fix"
        }}
    ],
    "market_opportunity": {{
        "tam_estimate": "e.g. $5B",
        "target_customer_persona": "Description",
        "differentiation_opportunities": "How to stand out"
    }},
    "go_to_market": {{
        "short_term_strategy": "...",
        "long_term_expansion": "...",
        "marketing_channels": ["c1", "c2"],
        "revenue_streams": ["r1", "r2"]
    }},
    "next_steps": {{
        "recommended_mvp_features": ["f1", "f2"],
        "best_first_customer_segment": "...",
        "suggested_marketing_channels": ["c1", "c2"],
        "suggested_monetization_model": "...",
        "suggested_tech_stack": "...",
        "first_30_day_execution_plan": "..."
    }}
}}
"""
