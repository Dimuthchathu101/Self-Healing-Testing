import pytest
from predictive_healing import ChangePredictor
import asyncio
from heal_element import heal_element
from certify_healing import certify_healing

# Example element for healing/certification
element = {"name": "login button", "selector": "#login-btn"}

@pytest.mark.asyncio
async def test_login_success(page, locator_model):
    username_locator = locator_model(None, None, "login username field")
    password_locator = locator_model(None, None, "login password field")
    login_btn_locator = locator_model(None, None, "login button")
    await page.goto("http://127.0.0.1:5000/login")
    login_success = False
    try:
        await page.fill(username_locator, 'alice2')
        await page.fill(password_locator, 'password')
        await page.click(login_btn_locator)
        await page.wait_for_url("**/dashboard")
        login_success = True
    except Exception:
        # Use healing strategies if normal selectors fail
        candidate = heal_element(page, element, ["VISUAL_CONTEXT", "SEMANTIC_GRAPH", "XAI_VERIFICATION"])
        if candidate:
            await page.click(candidate.selector)
            await page.wait_for_url("**/dashboard")
            login_success = True
        else:
            predictor = ChangePredictor(repo_path="/Users/testing/Documents/GitHub/Self-Healing-Testing")
            risks = predictor.predict_breakages()
            print("[Predictive Healing] At-risk elements:", risks["affected_elements"])
            print("[Predictive Healing] Tests at risk:", risks["tests_at_risk"])
            print("[Predictive Healing] Suggestion: Try alternative selectors for login fields and button.")
            page_content = await page.content()
            print("[DEBUG] Page content after failed login attempt:\n", page_content)
            cookies = await page.context.cookies()
            print("[DEBUG] Cookies after failed login attempt:", cookies)
            await page.screenshot(path="login_failure_debug.png")
            print("[DEBUG] Screenshot saved as login_failure_debug.png")
            assert False, "Login failed after all self-healing attempts. See predictive healing output above."
    assert login_success
    assert "Welcome" in await page.content()
    # Certify healing across browsers
    assert await certify_healing(["chrome", "firefox"])  # limit to two for demo

@pytest.mark.asyncio
async def test_login_selector_issue(page, locator_model):
    username_locator = locator_model(None, None, "login username field")
    password_locator = locator_model(None, None, "login password field")
    login_btn_locator = locator_model(None, None, "login button")
    await page.goto("http://127.0.0.1:5000/login")
    login_success = False
    try:
        await page.fill(username_locator + "-typo", 'alice2')  # broken
    except Exception:
        try:
            await page.fill(username_locator, 'alice2')
        except Exception:
            await page.fill('input[type="text"]', 'alice2')
    try:
        await page.fill(password_locator, 'password')
        await page.click(login_btn_locator)
        await page.wait_for_url("**/dashboard")
        login_success = True
    except Exception:
        # Use healing strategies if normal selectors fail
        candidate = heal_element(page, element, ["VISUAL_CONTEXT", "SEMANTIC_GRAPH", "XAI_VERIFICATION"])
        if candidate:
            await page.click(candidate.selector)
            await page.wait_for_url("**/dashboard")
            login_success = True
        else:
            predictor = ChangePredictor(repo_path="/Users/testing/Documents/GitHub/Self-Healing-Testing")
            risks = predictor.predict_breakages()
            print("[Predictive Healing] At-risk elements:", risks["affected_elements"])
            print("[Predictive Healing] Tests at risk:", risks["tests_at_risk"])
            print("[Predictive Healing] Suggestion: Try alternative selectors for login fields and button.")
            page_content = await page.content()
            print("[DEBUG] Page content after failed login attempt:\n", page_content)
            cookies = await page.context.cookies()
            print("[DEBUG] Cookies after failed login attempt:", cookies)
            await page.screenshot(path="login_failure_debug.png")
            print("[DEBUG] Screenshot saved as login_failure_debug.png")
            assert False, "Login failed after all self-healing attempts. See predictive healing output above."
    assert login_success
    assert "Welcome" in await page.content()
    # Certify healing across browsers
    assert await certify_healing(["chrome", "firefox"])  # limit to two for demo 