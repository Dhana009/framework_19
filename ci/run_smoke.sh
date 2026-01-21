#!/bin/bash

# Smoke Tests Execution Script
# Runs critical smoke tests for quick validation

echo "========================================="
echo "Running Smoke Tests"
echo "========================================="

pytest -m smoke \
  --alluredir=reports/allure-results \
  --html=reports/html-report/smoke_report.html \
  --self-contained-html \
  -v

EXIT_CODE=$?

echo ""
echo "========================================="
echo "Smoke Tests Completed"
echo "Exit Code: $EXIT_CODE"
echo "========================================="

exit $EXIT_CODE
