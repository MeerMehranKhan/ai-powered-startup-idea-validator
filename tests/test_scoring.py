import pytest
from startupscope.models import StartupInput
from startupscope.heuristics import calculate_heuristic_scores, calculate_founder_readiness
from startupscope.scoring import generate_fallback_report

@pytest.fixture
def sample_startup():
    return StartupInput(
        name="Test",
        one_line_pitch="Pitch",
        description="Desc",
        target_audience="Devs",
        industry="Software as a Service (SaaS)",
        region="Global",
        budget=10000,
        team_size=2,
        tech_skill_level="Expert",
        business_type="B2B (Business to Business)"
    )

def test_heuristic_scoring_saas_b2b(sample_startup):
    scores = calculate_heuristic_scores(sample_startup)
    assert scores.scalability >= 80 # SaaS heuristic boosts scalability
    assert scores.revenue_potential >= 70 # B2B boosts revenue potential

def test_founder_readiness_expert(sample_startup):
    scores = calculate_heuristic_scores(sample_startup)
    readiness = calculate_founder_readiness(sample_startup, scores)
    assert readiness.score > 70
    assert "Medium" in readiness.risk_indicator or "Low" in readiness.risk_indicator

def test_generate_fallback_report(sample_startup):
    report = generate_fallback_report(sample_startup)
    assert report.input_data.name == "Test"
    assert report.analysis_mode == "Local Heuristic Analysis"
    assert len(report.swot.strengths) > 0
    assert len(report.competitors) > 0
