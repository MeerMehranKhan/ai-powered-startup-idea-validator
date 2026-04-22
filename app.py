import streamlit as st
import json
from startupscope.models import StartupInput, ValidationReport
from startupscope.validators import validate_startup_input
from startupscope.analysis import analyze_startup
from startupscope.storage import save_report, get_all_reports, delete_report
from startupscope.report_generator import generate_report_file
from startupscope.ui_helpers import inject_custom_css, render_metric_card, render_swot_matrix, render_competitors_table
from startupscope.charts import create_radar_chart, create_bar_chart
from startupscope.constants import INDUSTRIES, BUSINESS_TYPES, TECH_SKILL_LEVELS
from startupscope.config import Config

st.set_page_config(page_title="StartupScope AI", layout="wide", initial_sidebar_state="expanded")
inject_custom_css()

# Session State Initialization
if 'current_report' not in st.session_state:
    st.session_state.current_report = None
if 'history_reports' not in st.session_state:
    st.session_state.history_reports = get_all_reports()

def load_sample():
    st.session_state.sample_name = "DogWalker Pro"
    st.session_state.sample_pitch = "Uber for dog walking"
    st.session_state.sample_desc = "An on-demand mobile app that connects busy professionals with vetted local dog walkers."
    st.session_state.sample_audience = "Busy professionals with dogs"

def render_sidebar():
    with st.sidebar:
        st.title("StartupScope AI")
        st.info(f"Analysis Mode: **{Config.get_analysis_mode()}**")
        
        st.header("History")
        if not st.session_state.history_reports:
            st.write("No saved reports.")
        else:
            for rep in st.session_state.history_reports:
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button(f"{rep.input_data.name[:15]} ({rep.scores.overall_score})", key=f"load_{rep.report_id}"):
                        st.session_state.current_report = rep
                with col2:
                    if st.button("🗑️", key=f"del_{rep.report_id}"):
                        delete_report(rep.report_id)
                        st.session_state.history_reports = get_all_reports()
                        st.rerun()

def render_input_section():
    st.header("Validate Your Startup Idea")
    
    st.button("Load Sample Idea", on_click=load_sample)
    
    with st.form("startup_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Startup Name", value=st.session_state.get('sample_name', ''))
            pitch = st.text_input("One-Line Pitch", value=st.session_state.get('sample_pitch', ''))
            industry = st.selectbox("Industry", INDUSTRIES)
            b_type = st.selectbox("Business Type", BUSINESS_TYPES)
        with col2:
            target_aud = st.text_input("Target Audience", value=st.session_state.get('sample_audience', ''))
            budget = st.number_input("Estimated Budget ($)", min_value=0, value=5000, step=1000)
            team_size = st.number_input("Team Size", min_value=1, value=1, step=1)
            tech_skill = st.selectbox("Technical Skill Level", TECH_SKILL_LEVELS)
            
        desc = st.text_area("Detailed Description", value=st.session_state.get('sample_desc', ''))
        
        submitted = st.form_submit_button("Analyze Idea")
        if submitted:
            try:
                raw_data = {
                    "name": name,
                    "one_line_pitch": pitch,
                    "description": desc,
                    "target_audience": target_aud,
                    "industry": industry,
                    "region": "Global",
                    "budget": float(budget),
                    "team_size": int(team_size),
                    "tech_skill_level": tech_skill,
                    "business_type": b_type
                }
                valid_data = validate_startup_input(raw_data)
                startup_input = StartupInput(**valid_data)
                
                with st.spinner("Analyzing startup idea..."):
                    report = analyze_startup(startup_input)
                    st.session_state.current_report = report
                    save_report(report)
                    st.session_state.history_reports = get_all_reports()
                
            except ValueError as e:
                st.error(str(e))

def render_dashboard(report: ValidationReport):
    st.header(f"Validation Report: {report.input_data.name}")
    
    # Executive Summary (Always top)
    st.markdown("### Executive Summary")
    st.info(report.executive_summary.short_summary)
    st.success(f"**Recommendation:** {report.executive_summary.recommendation}")
    
    # Top Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1: render_metric_card("Overall Score", f"{report.scores.overall_score}/100", report.scores.risk_level)
    with col2: render_metric_card("Founder Readiness", f"{report.founder_readiness.score}/100", report.founder_readiness.risk_indicator)
    with col3: render_metric_card("Est. Budget", report.feasibility_estimate.estimated_budget_required)
    with col4: render_metric_card("Time to Market", report.feasibility_estimate.estimated_time_to_market)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Scores & Analysis", "SWOT & Market", "Competitors & Models", "MVP & Risks", "Next Steps"])
    
    with tab1:
        c1, c2 = st.columns(2)
        with c1: st.plotly_chart(create_radar_chart(report.scores), use_container_width=True)
        with c2: st.plotly_chart(create_bar_chart(report.scores), use_container_width=True)
            
    with tab2:
        render_swot_matrix(report.swot)
        st.divider()
        st.subheader("Market Opportunity")
        st.write(f"**TAM Estimate:** {report.market_opportunity.tam_estimate}")
        st.write(f"**Target Persona:** {report.market_opportunity.target_customer_persona}")
        
    with tab3:
        st.subheader("Competitors")
        render_competitors_table(report.competitors)
        st.divider()
        st.subheader("Suggested Business Models")
        for bm in report.business_models:
            with st.expander(f"{bm.name} (Fit: {bm.fit_score})"):
                st.write(bm.explanation)
                
    with tab4:
        st.subheader("MVP Features")
        for f in report.mvp_features:
            st.write(f"- **{f.name}** ({f.priority} priority, {f.complexity} complexity): {f.description}")
        st.divider()
        st.subheader("Risk Assessment")
        for r in report.risks:
            st.warning(f"**{r.risk_name}** ({r.severity}): {r.mitigation_strategy}")
            
    with tab5:
        st.subheader("Next Steps")
        st.write(f"**First 30 Days:** {report.next_steps.first_30_day_execution_plan}")
        st.write(f"**Tech Stack:** {report.next_steps.suggested_tech_stack}")
        st.write(f"**Marketing:** {', '.join(report.next_steps.suggested_marketing_channels)}")
        
        st.divider()
        st.subheader("Export Report")
        ec1, ec2, ec3, ec4 = st.columns(4)
        if ec1.button("Export PDF"):
            meta = generate_report_file(report, "pdf")
            st.success(f"Generated {meta.filename}")
        if ec2.button("Export DOCX"):
            meta = generate_report_file(report, "docx")
            st.success(f"Generated {meta.filename}")
        if ec3.button("Export JSON"):
            meta = generate_report_file(report, "json")
            st.success(f"Generated {meta.filename}")

render_sidebar()
if st.session_state.current_report is None:
    render_input_section()
else:
    if st.button("← New Idea"):
        st.session_state.current_report = None
        st.rerun()
    render_dashboard(st.session_state.current_report)
