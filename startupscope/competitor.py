from typing import List
from startupscope.models import StartupInput, CompetitorItem
from startupscope.constants import FALLBACK_COMPETITORS

def get_heuristic_competitors(startup: StartupInput) -> List[CompetitorItem]:
    ind = startup.industry
    if ind in FALLBACK_COMPETITORS:
        return [CompetitorItem(**comp) for comp in FALLBACK_COMPETITORS[ind]]
    
    # Generic competitor
    return [
        CompetitorItem(
            name="Incumbent Solutions",
            type="Direct",
            strengths="Established user base, more resources",
            weaknesses="Slow, poor UX, outdated tech",
            pricing_style="Expensive Enterprise",
            market_positioning="Legacy leader"
        )
    ]
