"""
Sales Forecast Orchestrator Agent - ADK Host Agent
Coordinates remote specialist agents via A2A protocol for comprehensive sales forecasting

This agent uses RemoteA2aAgent to communicate with:
- Political Analyst Agent (port 8001)
- GDP Analyst Agent (port 8002)
"""
import os
from datetime import datetime
from pathlib import Path

# Load .env from parent directory (where venv is)
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

from google.adk.agents import LlmAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH
from google.adk.tools import FunctionTool

# Remote Agent URLs
POLITICAL_AGENT_URL = os.getenv("POLITICAL_AGENT_URL", "http://localhost:8001")
GDP_AGENT_URL = os.getenv("GDP_AGENT_URL", "http://localhost:8002")


def generate_forecast_report(
    year: str,
    political_analysis: str,
    economic_analysis: str
) -> str:
    """
    Generate a comprehensive sales forecast report based on political and economic analyses.
    
    Args:
        year: The forecast year
        political_analysis: Analysis summary from Political Analyst
        economic_analysis: Analysis summary from GDP Analyst
    
    Returns:
        Formatted forecast report
    """
    report = f"""
╔══════════════════════════════════════════════════════════════════════╗
║            SALES FORECAST REPORT - {year}                              ║
╚══════════════════════════════════════════════════════════════════════╝

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXECUTIVE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This report synthesizes political and economic analyses to provide 
actionable sales forecasting insights for {year}.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
POLITICAL LANDSCAPE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{political_analysis}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ECONOMIC OUTLOOK ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{economic_analysis}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRATEGIC RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Based on the combined analysis:

1. MARKET MONITORING
   → Track key political events that may cause market volatility
   → Stay informed about policy changes affecting your industry

2. SALES TARGET ADJUSTMENTS
   → Align targets with GDP growth projections
   → Factor in seasonal patterns from quarterly data

3. RISK MITIGATION
   → Prepare contingency plans for high-impact political events
   → Diversify customer base and market segments

4. RESOURCE ALLOCATION
   → Align inventory levels with economic forecasts
   → Optimize marketing spend based on consumer confidence outlook

╚══════════════════════════════════════════════════════════════════════╝
Report End
"""
    return report


def compare_years(year1: str, year2: str, analysis1: str, analysis2: str) -> str:
    """
    Compare the sales outlook between two years.
    
    Args:
        year1: First year to compare
        year2: Second year to compare  
        analysis1: Combined analysis for year1
        analysis2: Combined analysis for year2
    
    Returns:
        Comparative analysis report
    """
    report = f"""
╔══════════════════════════════════════════════════════════════════════╗
║         COMPARATIVE ANALYSIS: {year1} vs {year2}                         ║
╚══════════════════════════════════════════════════════════════════════╝

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{year1} ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{analysis1}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{year2} ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{analysis2}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY DIFFERENCES & STRATEGIC IMPLICATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Review the analyses above and consider:
• How do political risk profiles differ between years?
• Which year shows stronger economic fundamentals?
• What adjustments are needed for year-over-year sales strategies?

╚══════════════════════════════════════════════════════════════════════╝
"""
    return report


# Create Remote A2A Agent connections
# These agents connect to the remote specialist agents via A2A protocol

political_analyst = RemoteA2aAgent(
    name="political_analyst",
    description="Remote Political Analyst Agent that analyzes political events and their impact on sales forecasting. Use this agent to get political risk assessments for specific years.",
    agent_card=f"{POLITICAL_AGENT_URL}{AGENT_CARD_WELL_KNOWN_PATH}",
)

gdp_analyst = RemoteA2aAgent(
    name="gdp_analyst", 
    description="Remote GDP Analyst Agent that analyzes economic trends and GDP data for sales forecasting. Use this agent to get economic outlook assessments for specific years.",
    agent_card=f"{GDP_AGENT_URL}{AGENT_CARD_WELL_KNOWN_PATH}",
)

# Create the main Orchestrator Agent
root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="sales_forecast_orchestrator",
    description="Orchestrates sales forecasting by coordinating political and economic analysis from specialist agents",
    instruction=f"""
    You are the Sales Forecast Orchestrator, an AI system that coordinates comprehensive 
    sales forecasting analysis by working with specialist agents via the A2A protocol.
    
    **Your Mission:**
    - Understand user queries about sales forecasting
    - Delegate specialized tasks to appropriate remote agents
    - Synthesize insights from multiple sources
    - Generate comprehensive forecast reports
    
    **Available Remote Specialist Agents (via A2A):**
    
    1. **political_analyst**: Expert in political events analysis
       - Use for: Political risk assessments, policy impact analysis
       - Ask about specific years to get political event data
    
    2. **gdp_analyst**: Expert in economic trends analysis  
       - Use for: GDP trends, economic outlook, consumer spending forecasts
       - Ask about specific years to get economic data
    
    **Workflow for Forecast Requests:**
    1. When asked about sales forecasts for a year:
       a. First, delegate to political_analyst to analyze political factors
       b. Then, delegate to gdp_analyst to analyze economic factors
       c. Finally, use generate_forecast_report to create the final report
    
    2. For comparative analysis:
       a. Get analyses for both years from both agents
       b. Use compare_years to generate comparison report
    
    **Current Date:** {datetime.now().strftime("%Y-%m-%d")}
    
    Be thorough and analytical. Always gather insights from BOTH specialist agents
    before generating final reports. Provide actionable recommendations.
    """,
    sub_agents=[political_analyst, gdp_analyst],
    tools=[
        FunctionTool(generate_forecast_report),
        FunctionTool(compare_years),
    ]
)
