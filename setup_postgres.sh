#!/bin/bash
# ===========================================================================
# NeuroCare Database Setup Script (Linux/macOS)
# ===========================================================================
# This script automates the PostgreSQL database setup for NeuroCare
#
# Requirements:
#   - PostgreSQL installed and running
#   - Python 3.8+ installed
#   - Dependencies installed (pip install -r requirements.txt)
#
# Usage:
#   chmod +x setup_postgres.sh
#   ./setup_postgres.sh
# ===========================================================================

set -e  # Exit on first error

echo ""
echo "=========================================================================="
echo "NeuroCare PostgreSQL Database Setup"
echo "=========================================================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "   Please install Python 3.8+ and try again"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if psycopg2 is available, install if needed
python3 -c "import psycopg2" 2>/dev/null || {
    echo ""
    echo "⚠️  Installing Python dependencies..."
    python3 -m pip install -q -r requirements.txt
}

# Run the Python setup script
echo ""
echo "Running database setup..."
echo ""

if python3 setup_postgres.py; then
    echo ""
    echo "=========================================================================="
    echo "✅ Setup completed successfully!"
    echo "=========================================================================="
    echo ""
    echo "Next steps:"
    echo "  1. Verify your database is running: psql -U postgres -h localhost"
    echo "  2. You can now start the Django development server:"
    echo "     python3 manage.py runserver"
    echo ""
    exit 0
else
    echo ""
    echo "❌ Setup failed. Please check the errors above."
    echo ""
    exit 1
fi
