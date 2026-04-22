# constants.py

INDUSTRIES = [
    "Software as a Service (SaaS)", "E-commerce", "Marketplace", "Healthcare / MedTech",
    "Finance / FinTech", "Education / EdTech", "Real Estate / PropTech", "Entertainment",
    "Social Media", "Hardware", "Artificial Intelligence (AI)", "Other"
]

BUSINESS_TYPES = [
    "B2B (Business to Business)", "B2C (Business to Consumer)", 
    "B2B2C", "C2C (Consumer to Consumer)", "D2C (Direct to Consumer)"
]

TECH_SKILL_LEVELS = [
    "Non-Technical", "Beginner", "Intermediate", "Advanced", "Expert"
]

CONFIDENCE_LABELS = {
    "HIGH": "High",
    "MEDIUM": "Medium",
    "LOW": "Low"
}

RISK_LEVEL_LABELS = {
    "LOW": "Low Risk",
    "MEDIUM": "Medium Risk",
    "HIGH": "High Risk",
    "EXTREME": "Extreme Risk"
}

CHART_PALETTE = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A", "#19D3F3", "#FF6692", "#B6E880"]

EXPORT_FORMATS = ["PDF", "DOCX", "JSON", "CSV"]

FALLBACK_COMPETITORS = {
    "Software as a Service (SaaS)": [
        {"name": "Established Enterprise Giant", "type": "Direct", "strengths": "Large budget, brand trust", "weaknesses": "Slow to innovate, expensive", "pricing_style": "High-tier subscription", "market_positioning": "Enterprise market leader"}
    ],
    "Artificial Intelligence (AI)": [
        {"name": "OpenAI / Anthropic", "type": "Indirect", "strengths": "State-of-the-art models", "weaknesses": "Lack of domain-specific workflow", "pricing_style": "Pay per token", "market_positioning": "Foundation model provider"}
    ]
}
