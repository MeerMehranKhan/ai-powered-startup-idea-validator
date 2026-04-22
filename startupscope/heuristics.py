from startupscope.models import StartupInput, StartupScoreBreakdown, FounderReadinessScore, ExecutiveSummary, ProjectFeasibilityEstimate

def calculate_heuristic_scores(startup: StartupInput) -> StartupScoreBreakdown:
    # Base scores
    scores = {
        "viability": 50,
        "revenue_potential": 50,
        "market_demand": 50,
        "tech_difficulty": 50,
        "competition": 50,
        "scalability": 50
    }
    reasonings = {k: ["Started at baseline 50"] for k in scores}

    def adjust(metric, value, reason):
        scores[metric] += value
        sign = "+" if value > 0 else ""
        reasonings[metric].append(f"{sign}{value} {reason}")

    # Adjust based on business type
    b_type = startup.business_type.lower()
    if "b2b" in b_type:
        adjust("revenue_potential", 20, "Revenue Potential because B2B customers pay recurring subscription fees")
        adjust("viability", 10, "Viability because B2B solves concrete business problems")
        adjust("market_demand", 5, "Market Demand due to consistent need for B2B tools")
    if "b2c" in b_type:
        adjust("competition", 20, "Competition is usually higher in consumer-facing markets")
        adjust("scalability", 10, "Scalability because B2C has higher viral growth potential")
        adjust("revenue_potential", -10, "Revenue Potential as B2C monetization is often harder initially")
        
    # Adjust based on industry
    ind = startup.industry.lower()
    if "saas" in ind:
        adjust("scalability", 25, "Scalability because SaaS products can scale globally with low marginal cost")
        adjust("tech_difficulty", 10, "Tech Difficulty due to cloud architecture requirements")
        adjust("revenue_potential", 15, "Revenue Potential for recurring revenue model")
    if "marketplace" in ind:
        adjust("competition", 20, "Competition from existing network effects")
        adjust("viability", -15, "Viability due to the cold-start problem (supply vs demand)")
        adjust("scalability", 20, "Scalability once network effects are achieved")
    if "ai" in ind or "artificial intelligence" in ind:
        adjust("tech_difficulty", 30, "Tech Difficulty because AI development and integration requires specialized skills")
        adjust("market_demand", 25, "Market Demand due to high current market interest in AI solutions")
        adjust("competition", 15, "Competition as AI is a highly saturated space right now")
    if "e-commerce" in ind:
        adjust("competition", 25, "Competition from established e-commerce giants")
        adjust("tech_difficulty", -10, "Tech Difficulty as off-the-shelf e-commerce platforms exist")
        adjust("scalability", -10, "Scalability can be limited by physical logistics/inventory")
    if "healthcare" in ind or "fintech" in ind:
        adjust("tech_difficulty", 20, "Tech Difficulty due to strict regulatory and compliance requirements")
        adjust("viability", -10, "Viability due to high barriers to entry")
        adjust("revenue_potential", 15, "Revenue Potential due to high transaction values")

    # Adjust based on complexity of description
    desc_len = len(startup.description.split())
    if desc_len > 100:
        adjust("viability", 5, "Viability due to a well-thought-out and detailed concept")
    elif desc_len < 20:
        adjust("viability", -10, "Viability due to vague or overly brief description")
        
    # Adjust based on target audience
    aud = startup.target_audience.lower()
    if "enterprise" in aud or "corporate" in aud:
        adjust("revenue_potential", 15, "Revenue Potential for high-ticket enterprise clients")
        adjust("tech_difficulty", 15, "Tech Difficulty to meet enterprise security/compliance standards")
    elif "student" in aud or "teen" in aud:
        adjust("revenue_potential", -15, "Revenue Potential as younger audiences have lower willingness to pay")
        adjust("scalability", 15, "Scalability as younger demographics can drive fast viral growth")

    # Adjust based on tech skill of founder for general feasibility
    tech = startup.tech_skill_level.lower()
    if "expert" in tech or "advanced" in tech:
        adjust("tech_difficulty", -15, "Tech Difficulty lowered because founder has strong technical capabilities")
    elif "non-technical" in tech:
        adjust("tech_difficulty", 15, "Tech Difficulty increased because founder lacks direct technical skills")

    # Bounds check
    for k in scores:
        scores[k] = max(0, min(100, scores[k]))
        
    overall = int((scores["viability"] + scores["revenue_potential"] + scores["market_demand"] + (100 - scores["tech_difficulty"]) + (100 - scores["competition"]) + scores["scalability"]) / 6)
    
    risk_level = "Medium Risk"
    if scores["tech_difficulty"] > 80 or scores["competition"] > 80:
        risk_level = "High Risk"
    if overall > 75:
        risk_level = "Low Risk"
        
    final_reasonings = {k: " | ".join(v) for k, v in reasonings.items()}

    return StartupScoreBreakdown(
        viability=scores["viability"],
        revenue_potential=scores["revenue_potential"],
        market_demand=scores["market_demand"],
        tech_difficulty=scores["tech_difficulty"],
        competition=scores["competition"],
        scalability=scores["scalability"],
        overall_score=overall,
        risk_level=risk_level,
        confidence_level="Medium (Heuristic)",
        score_reasoning=final_reasonings
    )

def calculate_founder_readiness(startup: StartupInput, scores: StartupScoreBreakdown) -> FounderReadinessScore:
    score = 50
    reasons = []
    
    tech_level = startup.tech_skill_level.lower()
    if "expert" in tech_level or "advanced" in tech_level:
        score += 30
        reasons.append("+30 Founder Readiness because technical founders can execute efficiently")
    elif "non-technical" in tech_level:
        if startup.team_size == 1:
            score -= 20
            reasons.append("-20 Founder Readiness because solo non-technical founders may struggle with building and maintaining the product")
        else:
            score -= 10
            reasons.append("-10 Founder Readiness due to non-technical skills, but mitigated by having a team")
            
    if startup.budget < 5000 and scores.tech_difficulty > 70:
        score -= 15
        reasons.append("-15 Founder Readiness due to low budget for a highly technical project")
    elif startup.budget > 50000:
        score += 15
        reasons.append("+15 Founder Readiness due to sufficient capital to hire or outsource")
        
    if startup.team_size > 1:
        score += 10
        reasons.append("+10 Founder Readiness for having a multi-person team to share the workload")

    score = max(0, min(100, score))
    explanation = " | ".join(reasons) if reasons else "Average founder readiness."
    
    solo = "Viable"
    if startup.team_size == 1 and scores.tech_difficulty > 70 and "non-technical" in tech_level:
        solo = "Challenging"
    
    return FounderReadinessScore(
        score=score,
        explanation=explanation,
        solo_founder_viability=solo,
        risk_indicator="High" if score < 40 else "Medium" if score < 70 else "Low"
    )

def generate_heuristic_executive_summary(startup: StartupInput, scores: StartupScoreBreakdown) -> ExecutiveSummary:
    recommendation = []
    
    if scores.scalability > 70 and "saas" in startup.industry.lower():
        recommendation.append("This idea has strong long-term potential due to its scalability and recurring SaaS revenue model.")
    elif scores.overall_score > 70:
        recommendation.append("This idea shows strong potential with solid fundamentals.")
    else:
        recommendation.append("This concept requires careful validation as there are significant structural risks.")
        
    if scores.competition > 70:
        recommendation.append("However, the space is highly competitive, and execution quality will matter heavily.")
        
    if startup.team_size == 1 and "non-technical" in startup.tech_skill_level.lower():
        recommendation.append("A solo non-technical founder may struggle without a technical co-founder or outsourced development support.")
        
    rec_text = " ".join(recommendation) if recommendation else "Proceed with caution."

    return ExecutiveSummary(
        short_summary=f"{startup.name} is a {startup.industry} startup targeting {startup.target_audience}.",
        strongest_advantage="Market alignment" if scores.market_demand > 60 else "Scalability" if scores.scalability > 60 else "Niche focus",
        biggest_risk="High competition" if scores.competition > 70 else "Technical difficulty" if scores.tech_difficulty > 70 else "Unknown market demand",
        recommendation=rec_text,
        pursue_score=scores.overall_score
    )

def generate_heuristic_feasibility(startup: StartupInput, scores: StartupScoreBreakdown) -> ProjectFeasibilityEstimate:
    time = "3-6 months"
    if scores.tech_difficulty > 80:
        time = "9-12 months"
    elif scores.tech_difficulty < 30:
        time = "1-2 months"
        
    return ProjectFeasibilityEstimate(
        estimated_mvp_build_time=time,
        estimated_budget_required=f"${max(5000, scores.tech_difficulty * 200)} - ${scores.tech_difficulty * 500}",
        recommended_team_size=max(1, int(scores.tech_difficulty / 25)),
        difficulty_level="High" if scores.tech_difficulty > 70 else "Medium" if scores.tech_difficulty > 40 else "Low",
        estimated_time_to_market=time
    )
