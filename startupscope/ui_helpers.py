import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
            /* Premium UI styling */
            .metric-card {
                background-color: #1e293b;
                border-radius: 8px;
                padding: 16px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                border: 1px solid #334155;
            }
            .metric-title {
                color: #94a3b8;
                font-size: 0.875rem;
                font-weight: 500;
                margin-bottom: 4px;
            }
            .metric-value {
                color: #f8fafc;
                font-size: 1.5rem;
                font-weight: 700;
            }
            .badge-low { background-color: #065f46; color: #a7f3d0; padding: 2px 8px; border-radius: 9999px; font-size: 0.75rem; }
            .badge-medium { background-color: #854d0e; color: #fef08a; padding: 2px 8px; border-radius: 9999px; font-size: 0.75rem; }
            .badge-high { background-color: #991b1b; color: #fecaca; padding: 2px 8px; border-radius: 9999px; font-size: 0.75rem; }
        </style>
    """, unsafe_allow_html=True)

def render_metric_card(title: str, value: str, risk_indicator: str = None):
    badge_html = ""
    if risk_indicator:
        level = risk_indicator.lower()
        if "low" in level: badge_class = "badge-low"
        elif "medium" in level: badge_class = "badge-medium"
        else: badge_class = "badge-high"
        badge_html = f"<span class='{badge_class}'>{risk_indicator}</span>"

    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{title} {badge_html}</div>
            <div class="metric-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)

def render_swot_matrix(swot):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🟢 Strengths")
        for s in swot.strengths: st.write(f"- {s}")
        st.subheader("🔵 Opportunities")
        for o in swot.opportunities: st.write(f"- {o}")
    with col2:
        st.subheader("🔴 Weaknesses")
        for w in swot.weaknesses: st.write(f"- {w}")
        st.subheader("🟠 Threats")
        for t in swot.threats: st.write(f"- {t}")

def render_competitors_table(competitors):
    for comp in competitors:
        with st.expander(f"{comp.name} ({comp.type})"):
            st.markdown(f"**Market Positioning:** {comp.market_positioning}")
            st.markdown(f"**Strengths:** {comp.strengths}")
            st.markdown(f"**Weaknesses:** {comp.weaknesses}")
            st.markdown(f"**Pricing Style:** {comp.pricing_style}")
