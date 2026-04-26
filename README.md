# Smart Startup Idea Validator

It is a premium, AI-powered startup idea validation platform. It allows founders, product managers, and builders to input a startup concept and receive a comprehensive, data-driven business analysis report.

Whether you are validating a SaaS product, a marketplace, or a local service, it helps you answer:

- Is this startup idea worth pursuing?
- What are the risks and the recommended MVP scope?
- Who are my competitors, and what is the best business model?
- Do I have the technical skills, budget, and founder readiness to pull this off?

## Features

- **AI-Powered & Heuristic Fallback:** Uses OpenAI or Anthropic models for deep, nuanced analysis. If no API keys are provided, it smoothly falls back to a sophisticated rule-based heuristic engine.
- **Premium UI:** Dashboard-style Streamlit interface with sticky metric cards, side-by-side comparison mode, and Plotly visualizations (radar charts, bar charts).
- **Comprehensive Reports:** Generates Executive Summaries, SWOT analysis, Competitor Breakdowns, Business Models, Risk Assessments, and Next Steps.
- **Exporting:** Download timestamped reports as PDF, DOCX, JSON, or CSV.
- **History & Versioning:** Saves past analyses locally using SQLite. You can search, filter, reload, and compare past startup ideas.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/MeerMehranKhan/ai-powered-startup-idea-validator.git
   cd ai-powered-startup-idea-validator
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

## Architecture

The project follows a clean, modular architecture:

- `startupscope/models.py`: Pydantic models enforcing strict schemas.
- `startupscope/heuristics.py`: Rule-based scoring engine for fallback mode.
- `startupscope/analysis.py`: LLM orchestration with retry/fallback logic.
- `startupscope/storage.py`: SQLite-backed history tracking and versioning.
- `startupscope/ui_helpers.py` & `charts.py`: Custom Streamlit UI components.

## Export Details

Generated reports are stored locally in the `exports/` folder categorized by type (pdf, docx, json, csv), ensuring you never lose a generated file.
