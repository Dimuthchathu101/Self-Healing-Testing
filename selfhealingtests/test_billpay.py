import pytest
from predictive_healing import ChangePredictor

@pytest.mark.asyncio
async def test_billpay_selector_issue(page, locator_model):
    vendor_locator = locator_model(None, None, "vendor field")
    amount_locator = locator_model(None, None, "amount field")
    pay_btn_locator = locator_model(None, None, "pay button")
    # Self-healing login step
    await page.goto("http://127.0.0.1:5000/login")
    login_success = False
    try:
        await page.fill(locator_model(None, None, "login username field"), 'alice')
        await page.fill(locator_model(None, None, "login password field"), 'password')
        await page.click(locator_model(None, None, "login button"))
        await page.wait_for_url("**/dashboard")
        login_success = True
    except Exception:
        try:
            await page.fill('#login-username', 'alice')
            await page.fill('#login-password', 'password')
            await page.click('#login-btn')
            await page.wait_for_url("**/dashboard")
            login_success = True
        except Exception:
            try:
                await page.fill('input[type="text"]', 'alice')
                await page.fill('input[type="password"]', 'password')
                await page.click('button:has-text("Login")')
                await page.wait_for_url("**/dashboard")
                login_success = True
            except Exception:
                # Predictive healing: print at-risk elements and suggest alternatives
                predictor = ChangePredictor(repo_path="/Users/testing/Documents/GitHub/Self-Healing-Testing")
                risks = predictor.predict_breakages()
                print("[Predictive Healing] At-risk elements:", risks["affected_elements"])
                print("[Predictive Healing] Tests at risk:", risks["tests_at_risk"])
                # Optionally, suggest fallback selectors
                print("[Predictive Healing] Suggestion: Try alternative selectors for login fields and button.")
                page_content = await page.content()
                print("[DEBUG] Page content after failed login attempt:\n", page_content)
                assert False, "Login failed after all self-healing attempts. See predictive healing output above."
    await page.goto("http://127.0.0.1:5000/billpay")
    try:
        await page.fill(vendor_locator + "-typo", 'Electric Co')  # broken
    except Exception:
        await page.fill(vendor_locator, 'Electric Co')
    await page.fill(amount_locator, '50')
    await page.click(pay_btn_locator)
    assert "Paid $50 to Electric Co!" in await page.content() 