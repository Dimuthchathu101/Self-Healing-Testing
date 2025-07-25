import pytest
from predictive_healing import ChangePredictor
from multimodal_locator import MultiModalLocator
import asyncio

@pytest.mark.asyncio
async def test_profile_edit_selector_issue(page, locator_model):
    # Use the mock multimodal locator from the fixture
    # Login step (use login page locators)
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
        username_locator = locator_model(None, None, "login username field")
        password_locator = locator_model(None, None, "login password field")
        login_btn_locator = locator_model(None, None, "login button")
        await page.fill(username_locator, 'alice2')
        await page.fill(password_locator, 'password')
        await page.click(login_btn_locator)
        await page.wait_for_url("**/dashboard", timeout=90000)
        login_success = True
    except Exception:
        try:
            await page.fill('#login-username', 'alice2')
            await page.fill('#login-password', 'password')
            await page.click('#login-btn')
            await page.wait_for_url("**/dashboard", timeout=90000)
            login_success = True
        except Exception:
            try:
                await page.fill('input[type="text"]', 'alice2')
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
                await page.screenshot(path="login_failure_profile_debug.png")
                print("[DEBUG] Screenshot saved as login_failure_profile_debug.png")
                assert False, "Login failed after all self-healing attempts. See predictive healing output above."
    # Go to profile page
    await page.goto("http://127.0.0.1:5000/profile")
    # Self-healing: try predicted locator, then fallback
    username_locator = locator_model(None, None, "profile username field")
    save_btn_locator = locator_model(None, None, "save button")
    try:
        await page.fill(username_locator + "-typo", 'alice2')  # broken
    except Exception:
        try:
            await page.fill(username_locator, 'alice2')
        except Exception:
            await page.fill('input[type="text"]', 'alice2')
    await page.click(save_btn_locator)
    assert "Profile updated!" in await page.content() 