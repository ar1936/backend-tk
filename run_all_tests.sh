#!/bin/bash

# Create reports directory if it doesn't exist
mkdir -p test_reports

echo "Running unit and integration tests..."
pytest -v --html=test_reports/unit_test_report.html --self-contained-html

# Check if pytest-html was installed
if [ $? -ne 0 ]; then
    echo "Installing pytest-html for HTML reports..."
    pip install pytest-html
    pytest -v --html=test_reports/unit_test_report.html --self-contained-html
fi

echo "\nRunning load tests..."
locust -f tests/locustfile.py --headless --users 100 --spawn-rate 5 --run-time 1m --html=test_reports/load_test_report.html

echo "\nTest reports generated in the test_reports/ directory:"
ls -la test_reports/
