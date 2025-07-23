import pytest
from predictive_healing import ChangePredictor
import asyncio

@pytest.mark.asyncio
async def test_billpay_selector_issue(page, locator_model):
    vendor_locator = locator_model(None, None, "vendor field")
    amount_locator = locator_model(None, None, "amount field")
    pay_btn_locator = locator_model(None, None, "pay button")
    # Self-healing login step
    # Retry navigation up to 3 times with increased timeout
    for attempt in range(3):
        try:
            await page.goto("http://127.0.0.1:5000/login", timeout=90000)
            break
        except Exception as e:
            print(f"[DEBUG] Attempt {attempt+1} to load login page failed: {e}")
            if attempt == 2:
                raise
            await asyncio.sleep(3)
    login_success = False
    try:
        await page.fill(locator_model(None, None, "login username field"), 'alice')
        await page.fill(locator_model(None, None, "login password field"), 'password')
        await page.click(locator_model(None, None, "login button"))
        await page.wait_for_url("**/dashboard", timeout=90000)
        login_success = True
    except Exception:
        try:
            await page.fill('#login-username', 'alice')
            await page.fill('#login-password', 'password')
            await page.click('#login-btn')
            await page.wait_for_url("**/dashboard", timeout=90000)
            login_success = True
        except Exception:
            try:
                await page.fill('input[type="text"]', 'alice')
                await page.fill('input[type="password"]', 'password')
                await page.click('button:has-text("Login")')
                await page.wait_for_url("**/dashboard", timeout=90000)
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
    await page.goto("http://127.0.0.1:5000/billpay")
    try:
        await page.fill(vendor_locator + "-typo", 'Electric Co')  # broken
    except Exception:
        await page.fill(vendor_locator, 'Electric Co')
    await page.fill(amount_locator, '50')
    await page.click(pay_btn_locator)
    assert "Paid $50 to Electric Co!" in await page.content() 