# AutomationExercise - Automated Testing Project

## ✅ Project Overview

This repository contains automated tests for the demo website [AutomationExercise.com](https://automationexercise.com/). 
It demonstrates both **UI** and **API** automated testing using:
- Python
- Playwright (for UI)
- requests (for API)
- pytest + pytest-bdd (for test execution and BDD structure)
- Allure & HTML reporting

## 🚀 Automated Test Scenarios

### ✅ UI Test (BDD)
- Place Order: Login before Checkout ([Test Case](https://automationexercise.com/test_cases#collapse16))

### ✅ API Tests
- Login with invalid credentials (negative) ([API Doc](https://automationexercise.com/api_list#collapse10))
- Search product (positive) ([API Doc](https://automationexercise.com/api_list#collapse5))

---

## 🔨 Project Structure

```
AutomationExercise/
├── conftest.py               # Pytest fixtures (browser config, etc.)
├── pytest.ini                # Pytest config (markers, reports)
├── requirements.txt          # Dependencies
├── README.md                  # This file
├── reports/                   # Allure & HTML reports (.gitignore)
├── tests/
│   ├── api/
│   │   ├── api_test.py
│   │   ├── api_tests_bdd.py
│   │
│   ├── ui/
│   │   ├── pages/
│   │   │   └── place_order_page.py
│   │   ├── ui_test.py
│   │   └── ui_steps_bdd.py
│   │
│   └── features/
│       ├── api_tests.feature
│       └── ui_tests.feature
└── .github/workflows/
    └── ci.yml (optional)     # GitHub Actions CI/CD (optional)
```

---

## 🛠️ Setup Instructions

1. Clone this repo:

```bash
git clone https://github.com/YourUsername/AutomationExercise.git
cd AutomationExercise
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
playwright install
```

---

## ▶️ Running Tests

### ✅ UI Test:
```bash
pytest tests/ui/ui_test.py --alluredir=reports/allure-results
```

### ✅ API Tests:
```bash
pytest tests/api/api_test.py --alluredir=reports/allure-results
```

### ✅ BDD Tests:
```bash
pytest tests/api/api_tests_bdd.py --alluredir=reports/allure-results
pytest tests/ui/ui_steps_bdd.py --alluredir=reports/allure-results
```

---

## 📊 Viewing Reports

### ▶️ HTML Report:
```bash
pytest --html=reports/html/report.html
```

### ▶️ Allure Report:
```bash
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

---

## 🛡️ Assumptions / Notes
- Demo site may return inconsistent responses (e.g., API might return 405 instead of 404)
- Payment flow may not complete in demo (but success message is checked)
- Dummy credentials for login: `qa_testuser_01@example.com` / `123456`

---

## 🔧 Bonus (Optional)
- GitHub Actions CI/CD workflow in `.github/workflows/ci.yml` (setup ready)
- Supports Playwright screenshots and Allure screenshots on failure
- Example: Add BDD tests for future flows


