import pytest

@pytest.mark.asyncio
async def test_profile_edit_selector_issue(page, locator_model):
    # Login step (use login page locators)
    await page.goto("http://127.0.0.1:5000/login")
    await page.fill(locator_model(None, None, "login username field"), 'alice')
    await page.fill(locator_model(None, None, "login password field"), 'password')
    await page.click(locator_model(None, None, "login button"))
    await page.wait_for_url("**/dashboard")
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
            # Fallback: try a generic input selector as last resort
            await page.fill('input[type="text"]', 'alice2')
    await page.click(save_btn_locator)
    assert "Profile updated!" in await page.content() 