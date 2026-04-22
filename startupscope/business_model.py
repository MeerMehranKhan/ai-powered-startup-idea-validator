from typing import List
from startupscope.models import StartupInput, BusinessModelSuggestion

def get_heuristic_business_models(startup: StartupInput) -> List[BusinessModelSuggestion]:
    models = []
    
    ind = startup.industry.lower()
    b_type = startup.business_type.lower()
    
    if "saas" in ind or "b2b" in b_type:
        models.append(BusinessModelSuggestion(
            name="Tiered Subscription (SaaS)",
            fit_score=90,
            explanation="Industry standard for B2B software, provides predictable recurring revenue.",
            pros=["Predictable revenue", "Scalable", "High valuation multiples"],
            cons=["High customer acquisition cost", "Requires constant updates"]
        ))
    
    if "marketplace" in ind or "c2c" in b_type:
        models.append(BusinessModelSuggestion(
            name="Commission / Take Rate",
            fit_score=95,
            explanation="Take a percentage of every transaction facilitated through the platform.",
            pros=["Scales with transaction volume", "Aligns incentives"],
            cons=["Hard to solve chicken-and-egg problem", "Platform leakage"]
        ))
        
    if not models:
        models.append(BusinessModelSuggestion(
            name="Freemium + Premium Features",
            fit_score=75,
            explanation="Offer core features for free to build user base, charge for advanced features.",
            pros=["Low barrier to entry", "Viral growth potential"],
            cons=["Low conversion rate", "Free users consume resources"]
        ))
        
    return models
