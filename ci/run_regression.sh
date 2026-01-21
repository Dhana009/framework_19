#!/bin/bash

# Regression Tests Execution Script
# Runs comprehensive regression test suite

echo "========================================="
echo "Running Regression Tests"
echo "========================================="

pytest -m regression \
  --alluredir=reports/allure-results \
  --html=reports/html-report/regression_report.html \
  --self-contained-html \
  -v \
  -n auto

EXIT_CODE=$?

echo ""
echo "========================================="
echo "Regression Tests Completed"
echo "Exit Code: $EXIT_CODE"
echo "========================================="

exit $EXIT_CODE
