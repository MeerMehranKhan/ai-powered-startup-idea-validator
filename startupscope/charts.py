import plotly.graph_objects as go
import plotly.express as px
from startupscope.models import StartupScoreBreakdown
from startupscope.constants import CHART_PALETTE

def get_score_color(val: int) -> str:
    if val < 40:
        return '#ef4444' # Red
    elif val < 70:
        return '#eab308' # Yellow
    else:
        return '#22c55e' # Green

def create_radar_chart(scores: StartupScoreBreakdown) -> go.Figure:
    categories = ['Viability', 'Revenue Potential', 'Market Demand', 'Tech Difficulty', 'Competition', 'Scalability']
    values = [
        scores.viability, 
        scores.revenue_potential, 
        scores.market_demand, 
        scores.tech_difficulty, 
        scores.competition, 
        scores.scalability
    ]
    colors = [get_score_color(v) for v in values]
    
    reasoning = getattr(scores, 'score_reasoning', {})
    if not isinstance(reasoning, dict):
        reasoning = {}
        
    def break_text(text, n=60):
        if not text: return "No reasoning provided"
        # simple word wrap for tooltips
        words = text.split()
        lines, current = [], []
        length = 0
        for w in words:
            if length + len(w) > n:
                lines.append(" ".join(current))
                current = [w]
                length = len(w)
            else:
                current.append(w)
                length += len(w) + 1
        lines.append(" ".join(current))
        return "<br>".join(lines)

    hover_texts = [
        f"<b>{categories[0]}: {values[0]}</b><br>{break_text(reasoning.get('viability', 'No reasoning provided'))}",
        f"<b>{categories[1]}: {values[1]}</b><br>{break_text(reasoning.get('revenue_potential', 'No reasoning provided'))}",
        f"<b>{categories[2]}: {values[2]}</b><br>{break_text(reasoning.get('market_demand', 'No reasoning provided'))}",
        f"<b>{categories[3]}: {values[3]}</b><br>{break_text(reasoning.get('tech_difficulty', 'No reasoning provided'))}",
        f"<b>{categories[4]}: {values[4]}</b><br>{break_text(reasoning.get('competition', 'No reasoning provided'))}",
        f"<b>{categories[5]}: {values[5]}</b><br>{break_text(reasoning.get('scalability', 'No reasoning provided'))}"
    ]
    
    fig = go.Figure()
    
    # Baseline at 50
    fig.add_trace(go.Scatterpolar(
        r=[50] * 7,
        theta=categories + [categories[0]],
        mode='lines',
        line=dict(color='gray', dash='dot', width=1),
        hoverinfo='skip',
        showlegend=False,
        name='Baseline 50'
    ))
    
    # Actual values
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        mode='lines+markers+text',
        marker=dict(
            color=colors + [colors[0]],
            size=10,
            line=dict(color='white', width=1)
        ),
        line_color=CHART_PALETTE[0] if CHART_PALETTE else '#3b82f6',
        text=values + [values[0]],
        textposition="top center",
        hovertext=hover_texts + [hover_texts[0]],
        hoverinfo="text",
        name='Score'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], color="#94a3b8", tickfont=dict(size=10)),
            angularaxis=dict(color="#e2e8f0", tickfont=dict(size=12, weight="bold"))
        ),
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0")
    )
    return fig

def create_bar_chart(scores: StartupScoreBreakdown) -> go.Figure:
    categories = ['Viability', 'Revenue Potential', 'Market Demand', 'Tech Difficulty', 'Competition', 'Scalability']
    values = [
        scores.viability, 
        scores.revenue_potential, 
        scores.market_demand, 
        scores.tech_difficulty, 
        scores.competition, 
        scores.scalability
    ]
    colors = [get_score_color(v) for v in values]
    
    reasoning = getattr(scores, 'score_reasoning', {})
    if not isinstance(reasoning, dict):
        reasoning = {}
        
    def break_text(text, n=60):
        if not text: return "No reasoning provided"
        words = text.split()
        lines, current = [], []
        length = 0
        for w in words:
            if length + len(w) > n:
                lines.append(" ".join(current))
                current = [w]
                length = len(w)
            else:
                current.append(w)
                length += len(w) + 1
        lines.append(" ".join(current))
        return "<br>".join(lines)

    hover_texts = [
        f"<b>{categories[0]}: {values[0]}</b><br>{break_text(reasoning.get('viability', 'No reasoning provided'))}",
        f"<b>{categories[1]}: {values[1]}</b><br>{break_text(reasoning.get('revenue_potential', 'No reasoning provided'))}",
        f"<b>{categories[2]}: {values[2]}</b><br>{break_text(reasoning.get('market_demand', 'No reasoning provided'))}",
        f"<b>{categories[3]}: {values[3]}</b><br>{break_text(reasoning.get('tech_difficulty', 'No reasoning provided'))}",
        f"<b>{categories[4]}: {values[4]}</b><br>{break_text(reasoning.get('competition', 'No reasoning provided'))}",
        f"<b>{categories[5]}: {values[5]}</b><br>{break_text(reasoning.get('scalability', 'No reasoning provided'))}"
    ]
    
    fig = px.bar(x=categories, y=values, color=categories, color_discrete_sequence=colors)
    fig.update_traces(
        text=values, 
        textposition='outside',
        hovertext=hover_texts,
        hoverinfo="text"
    )
    
    # Add a baseline
    fig.add_hline(y=50, line_dash="dot", line_color="gray", annotation_text="Average (50)")

    fig.update_layout(
        xaxis_title="", 
        yaxis_title="Score", 
        yaxis=dict(range=[0, 100]),
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"),
        showlegend=False
    )
    return fig
