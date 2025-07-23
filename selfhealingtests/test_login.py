import pytest

@pytest.mark.asyncio
async def test_login_success(page, locator_model):
    username_locator = locator_model(None, None, "login username field")
    password_locator = locator_model(None, None, "login password field")
    login_btn_locator = locator_model(None, None, "login button")
    await page.goto("http://127.0.0.1:5000/login")
    await page.fill(username_locator, 'alice')
    await page.fill(password_locator, 'password')
    await page.click(login_btn_locator)
    await page.wait_for_url("**/dashboard")
    assert "Welcome" in await page.content()

@pytest.mark.asyncio
async def test_login_selector_issue(page, locator_model):
    username_locator = locator_model(None, None, "login username field")
    password_locator = locator_model(None, None, "login password field")
    login_btn_locator = locator_model(None, None, "login button")
    await page.goto("http://127.0.0.1:5000/login")
    try:
        await page.fill(username_locator + "-typo", 'alice')  # broken
    except Exception:
        await page.fill(username_locator, 'alice')
    await page.fill(password_locator, 'password')
    await page.click(login_btn_locator)
    await page.wait_for_url("**/dashboard")
    assert "Welcome" in await page.content() 