#!/bin/bash
# ==============================================================================
# CAN-Sentinel: Automated Test Suite Runner
# Runs Normal Traffic, Attack Detection, and Integration tests.
# ==============================================================================

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo -e "${BOLD}${BLUE}======================================================================${NC}"
echo -e "${BOLD}${BLUE}               CAN-SENTINEL AUTOMATED TEST SUITE                     ${NC}"
echo -e "${BOLD}${BLUE}======================================================================${NC}"

FAILURES=0

run_test() {
    local test_name="$1"
    local test_script="$2"

    echo -e "\n${YELLOW}[*] Running: ${test_name}...${NC}"
    if python3 "$test_script"; then
        echo -e "${GREEN}[?] ${test_name} PASSED${NC}"
    else
        echo -e "${RED}[?] ${test_name} FAILED${NC}"
        FAILURES=$((FAILURES + 1))
    fi
}

run_test "Normal Traffic Validation" "tests/normal_traffic/test_normal_traffic.py"
run_test "Cyberattack Anomaly Detection" "tests/attack_traffic/test_attack_detection.py"
run_test "Pipeline Integration & Schema Contract" "tests/integration/test_pipeline.py"

echo -e "\n${BOLD}${BLUE}======================================================================${NC}"
if [ $FAILURES -eq 0 ]; then
    echo -e "${BOLD}${GREEN}  ALL TESTS PASSED! CAN-Sentinel is fully verified and review-ready.  ${NC}"
    echo -e "${BOLD}${BLUE}======================================================================${NC}"
    exit 0
else
    echo -e "${BOLD}${RED}  ${FAILURES} TEST(S) FAILED. Check error logs above.  ${NC}"
    echo -e "${BOLD}${BLUE}======================================================================${NC}"
    exit 1
fi
