import pytest
from predictive_healing import ChangePredictor
import asyncio

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
        try:
            await page.fill('#login-username', 'alice2')
            await page.fill('#login-password', 'password')
            await page.click('#login-btn')
            await page.wait_for_url("**/dashboard")
            login_success = True
        except Exception:
            try:
                await page.fill('input[type="text"]', 'alice2')
                await page.fill('input[type="password"]', 'password')
                await page.click('button:has-text("Login")')
                await page.wait_for_url("**/dashboard")
                login_success = True
            except Exception:
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
        try:
            await page.fill('#login-password', 'password')
            await page.click('#login-btn')
            await page.wait_for_url("**/dashboard")
            login_success = True
        except Exception:
            try:
                await page.fill('input[type="password"]', 'password')
                await page.click('button:has-text("Login")')
                await page.wait_for_url("**/dashboard")
                login_success = True
            except Exception:
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