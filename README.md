# AutomationExercise

![Build](https://github.com/Ivankov742/AutomationExercise/actions/workflows/tests.yml/badge.svg)

Automated UI and API tests using Playwright and Pytest.


Сreated as part of the AQA 3 Assignment.

🔍 Scope of Work
✅ 1 UI test: Place Order (using Playwright, Page Object pattern)
✅ 2 API tests: Login (negative) and Search Product
✅ Clear test structure with pytest fixtures
✅ Reporting: HTML and Allure reports
✅ CI-ready using GitHub Actions

🚀 Automated Test Cases
Type	Scenario Description	API / Page Reference
API	  Verify login with invalid details (negative case)	API: Verify Login
API	  Search product API: Search Product
UI	   Place Order: Login before Checkout	Test Case #16

📂 Project Structure

AutomationExercise/
├── conftest.py               # Shared fixtures for Playwright
├── pytest.ini                # Report generation configs
├── requirements.txt          # Python dependencies
├── README.md                  # This file
├── ui/                       
│   └── ui_test.py            # UI tests using Playwright
└── tests/
    └── api/
        └── api_test.py       # API tests using Playwright's APIRequestContext

⚙️ Setup Instructions

✅ Install Dependencies
pip install -r requirements.txt
playwright install

✅ Run All Tests
pytest

📃 Test Reports
HTML Report:

pytest  # Generates HTML report automatically
# Then open the report
start reports/html/report.html  # Windows
open reports/html/report.html   # macOS

Allure Report:
# Generate and view Allure report
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report

✅ CI/CD: GitHub Actions
This project uses GitHub Actions to:
- Run all tests on push to main
- Show build status with the badge above

See workflow file: .github/workflows/tests.yml

🔧 Technologies Used
- Python 3.11
- Playwright (for UI & API)
- Pytest
- Allure
- pytest-html
- GitHub Actions CI

⚠️ Assumptions & Notes
Test User: A test account (qa_testuser_01@example.com / 123456) is used and deleted during the UI flow.
API endpoints may be unstable and sometimes return inconsistent responses (e.g., incorrect status codes).
The automation focuses on basic happy and negative paths; edge cases are excluded for simplicity.
Allure reports are generated locally; publishing them online (e.g., GitHub Pages) is not configured.


🎯 Future Improvements
Add Page Object Model classes for the entire UI flow
Add parameterization for environments (dev/stage/prod)
Publish Allure reports as a GitHub Pages site
Add BDD (Gherkin) support (optional)