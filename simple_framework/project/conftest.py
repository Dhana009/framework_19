from playwright.sync_api import sync_playwright, expect
import pytest

@pytest.fixture(scope='session')
def browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    yield browser
    browser.close()
    playwright.stop()


@pytest.fixture
def context(browser):
    new_context = browser.new_context(
        viewport=None
    )
    new_context.set_default_timeout(30000)
    new_context.set_default_navigation_timeout(30000)

    yield new_context
    new_context.close()

@pytest.fixture
def page(context):
    new_page = context.new_page()
    new_page.goto('https://projects.hackerearth.com/p2#/')
    yield new_page
    new_page.close()