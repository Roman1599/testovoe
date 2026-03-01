from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import LOGIN_URL


class LoginPage:
    """
    Page Object для авторизации на https://the-internet.herokuapp.com/login
    """

    # --- Locators  ---
    H2_LOGIN = (By.XPATH, "//h2[normalize-space()='Login Page']")
    USERNAME = (By.XPATH, "//input[@id='username']")
    PASSWORD = (By.XPATH, "//input[@id='password']")
    BTN_LOGIN = (By.XPATH, "//button[@type='submit' and contains(., 'Login')]")

    FLASH = (By.ID, "flash")

    H2_SECURE = (By.XPATH, "//h2[normalize-space()='Secure Area']")
    BTN_LOGOUT = (By.XPATH, "//a[contains(@class,'button') and contains(., 'Logout')]")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ---------- Actions ----------
    def open(self):
        self.driver.get(LOGIN_URL)
        return self

    def login(self, username: str, password: str):
        self._type(self.USERNAME, username)
        self._type(self.PASSWORD, password)
        self._click(self.BTN_LOGIN)
        return self

    def logout(self):
        self._click(self.BTN_LOGOUT)
        return self

    # ---------- Assertions ----------
    def assert_login_page_opened(self):
        assert "/login" in self.driver.current_url, (
            f"Ожидали /login в URL, получили: {self.driver.current_url}"
        )
        self.wait.until(EC.visibility_of_element_located(self.H2_LOGIN))
        self.wait.until(EC.visibility_of_element_located(self.USERNAME))
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD))
        self.wait.until(EC.element_to_be_clickable(self.BTN_LOGIN))
        return self

    def assert_secure_page_opened(self):
        assert "/secure" in self.driver.current_url, (
            f"Ожидали /secure в URL, получили: {self.driver.current_url}"
        )
        self.wait.until(EC.visibility_of_element_located(self.H2_SECURE))
        self.wait.until(EC.element_to_be_clickable(self.BTN_LOGOUT))
        return self

    def flash_text(self) -> str:
        text = self.wait.until(EC.visibility_of_element_located(self.FLASH)).text
        return " ".join(text.split()).lower()

    def assert_flash_contains(self, expected_substring: str):
        actual = self.flash_text()
        exp = expected_substring.lower()
        assert exp in actual, f"Ожидали '{exp}' в flash, получили: '{actual}'"
        return self

    # ---------- Helpers ----------
    def _type(self, locator, value: str):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(value)

    def _click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()