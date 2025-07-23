# Advanced Fintech Application for Self-Healing Test Scripts

This project is a demo fintech web application built with Flask and SQLite, designed specifically to test **Self-Healing Test Scripts with Playwright + Machine Learning**. The app intentionally introduces issues in locators and selectors to challenge and validate self-healing automation.

## Features
- User authentication (login/logout)
- Dashboard with notifications
- Profile page (view/edit user info)
- Bill payments
- Transaction history with search/filter
- Responsive sidebar navigation
- Dark mode toggle

## Intentional Locator/Selector Issues
- **Mismatched IDs:** Some element IDs in the HTML do not match those in the database.
- **Missing Locators:** Some elements (fields, buttons, links) have no locator in the database.
- **Dynamic IDs:** Some elements (e.g., pay button) use randomized IDs.
- **Duplicate IDs:** Some fields intentionally share the same ID.
- **Generic Classes:** Some elements use only a generic class, with no unique selector.
- **Extra Wrappers:** Some elements are wrapped in extra divs or containers.

These issues are designed to break brittle test scripts and provide a real-world scenario for self-healing and ML-based locator recovery.

## Setup Instructions

1. **Clone the repository and enter the project directory:**
   ```bash
   git clone <repo-url>
   cd Self-Healing-Testing
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install flask flask_sqlalchemy
   ```

4. **Seed the database:**
   ```bash
   python -m fintechapplication.seed
   ```

5. **Run the app:**
   ```bash
   python -m fintechapplication.app
   ```

6. **Access the app:**
   Open [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login) in your browser.

## Default Users
- Username: `alice` / Password: `password`
- Username: `bob` / Password: `password`

## Playwright + ML Self-Healing Testing
- Use Playwright to write tests that interact with the UI using locators from the SQLite database (`fintechapplication/fintech.db`).
- Observe how tests fail or self-heal when selectors are missing, mismatched, or dynamic.
- Use this environment to train or validate ML models for locator recovery.

---

**This project is for research and demonstration purposes. Do not use in production.** 