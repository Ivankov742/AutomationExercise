# AutomationExercise — Automated Testing Project

![CI](https://github.com/Ivankov742/AutomationExercise/actions/workflows/tests.yml/badge.svg)
[![Allure Report](https://img.shields.io/badge/Allure-Report-blue)](https://Ivankov742.github.io/AutomationExercise/)

---

## ✅ Overview

Automated tests for the demo site [automationexercise.com](https://automationexercise.com/) covering both **UI** and **API** with clean structure, Page Object pattern, BDD examples, and dual reporting (HTML + Allure).

**Tech stack**
- Python, `pytest`, `pytest-bdd`
- Playwright (UI) with Page Object
- `requests` (API client)
- Allure + HTML reports
- GitHub Actions CI (build, test, publish Allure on GitHub Pages)

---

## 🚀 Test Scope

### UI (BDD + POM)
- **Place Order: Login before Checkout** — [Official Test Case #16](https://automationexercise.com/test_cases#collapse16)

### API
- **Verify login (negative)** — body returns `responseCode=404` on invalid credentials  
- **Search product (positive)** — successful search by keyword  
- **Search product (GET)** — validate `responseCode in {400, 405}` for unsupported method / missing param

> The demo API can return slightly different codes/messages (e.g., 400 vs 405); tests account for that where appropriate.

---

## 🧱 Project Structure



```
AutomationExercise/
├── .github/
│ └── workflows/
│  └── tests.yml    # GitHub Actions: tests + publish Allure to GitHub Pages
├── .gitignore
├── conftest.py   # Playwright/pytest fixtures, artifacts, trace/video, Allure env
├── pytest.ini    # Markers, HTML + Allure addopts, defaults
├── requirements.txt
├── reports/   # Generated on the fly (ignored by Git)
├── tests/
│ ├── data/
│ │ └── config.json   # Base URL, creds, timeouts, payment data, etc.
│ ├── utils/
│ │ ├── data_loader.py
│ │ └── logger.py
│ ├── api/
│ │ ├── client.py   # requests-based API client with logging + Allure attachments
│ │ ├── api_test.py   # Classic pytest tests
│ │ └── api_tests_bdd.py   # BDD steps for API
│ ├── ui/
│ │ ├── pages/
│ │ │ └── place_order_page.py   # Page Object: locators/actions/assertions
│ │ ├── ui_test.py # UI test (non-BDD) using POM
│ │ └── ui_steps_bdd.py # BDD steps for UI
│ └── features/
│  ├── api_tests.feature # BDD scenarios: API
│  └── ui_tests.feature # BDD scenario: Place Order
```

---

## 🛠️ Setup Instructions

1. Clone this repo:

```bash
git clone https://github.com/YourUsername/AutomationExercise.git
cd AutomationExercise
```

2. Virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies + Playwright browsers:

```bash
pip install -r requirements.txt
python -m playwright install
```

---

## ▶️ Running Tests

### ✅ All Tests:
```bash
pytest
```

### ✅ Only UI (headless):
```bash
pytest -m ui
```

### ✅ UI with visible browser + trace + video (debug):
```bash
pytest -m ui --headed --tracing=retain-on-failure --video=retain-on-failure
```

### ✅ Only API:
```bash
pytest -m api
```

### ✅ BDD(UI):
```bash
pytest tests/ui/ui_steps_bdd.py
```

### ✅ BDD(API):
```bash
pytest tests/api/api_tests_bdd.py
```

### ✅ Single test:
```bash
pytest tests/ui/ui_test.py::test_place_order_login_before_checkout --headed
```

### ✅ Optional: pick a browser:
```bash
pytest -m ui --browser=chromium
# or: --browser=firefox / --browser=webkit
```

---

## 📊 Viewing Reports

### ▶️ HTML(local):
```bash
Open ./reports/html/report.html in your browser after a run.
```

### ▶️ Allure (local):
```bash
# Generate static site
allure generate reports/allure-results -o reports/allure-report --clean
# Open in browser
allure open reports/allure-report

# Or quick preview:
allure serve reports/allure-results
```
Allure (GitHub Pages)

- CI generates and publishes a static Allure report to GitHub Pages on each run.
- Use the badge link at the top once your first run completes successfully.

---

## 🛡️ Assumptions / Notes
- POM (place_order_page.py): clear separation of locators, actions, assertions; resilient navigation (wait_until="domcontentloaded", key element waits, optional HTTPS→HTTP fallback).
- Artifacts on failure: screenshot, page HTML, browser console logs, Playwright trace.zip, and optional video (when enabled).
- API client (tests/api/client.py): wraps requests, logs request/response, attaches details to Allure.

---

## 🧰 Troubleshooting
- Headed in CI → will fail (no X server). Run headed only locally.
- “Playwright browsers not found” → run python -m playwright install (use --with-deps on Linux if needed).
- Allure empty → ensure pytest.ini has --alluredir=reports/allure-results, and you ran tests before generating.
- Slow page load / timeouts → increase navigation_ms in config.json. Our POM also retries with HTTP if HTTPS is sluggish.
- API responses differ → the public demo API can vary (e.g., 400 vs 405). Tests include tolerant checks where appropriate.

---
## 🔒 Credentials & Data
- Demo login used in UI: qa_testuser_01@example.com / 123456
- Payment data is dummy and used only to pass the form.