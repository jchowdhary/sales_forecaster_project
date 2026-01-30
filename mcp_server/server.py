"""
MCP Server Implementation for Sales Forecasting Tools
Provides political events and GDP data for forecasting analysis

This server exposes MCP tools via HTTP/REST endpoints for remote agent access
"""
import json
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Sales Forecasting MCP Server",
    description="MCP-compatible server providing political events and GDP data tools",
    version="1.0.0"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data for political events
POLITICAL_EVENTS = {
    "2024": [
        {"date": "2024-11-05", "event": "US Presidential Election", "impact": "high", 
         "description": "Major election cycle affecting market sentiment and policy direction"},
        {"date": "2024-06-15", "event": "G7 Summit", "impact": "medium",
         "description": "International economic policy coordination meeting"},
        {"date": "2024-03-20", "event": "Federal Reserve Policy Meeting", "impact": "high",
         "description": "Interest rate decisions affecting consumer spending"},
    ],
    "2025": [
        {"date": "2025-01-20", "event": "Presidential Inauguration", "impact": "high",
         "description": "New administration begins, policy changes expected"},
        {"date": "2025-04-15", "event": "Tax Policy Changes", "impact": "medium",
         "description": "Corporate and individual tax adjustments take effect"},
        {"date": "2025-09-10", "event": "Climate Summit", "impact": "medium",
         "description": "Green economy policies affecting multiple sectors"},
    ],
    "2026": [
        {"date": "2026-01-15", "event": "Federal Budget Announcement", "impact": "high",
         "description": "Government spending priorities revealed"},
        {"date": "2026-06-20", "event": "Trade Agreement Negotiations", "impact": "high",
         "description": "International trade deals affecting import/export sectors"},
        {"date": "2026-11-03", "event": "Midterm Elections", "impact": "high",
         "description": "Congressional elections affecting legislative agenda"},
    ]
}

# Mock GDP data
GDP_DATA = {
    "2023": {"q1": 2.6, "q2": 2.1, "q3": 4.9, "q4": 3.4, "annual": 3.2,
             "notes": "Strong recovery year with robust consumer spending"},
    "2024": {"q1": 3.4, "q2": 2.8, "q3": 2.9, "q4": 3.1, "annual": 3.1,
             "notes": "Stable growth maintained despite global uncertainties"},
    "2025": {"q1": 2.9, "q2": 2.7, "q3": 3.2, "q4": 2.8, "annual": 2.9,
             "notes": "Moderate growth expected with policy transitions"},
    "2026": {"q1": 2.5, "q2": 2.8, "q3": None, "q4": None, "annual": None,
             "notes": "Projected growth with uncertainty in later quarters"},
}


# Pydantic models for request/response
class ToolCallRequest(BaseModel):
    name: str
    arguments: Dict[str, Any]


class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: int
    method: str
    params: Optional[Dict[str, Any]] = None


# ============================================================================
# TOOL IMPLEMENTATIONS
# ============================================================================

def get_political_events(year: str, impact_level: str = "all") -> Dict[str, Any]:
    """Retrieve political events for a specific year"""
    events = POLITICAL_EVENTS.get(year, [])
    
    if impact_level != "all":
        events = [e for e in events if e["impact"] == impact_level.lower()]
    
    return {
        "year": year,
        "impact_filter": impact_level,
        "event_count": len(events),
        "events": events,
        "retrieved_at": datetime.now().isoformat()
    }


def get_gdp_data(year: str, quarter: str = "all") -> Dict[str, Any]:
    """Retrieve GDP growth data for economic analysis"""
    gdp_info = GDP_DATA.get(year, {})
    
    if not gdp_info:
        return {
            "year": year,
            "error": f"No GDP data available for year {year}",
            "available_years": list(GDP_DATA.keys()),
            "retrieved_at": datetime.now().isoformat()
        }
    
    result = {
        "year": year,
        "retrieved_at": datetime.now().isoformat()
    }
    
    if quarter == "all":
        result["data"] = {
            "q1": gdp_info.get("q1"),
            "q2": gdp_info.get("q2"),
            "q3": gdp_info.get("q3"),
            "q4": gdp_info.get("q4"),
            "annual": gdp_info.get("annual"),
            "notes": gdp_info.get("notes")
        }
        result["note"] = "Values represent percentage GDP growth rates"
    else:
        quarter_key = quarter.lower()
        if quarter_key in gdp_info:
            result["quarter"] = quarter
            result["growth_rate"] = gdp_info[quarter_key]
            result["note"] = f"GDP growth rate for {quarter.upper()} {year} (percentage)"
        else:
            result["error"] = f"Quarter {quarter} not found for year {year}"
    
    return result


def analyze_forecast_factors(year: str) -> Dict[str, Any]:
    """Comprehensive analysis combining political events and GDP data"""
    political_events = POLITICAL_EVENTS.get(year, [])
    gdp_info = GDP_DATA.get(year, {})
    
    high_impact_events = [e for e in political_events if e["impact"] == "high"]
    risk_score = min(len(high_impact_events) * 20, 100)
    
    annual_gdp = gdp_info.get("annual")
    if annual_gdp:
        if annual_gdp >= 3.0:
            outlook = "strong"
            confidence = "high"
        elif annual_gdp >= 2.0:
            outlook = "moderate"
            confidence = "medium"
        else:
            outlook = "weak"
            confidence = "medium"
    else:
        outlook = "uncertain"
        confidence = "low"
    
    def get_recommendation(outlook: str, risk_score: int) -> str:
        if outlook == "strong" and risk_score < 40:
            return "Favorable conditions for aggressive sales targets"
        elif outlook == "strong" and risk_score >= 40:
            return "Good growth potential but monitor political developments"
        elif outlook == "moderate" and risk_score < 40:
            return "Steady growth expected, maintain current strategies"
        elif outlook == "moderate" and risk_score >= 40:
            return "Cautious optimism, prepare contingency plans"
        else:
            return "Conservative approach recommended, focus on risk mitigation"
    
    return {
        "year": year,
        "political_analysis": {
            "risk_score": risk_score,
            "total_events": len(political_events),
            "high_impact_events": len(high_impact_events),
            "key_events": [e["event"] for e in high_impact_events]
        },
        "economic_analysis": {
            "outlook": outlook,
            "gdp_growth": annual_gdp,
            "confidence": confidence,
            "notes": gdp_info.get("notes", "No notes available")
        },
        "combined_assessment": {
            "sales_outlook": f"{outlook}_with_{risk_score}%_political_risk",
            "recommendation": get_recommendation(outlook, risk_score)
        },
        "analyzed_at": datetime.now().isoformat()
    }


# Tool registry
TOOLS = {
    "get_political_events": get_political_events,
    "get_gdp_data": get_gdp_data,
    "analyze_forecast_factors": analyze_forecast_factors,
}

TOOL_DEFINITIONS = [
    {
        "name": "get_political_events",
        "description": "Retrieve political events for a specific year that may impact sales forecasting",
        "inputSchema": {
            "type": "object",
            "properties": {
                "year": {"type": "string", "description": "The year to query (e.g., '2024', '2025', '2026')"},
                "impact_level": {"type": "string", "description": "Filter by impact level - 'high', 'medium', 'low', or 'all'", "default": "all"}
            },
            "required": ["year"]
        }
    },
    {
        "name": "get_gdp_data",
        "description": "Retrieve GDP growth data for economic analysis in sales forecasting",
        "inputSchema": {
            "type": "object",
            "properties": {
                "year": {"type": "string", "description": "The year to query (e.g., '2023', '2024', '2025', '2026')"},
                "quarter": {"type": "string", "description": "Specific quarter ('q1', 'q2', 'q3', 'q4') or 'all'", "default": "all"}
            },
            "required": ["year"]
        }
    },
    {
        "name": "analyze_forecast_factors",
        "description": "Comprehensive analysis combining political events and GDP data for forecasting",
        "inputSchema": {
            "type": "object",
            "properties": {
                "year": {"type": "string", "description": "The year to analyze (e.g., '2024', '2025', '2026')"}
            },
            "required": ["year"]
        }
    }
]


# ============================================================================
# HTTP ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with server info"""
    return {
        "name": "Sales Forecasting MCP Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "tools_list": "/tools",
            "tool_call": "/tools/call",
            "mcp": "/mcp",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/tools")
async def list_tools():
    """List all available tools"""
    return {"tools": TOOL_DEFINITIONS}


@app.post("/tools/call")
async def call_tool(request: ToolCallRequest):
    """Call a specific tool with arguments"""
    tool_name = request.name
    arguments = request.arguments
    
    if tool_name not in TOOLS:
        raise HTTPException(
            status_code=404, 
            detail=f"Tool '{tool_name}' not found. Available tools: {list(TOOLS.keys())}"
        )
    
    try:
        result = TOOLS[tool_name](**arguments)
        return {
            "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
            "isError": False
        }
    except Exception as e:
        return {
            "content": [{"type": "text", "text": str(e)}],
            "isError": True
        }


@app.post("/mcp")
async def mcp_endpoint(request: MCPRequest):
    """MCP JSON-RPC compatible endpoint"""
    
    if request.method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request.id,
            "result": {"tools": TOOL_DEFINITIONS}
        }
    
    elif request.method == "tools/call":
        params = request.params or {}
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name not in TOOLS:
            return {
                "jsonrpc": "2.0",
                "id": request.id,
                "error": {
                    "code": -32601,
                    "message": f"Tool '{tool_name}' not found"
                }
            }
        
        try:
            result = TOOLS[tool_name](**arguments)
            return {
                "jsonrpc": "2.0",
                "id": request.id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
                    "isError": False
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request.id,
                "error": {
                    "code": -32000,
                    "message": str(e)
                }
            }
    
    else:
        return {
            "jsonrpc": "2.0",
            "id": request.id,
            "error": {
                "code": -32601,
                "message": f"Method '{request.method}' not found"
            }
        }


# Direct REST endpoints for easier testing
@app.get("/api/political-events/{year}")
async def get_political_events_rest(year: str, impact_level: str = "all"):
    """REST endpoint for political events"""
    return get_political_events(year, impact_level)


@app.get("/api/gdp/{year}")
async def get_gdp_data_rest(year: str, quarter: str = "all"):
    """REST endpoint for GDP data"""
    return get_gdp_data(year, quarter)


@app.get("/api/forecast-factors/{year}")
async def get_forecast_factors_rest(year: str):
    """REST endpoint for forecast factors"""
    return analyze_forecast_factors(year)


if __name__ == "__main__":
    print("🚀 Starting Sales Forecasting MCP Server")
    print("📊 Available tools: get_political_events, get_gdp_data, analyze_forecast_factors")
    print("🌐 Server running at http://localhost:8000")
    print("")
    print("📋 Endpoints:")
    print("   GET  /              - Server info")
    print("   GET  /health        - Health check")
    print("   GET  /tools         - List available tools")
    print("   POST /tools/call    - Call a tool")
    print("   POST /mcp           - MCP JSON-RPC endpoint")
    print("")
    print("🔧 REST API shortcuts:")
    print("   GET /api/political-events/{year}")
    print("   GET /api/gdp/{year}")
    print("   GET /api/forecast-factors/{year}")
    print("")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
