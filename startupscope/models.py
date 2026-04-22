import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class StartupInput(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    one_line_pitch: str
    description: str
    target_audience: str
    industry: str
    region: str
    budget: float
    team_size: int
    tech_skill_level: str
    business_type: str
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

class ExecutiveSummary(BaseModel):
    short_summary: str
    strongest_advantage: str
    biggest_risk: str
    recommendation: str
    pursue_score: int

class ProjectFeasibilityEstimate(BaseModel):
    estimated_mvp_build_time: str
    estimated_budget_required: str
    recommended_team_size: int
    difficulty_level: str
    estimated_time_to_market: str

class StartupScoreBreakdown(BaseModel):
    viability: int
    revenue_potential: int
    market_demand: int
    tech_difficulty: int
    competition: int
    scalability: int
    overall_score: int
    risk_level: str
    confidence_level: str
    score_reasoning: dict = Field(default_factory=dict)

class FounderReadinessScore(BaseModel):
    score: int
    explanation: str
    solo_founder_viability: str
    risk_indicator: str

class CompetitorItem(BaseModel):
    name: str
    type: str
    strengths: str
    weaknesses: str
    pricing_style: str
    market_positioning: str

class BusinessModelSuggestion(BaseModel):
    name: str
    fit_score: int
    explanation: str
    pros: List[str]
    cons: List[str]

class SWOTAnalysis(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]

class MVPFeature(BaseModel):
    name: str
    priority: str
    complexity: str
    description: str

class RiskAssessment(BaseModel):
    risk_name: str
    severity: str
    mitigation_strategy: str

class MarketOpportunity(BaseModel):
    tam_estimate: str
    target_customer_persona: str
    differentiation_opportunities: str

class GoToMarketPlan(BaseModel):
    short_term_strategy: str
    long_term_expansion: str
    marketing_channels: List[str]
    revenue_streams: List[str]

class NextSteps(BaseModel):
    recommended_mvp_features: List[str]
    best_first_customer_segment: str
    suggested_marketing_channels: List[str]
    suggested_monetization_model: str
    suggested_tech_stack: str
    first_30_day_execution_plan: str

class ValidationReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    version_id: int = 1
    generated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    analysis_mode: str
    input_data: StartupInput
    executive_summary: ExecutiveSummary
    feasibility_estimate: ProjectFeasibilityEstimate
    scores: StartupScoreBreakdown
    founder_readiness: FounderReadinessScore
    competitors: List[CompetitorItem]
    business_models: List[BusinessModelSuggestion]
    swot: SWOTAnalysis
    mvp_features: List[MVPFeature]
    risks: List[RiskAssessment]
    market_opportunity: MarketOpportunity
    go_to_market: GoToMarketPlan
    next_steps: NextSteps

class ComparisonReport(BaseModel):
    comparison_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    report_a: ValidationReport
    report_b: ValidationReport
    score_diff: dict
    budget_diff: dict

class ExportMetadata(BaseModel):
    filename: str
    format: str
    timestamp: str
    status: str
