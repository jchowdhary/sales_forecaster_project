"""
GDP Analyst Agent - A2A Enabled Remote Agent
Uses ADK with MCP tools to analyze economic trends for sales forecasting

This agent connects to the MCP server to fetch GDP and economic data
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


async def get_gdp_data_from_mcp(year: str, quarter: str = "all") -> str:
    """
    Fetch GDP data from MCP server.
    
    Args:
        year: The year to query (e.g., "2024", "2025")
        quarter: Specific quarter ("q1", "q2", "q3", "q4") or "all"
    
    Returns:
        JSON string with GDP data
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                MCP_SERVER_URL,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {
                        "name": "get_gdp_data",
                        "arguments": {
                            "year": year,
                            "quarter": quarter
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
        return _get_mock_gdp_data(year, quarter)


def _get_mock_gdp_data(year: str, quarter: str) -> str:
    """Fallback mock data when MCP server is unavailable"""
    mock_gdp = {
        "2024": {"q1": 3.4, "q2": 2.8, "q3": 2.9, "q4": 3.1, "annual": 3.1},
        "2025": {"q1": 2.9, "q2": 2.7, "q3": 3.2, "q4": 2.8, "annual": 2.9},
        "2026": {"q1": 2.5, "q2": 2.8, "q3": None, "q4": None, "annual": None},
    }
    
    data = mock_gdp.get(year, {})
    
    result = {
        "year": year,
        "source": "mock_fallback",
        "retrieved_at": datetime.now().isoformat()
    }
    
    if quarter == "all":
        result["data"] = data
    else:
        result["quarter"] = quarter
        result["growth_rate"] = data.get(quarter.lower())
    
    return json.dumps(result, indent=2)


def analyze_economic_trends(year: str, gdp_data: str) -> str:
    """
    Analyze economic trends based on GDP data.
    
    Args:
        year: The year being analyzed
        gdp_data: JSON string containing GDP data
    
    Returns:
        Analysis report as a string
    """
    try:
        data = json.loads(gdp_data)
        
        if "data" in data:
            gdp_info = data["data"]
        else:
            gdp_info = data
        
        annual = gdp_info.get("annual")
        quarters = [gdp_info.get(f"q{i}") for i in range(1, 5)]
        valid_quarters = [q for q in quarters if q is not None]
        
        # Calculate trend
        if len(valid_quarters) >= 2:
            trend = "improving" if valid_quarters[-1] > valid_quarters[0] else "declining"
        else:
            trend = "stable"
        
        # Determine economic outlook
        if annual:
            if annual >= 3.0:
                outlook = "strong"
                sales_forecast = "bullish"
            elif annual >= 2.0:
                outlook = "moderate"
                sales_forecast = "neutral"
            else:
                outlook = "weak"
                sales_forecast = "cautious"
        else:
            outlook = "uncertain"
            sales_forecast = "data_incomplete"
        
        analysis = {
            "year": year,
            "economic_outlook": outlook,
            "gdp_annual_growth": annual,
            "quarterly_trend": trend,
            "quarterly_data": {
                "q1": gdp_info.get("q1"),
                "q2": gdp_info.get("q2"),
                "q3": gdp_info.get("q3"),
                "q4": gdp_info.get("q4")
            },
            "sales_forecast_stance": sales_forecast,
            "consumer_spending_outlook": _get_consumer_outlook(annual, trend),
            "recommendations": _get_economic_recommendations(outlook, trend),
            "analyzed_at": datetime.now().isoformat()
        }
        
        return json.dumps(analysis, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "year": year})


def _get_consumer_outlook(annual_gdp: float, trend: str) -> dict:
    """Get consumer spending outlook based on GDP data"""
    if annual_gdp and annual_gdp >= 3.0:
        return {
            "level": "strong",
            "confidence": "Consumer confidence likely high, discretionary spending up"
        }
    elif annual_gdp and annual_gdp >= 2.0:
        return {
            "level": "moderate", 
            "confidence": "Consumer spending stable, some caution on big-ticket items"
        }
    else:
        return {
            "level": "cautious",
            "confidence": "Consumers may prioritize essentials over discretionary purchases"
        }


def _get_economic_recommendations(outlook: str, trend: str) -> list:
    """Generate recommendations based on economic analysis"""
    recommendations = []
    
    if outlook == "strong":
        recommendations.append("Expand product lines and marketing spend")
        recommendations.append("Consider aggressive growth targets")
    elif outlook == "moderate":
        recommendations.append("Maintain current strategies with flexibility")
        recommendations.append("Focus on customer retention")
    else:
        recommendations.append("Optimize costs and focus on core products")
        recommendations.append("Build cash reserves for opportunities")
    
    if trend == "improving":
        recommendations.append("Prepare for increased demand in coming quarters")
    elif trend == "declining":
        recommendations.append("Implement hedging strategies against economic softening")
    
    return recommendations


async def get_comprehensive_analysis_from_mcp(year: str) -> str:
    """
    Get comprehensive forecast factors from MCP server.
    
    Args:
        year: The year to analyze
    
    Returns:
        JSON string with combined analysis
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                MCP_SERVER_URL,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {
                        "name": "analyze_forecast_factors",
                        "arguments": {
                            "year": year
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
                return json.dumps({"error": "Unexpected response format"})
            else:
                return json.dumps({"error": f"MCP server returned status {response.status_code}"})
    except Exception as e:
        return json.dumps({"error": str(e), "year": year, "source": "mcp_unavailable"})


# Create the GDP Analyst ADK Agent
root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="gdp_analyst_agent",
    description="Expert economic analyst specializing in GDP trends and their impact on sales forecasting",
    instruction="""
    You are an expert GDP and Economic Analyst Agent specializing in assessing economic trends 
    and their impact on business performance and sales forecasting.
    
    Your responsibilities:
    1. Fetch GDP and economic data for requested years using get_gdp_data_from_mcp
    2. Analyze economic trends and their implications using analyze_economic_trends
    3. Optionally get comprehensive analysis using get_comprehensive_analysis_from_mcp
    4. Provide actionable economic insights for sales strategy
    
    When a user asks about economic factors for a specific year:
    1. First call get_gdp_data_from_mcp with the year
    2. Then call analyze_economic_trends to assess the data
    3. Provide a clear economic outlook with recommendations
    
    Key metrics to focus on:
    - Annual and quarterly GDP growth rates
    - Trend direction (improving/declining/stable)
    - Consumer spending implications
    - Sales strategy recommendations
    
    Maintain a professional, data-driven analytical tone.
    """,
    tools=[
        FunctionTool(get_gdp_data_from_mcp),
        FunctionTool(analyze_economic_trends),
        FunctionTool(get_comprehensive_analysis_from_mcp),
    ]
)

# Create A2A application
# This exposes the agent via A2A protocol on the specified port
a2a_app = to_a2a(root_agent, port=8002)

if __name__ == "__main__":
    import uvicorn
    
    print("📈 Starting GDP Analyst Agent")
    print("📊 Exposed via A2A protocol on http://localhost:8002")
    print("📋 Agent card available at http://localhost:8002/.well-known/agent.json")
    
    uvicorn.run(a2a_app, host="0.0.0.0", port=8002)
