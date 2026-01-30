# 🚀 Sales Forecasting System with ADK, A2A, and MCP

A complete end-to-end multi-agent system showcasing the integration of **Google ADK** (Agent Development Kit), **A2A** (Agent-to-Agent) protocol, and **MCP** (Model Context Protocol) for building a distributed sales forecasting system.

![Multi-Agentic Sales Forecaster using ADK,CrewAI,MCP with A2A Communication](https://github.com/jchowdhary/sales_forecaster_project/blob/master/MultiAgenticA2AWithMCP.png)

## 🏗️ Architecture Overview

This project demonstrates a **production-ready, modular architecture** where specialized agents collaborate via A2A protocol, with data provided through MCP servers.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATOR (ADK Web UI)                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   Sales Forecast Orchestrator Agent                                  │   │
│  │   - Coordinates analysis via A2A protocol                           │   │
│  │   - Uses RemoteA2aAgent to connect to specialists                   │   │
│  │   - Generates comprehensive forecast reports                        │   │
│  └──────────────────────┬─────────────────────┬───────────────────────┘   │
│                         │                     │                            │
└─────────────────────────┼─────────────────────┼────────────────────────────┘
                          │ A2A Protocol        │ A2A Protocol
                          │ (Port 8001)         │ (Port 8002)
                          │                     │
┌─────────────────────────┼─────────────────────┼────────────────────────────┐
│                         │  REMOTE AGENTS      │                            │
│  ┌──────────────────────▼─────────┐  ┌───────▼───────────────────────┐   │
│  │   Political Analyst Agent       │  │   GDP Analyst Agent            │   │
│  │   - ADK Agent with A2A wrapper  │  │   - ADK Agent with A2A wrapper │   │
│  │   - Analyzes political events   │  │   - Analyzes economic trends   │   │
│  │   - Exposed via to_a2a()        │  │   - Exposed via to_a2a()       │   │
│  └──────────────────────┬──────────┘  └───────┬───────────────────────┘   │
│                         │                     │                            │
│                         └──────────┬──────────┘                            │
│                                    │ HTTP/MCP Protocol                     │
│                                    │ (Port 8000)                           │
│                         ┌──────────▼──────────┐                            │
│                         │     MCP Server      │                            │
│                         │   (FastMCP/HTTP)    │                            │
│                         │ - get_political_events                           │
│                         │ - get_gdp_data                                   │
│                         │ - analyze_forecast_factors                       │
│                         └─────────────────────┘                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Technologies:

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Orchestrator** | Google ADK | Main agent with RemoteA2aAgent connections |
| **Remote Agents** | ADK + A2A | Specialist agents exposed via `to_a2a()` |
| **MCP Server** | FastMCP | Data tools provider with HTTP transport |
| **Communication** | A2A Protocol | Agent-to-agent communication standard |

## 📂 Project Structure

```
sales_forecaster_project/
├── README.md                    # This file
├── setup.sh                     # Complete setup script
├── start_all.sh                 # Start all services script
│
├── mcp_server/                  # MCP Data Tools Server
│   ├── .env                     # Server configuration
│   ├── requirements.txt         # Dependencies
│   └── server.py                # FastMCP server with tools
│
├── political_agent/             # Political Analyst Remote Agent
│   ├── .env                     # Agent configuration + API key
│   ├── requirements.txt         # Dependencies
│   └── agent.py                 # ADK agent with A2A wrapper
│
├── gdp_agent/                   # GDP Analyst Remote Agent
│   ├── .env                     # Agent configuration + API key
│   ├── requirements.txt         # Dependencies
│   └── agent.py                 # ADK agent with A2A wrapper
│
└── orchestrator_agent/          # Main Orchestrator Agent
    ├── .env                     # Agent configuration + API key
    ├── requirements.txt         # Dependencies
    └── sales_orchestrator/      # Agent directory (ADK scans this)
        ├── __init__.py
        └── agent.py             # ADK agent with RemoteA2aAgent
```

## 🔧 Prerequisites

- **Python 3.10+** (3.12+ recommended)
- **pip** and **venv** support
- **Google API Key** (Gemini API access)

### Getting a Google API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Save it for the setup process

## 🚀 Quick Setup

### Option 1: Automated Setup

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

### Option 2: Manual Setup

#### 1. Setup MCP Server

```bash
cd mcp_server
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
deactivate
```

#### 2. Setup Political Agent

```bash
cd political_agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
```

#### 3. Setup GDP Agent

```bash
cd gdp_agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
```

#### 4. Setup Orchestrator Agent

```bash
cd orchestrator_agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
```

### 3. Configure API Keys

Edit the `.env` files in each agent directory and add your Google API Key:

```bash
# In political_agent/.env, gdp_agent/.env, and orchestrator_agent/.env
GOOGLE_API_KEY=your_actual_api_key_here
```

## 🎯 Running the System

You'll need **4 terminal windows** to run the complete system:

### Terminal 1: Start MCP Server

```bash
cd mcp_server
source .venv/bin/activate
python server.py
```

**Expected Output:**
```
🚀 Starting Sales Forecasting MCP Server
📊 Available tools: get_political_events, get_gdp_data, analyze_forecast_factors
🌐 Running on http://localhost:8000
```

### Terminal 2: Start Political Analyst Agent

```bash
cd political_agent
source .venv/bin/activate
python agent.py
```

**Expected Output:**
```
🔷 Starting Political Analyst Agent
📊 Exposed via A2A protocol on http://localhost:8001
📋 Agent card available at http://localhost:8001/.well-known/agent.json
```

### Terminal 3: Start GDP Analyst Agent

```bash
cd gdp_agent
source .venv/bin/activate
python agent.py
```

**Expected Output:**
```
📈 Starting GDP Analyst Agent
📊 Exposed via A2A protocol on http://localhost:8002
📋 Agent card available at http://localhost:8002/.well-known/agent.json
```

### Terminal 4: Start Orchestrator (ADK Web UI)

```bash
cd orchestrator_agent
source .venv/bin/activate
adk web .
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:8000
```

Open your browser to **http://localhost:8000** and select **sales_orchestrator** from the agent dropdown to start chatting!

## 💡 Example Prompts to Test

Once the ADK Web UI is running, try these example prompts:

### Basic Forecast Request
```
What's the sales forecast outlook for 2025?
```

### Specific Year Analysis
```
Analyze the political and economic factors affecting sales in 2026
```

### Comparative Analysis
```
Compare the sales outlook between 2024 and 2025
```

### Political Focus
```
What are the key political events in 2025 that could affect our sales?
```

### Economic Focus
```
Give me the GDP trends and economic outlook for 2024
```

### Comprehensive Report
```
Generate a comprehensive sales forecast report for 2025 including both political and economic analysis
```

## 🧪 Testing Individual Components

### Test MCP Server Tools
```bash
# Test get_political_events
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_political_events","arguments":{"year":"2025","impact_level":"all"}}}'
```

### Verify A2A Agent Cards
```bash
# Political Analyst Agent Card
curl http://localhost:8001/.well-known/agent.json | jq

# GDP Analyst Agent Card
curl http://localhost:8002/.well-known/agent.json | jq
```

## 🔧 System Components Explained

### 1. MCP Server (`mcp_server/server.py`)

Provides three data tools via FastMCP with HTTP transport:

| Tool | Description |
|------|-------------|
| `get_political_events` | Returns political events by year and impact level |
| `get_gdp_data` | Returns GDP growth data by year and quarter |
| `analyze_forecast_factors` | Combined political and economic analysis |

### 2. Political Analyst Agent (`political_agent/agent.py`)

- **Type**: ADK Agent exposed via A2A
- **Port**: 8001
- **Purpose**: Analyzes political events and their market impact
- **Tools**: Connects to MCP server for political data

### 3. GDP Analyst Agent (`gdp_agent/agent.py`)

- **Type**: ADK Agent exposed via A2A
- **Port**: 8002
- **Purpose**: Analyzes economic trends and GDP data
- **Tools**: Connects to MCP server for economic data

### 4. Orchestrator Agent (`orchestrator_agent/agent.py`)

- **Type**: ADK Agent with RemoteA2aAgent sub-agents
- **Interface**: ADK Web UI
- **Purpose**: Coordinates specialist agents, generates reports
- **Connections**: Uses A2A protocol to communicate with remote agents

## 🛑 Stopping the System

1. Press `Ctrl+C` in each terminal window
2. Or use the `start_all.sh` script which handles cleanup automatically

## 🐛 Troubleshooting

### Issue: "Connection Refused" errors

**Solution**: Start services in the correct order:
1. MCP Server first (port 8000)
2. Remote agents (ports 8001, 8002)
3. Orchestrator last

### Issue: Import errors

**Solution**: Ensure you're in the correct virtual environment:
```bash
which python  # Should show path to .venv/bin/python
pip list      # Verify packages are installed
```

### Issue: "No root_agent found" or "No agent defined" errors

**Solution**: This happens when ADK scans directories it shouldn't. Make sure:
1. Your virtual environment is named `.venv` (hidden directory)
2. Run `adk web .` from INSIDE the `orchestrator_agent` directory
3. Select `sales_orchestrator` from the agent dropdown in the web UI

### Issue: "Agent not available" errors

**Solution**: Check that remote agents are running:
```bash
# Check if ports are listening
netstat -tuln | grep -E '8000|8001|8002'
# Or
lsof -i :8001
lsof -i :8002
```

### Issue: API Key errors

**Solution**: Verify your `.env` files contain the correct API key:
```bash
cat political_agent/.env
cat gdp_agent/.env
cat orchestrator_agent/.env
```

### Issue: MCP Server not responding

**Solution**: The MCP server uses stdio transport by default. It's designed to be called by agents, not directly via HTTP. Verify it starts without errors.

## 📚 Key Concepts Demonstrated

### 1. **Google ADK (Agent Development Kit)**
- Agent definition with instructions and tools
- FunctionTool for custom tool integration
- RemoteA2aAgent for A2A client connections
- ADK Web UI for interaction

### 2. **A2A (Agent-to-Agent) Protocol**
- `to_a2a()` function for exposing agents
- Agent card auto-generation
- RemoteA2aAgent for consuming remote agents
- Well-known agent card endpoints

### 3. **MCP (Model Context Protocol)**
- FastMCP server with HTTP transport
- `@mcp.tool()` decorator for tool definition
- JSON-RPC based communication
- Tool calling from agents

### 4. **Multi-Agent Architecture**
- Orchestrator pattern with specialist agents
- Separation of concerns (political vs economic analysis)
- Independent scaling of components
- Modular, maintainable design

## 🔐 Security Notes

- Never commit `.env` files with real API keys to version control
- Use environment variables for secrets in production
- Consider implementing authentication for A2A endpoints in production
- The mock data is for demonstration; connect to real APIs in production

## 📈 Extending the System

### Add New Specialist Agents

1. Create a new directory (e.g., `market_agent/`)
2. Define an ADK agent with relevant tools
3. Wrap with `to_a2a()` and expose on a unique port
4. Add `RemoteA2aAgent` reference in orchestrator

### Add New MCP Tools

1. Add tool function in `mcp_server/server.py` with `@mcp.tool()` decorator
2. Update remote agents to call the new tool
3. No changes needed in orchestrator (tools are accessed via remote agents)

### Connect to Real Data Sources

Replace mock data functions with real API calls:
- Political events: Connect to news APIs, government databases
- GDP data: Connect to World Bank, Federal Reserve APIs

## 📄 License

This project is for educational purposes demonstrating ADK, A2A, and MCP integration.

---

**Built with**: Google ADK, A2A Protocol, MCP, FastMCP

**Version**: 2.0.0
