#!/bin/bash

# 1. Navigate to the repository root directory (safeguard for CI runners)
cd "$(dirname "$0")"

echo "===================================================="
echo "🚀 Starting Automated CI Test Pipeline Suite"
echo "===================================================="

# 2. Activate the virtual environment
# In standard Linux/macOS or Git Bash environments, this uses the 'bin' folder
if [ -d "env/bin" ]; then
    echo "📦 Activating Linux/macOS Virtual Environment..."
    source env/bin/activate
elif [ -d "env/Scripts" ]; then
    echo "📦 Activating Windows Git Bash Virtual Environment..."
    source env/Scripts/activate
else
    echo "⚠️ Warning: 'env' directory not found. Proceeding with system python..."
fi

# 3. Execute the Pytest test suite
echo "🧪 Running Pytest validations..."
pytest test_app.py
TEST_EXIT_CODE=$?

# 4. Enforce Explicit Exit Codes (Requirement)
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "===================================================="
    echo "✅ SUCCESS: All tests passed flawlessly! Exit code: 0"
    echo "===================================================="
    exit 0
else
    echo "===================================================="
    echo "❌ FAILURE: Test suite regression found. Exit code: 1"
    echo "===================================================="
    exit 1
fi