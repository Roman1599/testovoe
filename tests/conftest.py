
import uuid

import pytest
import allure
from allure_commons.types import AttachmentType

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def random_credentials():
    # Рандомные данные для негативного логина
    return str(uuid.uuid4()), str(uuid.uuid4())


def _attach_debug_artifacts(driver):
    try:
        allure.attach(driver.get_screenshot_as_png(), "screenshot", AttachmentType.PNG)
    except Exception:
        pass

    try:
        allure.attach(driver.page_source, "page_source", AttachmentType.HTML)
    except Exception:
        pass

    try:
        allure.attach(driver.current_url, "current_url", AttachmentType.TEXT)
    except Exception:
        pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv:
            _attach_debug_artifacts(drv)