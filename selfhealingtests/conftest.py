import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
from predictive_healing import ChangePredictor
from multimodal_locator import MultiModalLocator

@pytest.fixture(scope="session", autouse=True)
def print_risk_report():
    predictor = ChangePredictor(repo_path="/Users/testing/Documents/GitHub/Self-Healing-Testing")
    risks = predictor.predict_breakages()
    print("\n[Predictive Healing] Tests at risk:", risks["tests_at_risk"])

@pytest_asyncio.fixture
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        yield browser
        await browser.close()

@pytest_asyncio.fixture
async def page(browser):
    context = await browser.new_context()
    page = await context.new_page()
    yield page
    await context.close()

@pytest.fixture(scope="session")
def locator_model():
    # Return a mock MultiModalLocator for test use
    class MockModel:
        def __call__(self, dom_features, screenshot, context_text):
            # Return a plausible locator string based on context_text
            if "username" in context_text:
                return "#login-username"
            if "password" in context_text:
                return "#login-password"
            if "login" in context_text:
                return "#login-btn"
            if "profile username" in context_text:
                return "#profile-username-field"
            if "save" in context_text:
                return "#profile-save-btn"
            if "vendor" in context_text:
                return "#bill-vendor-field"
            if "amount" in context_text:
                return "#bill-amount-field"
            if "pay" in context_text:
                return "button:has-text('Pay')"
            if "search" in context_text:
                return ".search-input"
            if "filter" in context_text:
                return "#filter-btn"
            return "input"
    return MockModel() 