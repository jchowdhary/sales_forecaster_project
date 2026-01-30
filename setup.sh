#!/bin/bash

# ============================================================================
# Sales Forecaster Project - Complete Setup Script
# ============================================================================
# This script sets up all virtual environments for each component
# ============================================================================

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_CMD="${PYTHON_CMD:-python3}"

echo "=============================================="
echo "Sales Forecaster Project - Complete Setup"
echo "=============================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to setup a component
setup_component() {
    local component=$1
    local dir="$SCRIPT_DIR/$component"
    
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}Setting up: $component${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    cd "$dir"
    
    # Create virtual environment if it doesn't exist
    # Use .venv (hidden directory) to avoid ADK scanning it as an agent
    if [ ! -d ".venv" ]; then
        echo "Creating virtual environment (.venv)..."
        $PYTHON_CMD -m venv .venv
    fi
    
    # Activate and install dependencies
    echo "Installing dependencies..."
    source .venv/bin/activate
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt
    
    deactivate
    
    echo -e "${GREEN}✓ $component setup complete${NC}"
    echo ""
    
    cd "$SCRIPT_DIR"
}

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}Error: Python $REQUIRED_VERSION or higher is required (found $PYTHON_VERSION)${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python $PYTHON_VERSION detected${NC}"
echo ""

# Setup each component
setup_component "mcp_server"
setup_component "political_agent"
setup_component "gdp_agent"
setup_component "orchestrator_agent"

echo "=============================================="
echo -e "${GREEN}✓ All components setup successfully!${NC}"
echo "=============================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Configure your Google API Key in each .env file:"
echo "   - political_agent/.env"
echo "   - gdp_agent/.env"
echo "   - orchestrator_agent/.env"
echo ""
echo "2. Start the system (in separate terminals):"
echo ""
echo "   Terminal 1 - MCP Server:"
echo "   cd mcp_server && source .venv/bin/activate && python server.py"
echo ""
echo "   Terminal 2 - Political Agent:"
echo "   cd political_agent && source .venv/bin/activate && python agent.py"
echo ""
echo "   Terminal 3 - GDP Agent:"  
echo "   cd gdp_agent && source .venv/bin/activate && python agent.py"
echo ""
echo "   Terminal 4 - Orchestrator (ADK Web):"
echo "   cd orchestrator_agent && source .venv/bin/activate && adk web ."
echo ""
echo "=============================================="
