#!/bin/bash

# Sanity Tests Execution Script
# Runs feature-level sanity tests

echo "========================================="
echo "Running Sanity Tests"
echo "========================================="

pytest -m sanity \
  --alluredir=reports/allure-results \
  --html=reports/html-report/sanity_report.html \
  --self-contained-html \
  -v

EXIT_CODE=$?

echo ""
echo "========================================="
echo "Sanity Tests Completed"
echo "Exit Code: $EXIT_CODE"
echo "========================================="

exit $EXIT_CODE
