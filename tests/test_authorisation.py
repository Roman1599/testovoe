import allure
from allure_commons.types import Severity

from pages.login_page import LoginPage
from config import VALID_USERNAME, VALID_PASSWORD


@allure.epic("Web UI")
@allure.feature("Authentication")
class TestAuth:

    @allure.title("Главная страница логина открывается корректно")
    @allure.story("Open login page")
    @allure.severity(Severity.CRITICAL)
    def test_home_page_opens(self, driver):
        with allure.step("Открыть страницу логина"):
            page = LoginPage(driver).open()

        with allure.step("Проверить URL и ключевые элементы страницы"):
            page.assert_login_page_opened()

    @allure.title("Невалидный логин")
    @allure.story("Negative login")
    @allure.severity(Severity.NORMAL)
    def test_login_negative_shows_error(self, driver, random_credentials):
        username, password = random_credentials

        with allure.step("Открыть страницу логина"):
            page = LoginPage(driver).open().assert_login_page_opened()

        with allure.step("Ввести невалидные данные и нажать Login"):
            page.login(username, password)

        with allure.step("Проверить, что показана ошибка и остались на /login"):
            page.assert_login_page_opened()
            page.assert_flash_contains("your username is invalid")

    @allure.title("Валидный логин + logout работают корректно")
    @allure.story("Positive login + logout")
    @allure.severity(Severity.BLOCKER)
    def test_login_logout_positive(self, driver):
        with allure.step("Открыть страницу логина"):
            page = LoginPage(driver).open().assert_login_page_opened()

        with allure.step("Ввести валидные данные и нажать Login"):
            page.login(VALID_USERNAME, VALID_PASSWORD)

        with allure.step("Проверить успешный вход: flash, URL "):
            page.assert_flash_contains("you logged into a secure area")
            page.assert_secure_page_opened()

        with allure.step("Нажать Logout"):
            page.logout()

        with allure.step("Проверить успешный выход: вернулись на /login и есть flash"):
            page.assert_login_page_opened()
            page.assert_flash_contains("you logged out")