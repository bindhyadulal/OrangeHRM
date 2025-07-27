from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time



class OrangeHRMLoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
        self.dashboard_url = "/dashboard/index"

        # Element Locators
        self.username_input = (By.NAME, "username")
        self.password_input = (By.NAME, "password")
        self.login_button = (By.CSS_SELECTOR, "button[type='submit']")
        self.invalid_credentials_alert = (
            By.XPATH,
            "//div[contains(@class, 'oxd-alert')]//p[contains(., 'Invalid')]"
        )

    def open_login_page(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        assert self.wait.until(ec.presence_of_element_located(self.username_input)), "Username input not found"

    def assert_no_error_alert(self):
        error_elements = self.driver.find_elements(*self.invalid_credentials_alert)
        assert len(error_elements) == 0, "Error alert present on initial load"
        print("No error alert on initial load")

    def login(self, username, password):
        username_field = self.wait.until(ec.element_to_be_clickable(self.username_input))
        password_field = self.wait.until(ec.element_to_be_clickable(self.password_input))

        username_field.clear()
        password_field.clear()
        username_field.send_keys(username)
        password_field.send_keys(password)

        login_btn = self.wait.until(ec.element_to_be_clickable(self.login_button))
        login_btn.click()

    def assert_error_alert_visible(self):
        time.sleep(1)
        self.wait.until(lambda d: d.execute_script("return document.readyState === 'complete'"))
        alert_present = self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "div.oxd-alert")))
        alert_visible = self.wait.until(ec.visibility_of_element_located(self.invalid_credentials_alert))

        assert alert_present and alert_visible, "Error alert not found or not visible"
        print(f"Error alert displayed with text: '{alert_visible.text}'")
        self.driver.save_screenshot("error_alert_screenshot.png")

    def assert_dashboard_loaded(self):
        assert self.wait.until(ec.url_contains(self.dashboard_url)), "Dashboard URL not loaded"
        print("Dashboard URL loaded successfully")
        self.driver.save_screenshot("dashboard_screenshot.png")


# ==== Main Test Runner ====

def main():
    driver = webdriver.Chrome()
    login_page = OrangeHRMLoginPage(driver)

    try:
        # Test 1: Initial page load
        print("\n=== Test 1: Initial page load ===")
        login_page.open_login_page()
        login_page.assert_no_error_alert()

        # Test 2: Correct username + incorrect password
        print("\n=== Test 2: Correct username + incorrect password ===")
        login_page.login("Admin", "wrongPassword123")
        login_page.assert_error_alert_visible()

        # Reset
        login_page.open_login_page()

        # Test 3: Incorrect username + correct password
        print("\n=== Test 3: Incorrect username + correct password ===")
        login_page.login("WrongUser", "admin123")
        login_page.assert_error_alert_visible()

        # Reset
        login_page.open_login_page()

        # Test 4: Correct credentials
        print("\n=== Test 4: Correct credentials ===")
        login_page.login("Admin", "admin123")
        login_page.assert_dashboard_loaded()

    except AssertionError as e:
        print(f"Test failed: {str(e)}")
        driver.save_screenshot("test_failure.png")
        raise
    finally:
        time.sleep(2)
        driver.quit()


if __name__ == "__main__":
    main()
