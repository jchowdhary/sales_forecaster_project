#!/bin/bash

# ============================================================================
# Sales Forecaster Project - Start All Services
# ============================================================================
# This script starts all services in separate background processes
# Use Ctrl+C to stop all services
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Array to store PIDs
declare -a PIDS=()

# Cleanup function
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down all services...${NC}"
    for pid in "${PIDS[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null
            echo "Stopped process $pid"
        fi
    done
    echo -e "${GREEN}All services stopped${NC}"
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM

echo "=============================================="
echo -e "${BLUE}Sales Forecaster - Starting All Services${NC}"
echo "=============================================="
echo ""

# Start MCP Server
echo -e "${YELLOW}Starting MCP Server on port 8000...${NC}"
cd "$SCRIPT_DIR/mcp_server"
source .venv/bin/activate
python server.py &
PIDS+=($!)
sleep 2
echo -e "${GREEN}✓ MCP Server started (PID: ${PIDS[-1]})${NC}"

# Start Political Agent
echo -e "${YELLOW}Starting Political Agent on port 8001...${NC}"
cd "$SCRIPT_DIR/political_agent"
source .venv/bin/activate
python agent.py &
PIDS+=($!)
sleep 2
echo -e "${GREEN}✓ Political Agent started (PID: ${PIDS[-1]})${NC}"

# Start GDP Agent
echo -e "${YELLOW}Starting GDP Agent on port 8002...${NC}"
cd "$SCRIPT_DIR/gdp_agent"
source .venv/bin/activate
python agent.py &
PIDS+=($!)
sleep 2
echo -e "${GREEN}✓ GDP Agent started (PID: ${PIDS[-1]})${NC}"

echo ""
echo "=============================================="
echo -e "${GREEN}All background services are running!${NC}"
echo "=============================================="
echo ""
echo "Service URLs:"
echo "  - MCP Server:      http://localhost:8000/mcp"
echo "  - Political Agent: http://localhost:8001"
echo "  - GDP Agent:       http://localhost:8002"
echo ""
echo "To start the Orchestrator (ADK Web UI):"
echo "  cd orchestrator_agent && source .venv/bin/activate && adk web ."
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for background processes
wait
