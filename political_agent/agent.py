"""
Political Analyst Agent - A2A Enabled Remote Agent
Uses ADK with MCP tools to analyze political events for sales forecasting

This agent connects to the MCP server to fetch political event data
and provides analysis via A2A protocol
"""
import os
import json
import httpx
from datetime import datetime
from pathlib import Path

# Load .env from the same directory as this file
from dotenv import load_dotenv
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.adk.a2a.utils.agent_to_a2a import to_a2a

# MCP Server URL
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp")


async def get_political_events_from_mcp(year: str, impact_level: str = "all") -> str:
    """
    Fetch political events from MCP server.
    
    Args:
        year: The year to analyze (e.g., "2024", "2025")
        impact_level: Filter by impact - "high", "medium", "low", or "all"
    
    Returns:
        JSON string with political events data
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Call MCP tool via HTTP
            response = await client.post(
                MCP_SERVER_URL,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {
                        "name": "get_political_events",
                        "arguments": {
                            "year": year,
                            "impact_level": impact_level
                        }
                    }
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if "result" in result and "content" in result["result"]:
                    for content in result["result"]["content"]:
                        if content.get("type") == "text":
                            return content.get("text", "{}")
                return json.dumps({"error": "Unexpected response format", "raw": result})
            else:
                return json.dumps({
                    "error": f"MCP server returned status {response.status_code}",
                    "year": year
                })
    except Exception as e:
        # Fallback to mock data if MCP server is unavailable
        return _get_mock_political_data(year, impact_level)


def _get_mock_political_data(year: str, impact_level: str) -> str:
    """Fallback mock data when MCP server is unavailable"""
    mock_events = {
        "2024": [
            {"date": "2024-11-05", "event": "US Presidential Election", "impact": "high"},
            {"date": "2024-03-20", "event": "Federal Reserve Policy Meeting", "impact": "high"},
        ],
        "2025": [
            {"date": "2025-01-20", "event": "Presidential Inauguration", "impact": "high"},
            {"date": "2025-04-15", "event": "Tax Policy Changes", "impact": "medium"},
        ],
        "2026": [
            {"date": "2026-11-03", "event": "Midterm Elections", "impact": "high"},
            {"date": "2026-06-20", "event": "Trade Agreement Negotiations", "impact": "high"},
        ]
    }
    
    events = mock_events.get(year, [])
    if impact_level != "all":
        events = [e for e in events if e["impact"] == impact_level]
    
    return json.dumps({
        "year": year,
        "impact_filter": impact_level,
        "event_count": len(events),
        "events": events,
        "source": "mock_fallback",
        "retrieved_at": datetime.now().isoformat()
    }, indent=2)


def analyze_political_impact(year: str, events_data: str) -> str:
    """
    Analyze the political impact on sales based on event data.
    
    Args:
        year: The year being analyzed
        events_data: JSON string containing political events
    
    Returns:
        Analysis report as a string
    """
    try:
        data = json.loads(events_data)
        events = data.get("events", [])
        
        high_impact = [e for e in events if e.get("impact") == "high"]
        medium_impact = [e for e in events if e.get("impact") == "medium"]
        
        risk_score = min(len(high_impact) * 25 + len(medium_impact) * 10, 100)
        
        analysis = {
            "year": year,
            "political_risk_score": risk_score,
            "high_impact_events": len(high_impact),
            "medium_impact_events": len(medium_impact),
            "key_events": [e.get("event") for e in high_impact],
            "analysis_summary": _generate_political_summary(high_impact, risk_score),
            "sales_impact_forecast": _get_sales_impact(risk_score),
            "analyzed_at": datetime.now().isoformat()
        }
        
        return json.dumps(analysis, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "year": year})


def _generate_political_summary(high_impact_events: list, risk_score: int) -> str:
    """Generate a summary of political impact"""
    if risk_score >= 70:
        return f"HIGH POLITICAL RISK: {len(high_impact_events)} major events may significantly impact market conditions"
    elif risk_score >= 40:
        return f"MODERATE POLITICAL RISK: {len(high_impact_events)} notable events require monitoring"
    else:
        return f"LOW POLITICAL RISK: Political environment appears stable for sales operations"


def _get_sales_impact(risk_score: int) -> dict:
    """Get sales impact forecast based on risk score"""
    if risk_score >= 70:
        return {
            "impact_level": "significant",
            "recommendation": "Prepare contingency plans and diversify strategies",
            "expected_volatility": "high"
        }
    elif risk_score >= 40:
        return {
            "impact_level": "moderate",
            "recommendation": "Monitor developments and maintain flexibility",
            "expected_volatility": "medium"
        }
    else:
        return {
            "impact_level": "minimal",
            "recommendation": "Proceed with standard sales strategies",
            "expected_volatility": "low"
        }


# Create the Political Analyst ADK Agent
root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="political_analyst_agent",
    description="Expert political analyst that assesses political events and their impact on sales forecasting",
    instruction="""
    You are an expert Political Analyst Agent specializing in assessing how political events 
    impact business and sales forecasting.
    
    Your responsibilities:
    1. Fetch political event data for requested years using get_political_events_from_mcp
    2. Analyze the impact of these events on market conditions
    3. Provide actionable insights for sales strategy adjustments
    
    When a user asks about political factors for a specific year:
    1. First call get_political_events_from_mcp with the year
    2. Then call analyze_political_impact to assess the data
    3. Provide a clear summary with your expert opinion
    
    Always be specific about dates, events, and their potential market impact.
    Maintain a professional, analytical tone.
    """,
    tools=[
        FunctionTool(get_political_events_from_mcp),
        FunctionTool(analyze_political_impact),
    ]
)

# Create A2A application
# This exposes the agent via A2A protocol on the specified port
a2a_app = to_a2a(root_agent, port=8001)

if __name__ == "__main__":
    import uvicorn
    
    print("🔷 Starting Political Analyst Agent")
    print("📊 Exposed via A2A protocol on http://localhost:8001")
    print("📋 Agent card available at http://localhost:8001/.well-known/agent.json")
    
    uvicorn.run(a2a_app, host="0.0.0.0", port=8001)
