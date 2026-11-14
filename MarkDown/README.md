# Testing
Steps to run the tests
1. Install dependencies
python3 -m pip install --break-system-packages pytest pytest-cov
2. Run the test suite
-> Navigate to project root -> cd Plant-and-Bees -> python3 -m pytest
3. To get a coverage report (a new one)
-> python3 -m pytest --cov=Base --cov=Manager --cov=States --cov=Head --cov-report=term-missing --cov-report=markdown:MarkDown/coverage.md