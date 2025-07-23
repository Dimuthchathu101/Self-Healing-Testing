import pytest
from predictive_healing import ChangePredictor

@pytest.mark.asyncio
async def test_transactions_search_selector_issue(page, locator_model):
    filter_btn_locator = locator_model(None, None, "filter button")
    search_input_locator = locator_model(None, None, "search input")
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
                print("[Predictive Healing] Suggestion: Try alternative selectors for login fields and button.")
                page_content = await page.content()
                print("[DEBUG] Page content after failed login attempt:\n", page_content)
                cookies = await page.context.cookies()
                print("[DEBUG] Cookies after failed login attempt:", cookies)
                await page.screenshot(path="login_failure_debug.png")
                print("[DEBUG] Screenshot saved as login_failure_debug.png")
                assert False, "Login failed after all self-healing attempts. See predictive healing output above."
    await page.goto("http://127.0.0.1:5000/transactions")
    await page.fill(search_input_locator, 'transfer')
    try:
        await page.click(filter_btn_locator + "-typo")  # broken
    except Exception:
        await page.click(filter_btn_locator)
    assert "Filtered results for" in await page.content() 