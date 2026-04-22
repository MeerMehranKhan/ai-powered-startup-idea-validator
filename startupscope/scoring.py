from startupscope.models import StartupInput, ValidationReport, SWOTAnalysis, MVPFeature, RiskAssessment, MarketOpportunity, GoToMarketPlan, NextSteps
from startupscope.heuristics import calculate_heuristic_scores, calculate_founder_readiness, generate_heuristic_executive_summary, generate_heuristic_feasibility
from startupscope.competitor import get_heuristic_competitors
from startupscope.business_model import get_heuristic_business_models

def generate_fallback_report(startup: StartupInput) -> ValidationReport:
    """Generates a complete report using the heuristic engine when APIs are unavailable or fail."""
    
    scores = calculate_heuristic_scores(startup)
    founder_readiness = calculate_founder_readiness(startup, scores)
    exec_summary = generate_heuristic_executive_summary(startup, scores)
    feasibility = generate_heuristic_feasibility(startup, scores)
    competitors = get_heuristic_competitors(startup)
    business_models = get_heuristic_business_models(startup)
    
    swot = SWOTAnalysis(
        strengths=["Clear market focus", "Heuristic-detected potential"],
        weaknesses=["Unvalidated assumptions", "Potential execution risks"],
        opportunities=["Expand target audience", "Add premium features"],
        threats=["Market saturation", "Changing consumer trends"]
    )
    
    mvp_features = [
        MVPFeature(name="Core User Flow", priority="High", complexity="Medium", description="The main value proposition feature."),
        MVPFeature(name="Authentication", priority="High", complexity="Low", description="Secure user login and profiles."),
        MVPFeature(name="Payments", priority="Medium", complexity="High", description="Stripe integration for revenue generation.")
    ]
    
    risks = [
        RiskAssessment(risk_name="Execution Risk", severity="Medium", mitigation_strategy="Focus on a single, well-defined MVP."),
        RiskAssessment(risk_name="Market Adoption", severity="High", mitigation_strategy="Conduct user interviews before coding.")
    ]
    
    market_opp = MarketOpportunity(
        tam_estimate="$1B+ (Heuristic Estimate)",
        target_customer_persona=f"Individuals in {startup.industry} seeking {startup.one_line_pitch}",
        differentiation_opportunities="Superior UX, hyper-niche targeting"
    )
    
    gtm = GoToMarketPlan(
        short_term_strategy="Leverage organic social media and content marketing.",
        long_term_expansion="Paid acquisition and strategic partnerships.",
        marketing_channels=["LinkedIn", "Twitter/X", "SEO", "Direct Outreach"],
        revenue_streams=["Primary subscriptions/commissions", "Optional premium support"]
    )
    
    next_steps = NextSteps(
        recommended_mvp_features=["Core User Flow", "Landing Page"],
        best_first_customer_segment="Early adopters in immediate network",
        suggested_marketing_channels=["Organic Social", "Cold Email"],
        suggested_monetization_model=business_models[0].name if business_models else "Freemium",
        suggested_tech_stack="Streamlit/Next.js + Python/Node.js backend",
        first_30_day_execution_plan="Validate with 10 users -> Build Landing Page -> Collect pre-signups -> Develop MVP."
    )

    return ValidationReport(
        analysis_mode="Local Heuristic Analysis",
        input_data=startup,
        executive_summary=exec_summary,
        feasibility_estimate=feasibility,
        scores=scores,
        founder_readiness=founder_readiness,
        competitors=competitors,
        business_models=business_models,
        swot=swot,
        mvp_features=mvp_features,
        risks=risks,
        market_opportunity=market_opp,
        go_to_market=gtm,
        next_steps=next_steps
    )
