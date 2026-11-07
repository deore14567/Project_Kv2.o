#!/usr/bin/env bash
# =========================================================================
# Village Setu — Quick Start Script (run after setup.sh has been run once)
# =========================================================================
# Starts the server using the existing virtual environment and .env.
# If .env doesn't exist yet, runs setup.sh instead.
# =========================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if setup has been run
if [ ! -f ".env" ] || [ ! -d ".venv" ]; then
    echo -e "${YELLOW}⚠ First run detected — running setup.sh first...${NC}"
    exec ./setup.sh
fi

# Activate virtual environment
source .venv/bin/activate

# Ensure database is initialized (idempotent)
echo -e "${BLUE}Checking database...${NC}"
python3 -c "
from backend.database import init_db, seed_admin_if_missing
init_db()
seed_admin_if_missing()
" 2>/dev/null || true

echo -e "${GREEN}✓ Ready — starting server at http://localhost:8000${NC}"
echo -e "${YELLOW}  Login: admin@villagesetu.gov.in / Admin@12345${NC}"
echo -e "${YELLOW}  Press Ctrl+C to stop${NC}"
echo ""

# Start uvicorn
exec python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
